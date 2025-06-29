from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
import uuid
import aiofiles
from PIL import Image
import io

from util.auth import SECRET_KEY, fazer_login, fazer_logout, obter_usuario_logado
from db.repo.imagem_repo import inserir_imagem, criar_tabela_imagens
from db.repo.avaliacao_repo import criar_tabela_avaliacao
from db.repo.usuario_repo import criar_tabela_usuario
from db.repo.profissao_repo import criar_tabela_profissao

criar_tabela_avaliacao()
criar_tabela_imagens()
criar_tabela_usuario()
criar_tabela_profissao()

# Configuração de diretórios
UPLOAD_DIR = Path("uploads")
templates = Jinja2Templates(directory="templates")


# Criar instância do FastAPI
app = FastAPI(title="Upload de Imagem API", version="1.0.0")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/quero-contratar")
async def quero_contratar(request: Request):
    return templates.TemplateResponse("quero-contratar/index.html", {"request": request})

@app.get("/quero-trabalhar", response_class=HTMLResponse)
async def quero_trabalhar(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cadastro")
async def cadastro(request: Request):
    return templates.TemplateResponse("cadastro/index.html", {"request": request})

@app.get("/login")
async def login_html(request: Request):
    return templates.TemplateResponse("login/index.html", {"request": request})

@app.get("/tela-inicio")
async def tela_inicio(request: Request):
    return templates.TemplateResponse("tela_inicio/index.html", {"request": request})

# Configurações de upload
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def is_valid_image(file: UploadFile, contents: bytes) -> bool:
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
    try:
        Image.open(io.BytesIO(contents))
        return True
    except Exception:
        return False

@app.post("/upload")
async def upload_image(request: Request, image: UploadFile = File(...)):
    contents = await image.read()
    if not image.filename:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Arquivo muito grande")
    if not is_valid_image(image, contents):
        raise HTTPException(status_code=400, detail="Arquivo inválido ou formato não suportado")
    nome_arquivo_unico = f"{uuid.uuid4().hex}{Path(image.filename).suffix.lower()}"
    caminho_arquivo = UPLOAD_DIR / nome_arquivo_unico
    async with aiofiles.open(caminho_arquivo, 'wb') as arquivo:
        await arquivo.write(contents)
    # --- Inserir no banco ---
    usuario = obter_usuario_logado(request)
    inserir_imagem(
        usuario_id=usuario.id,
        nome_arquivo=nome_arquivo_unico,
        nome_arquivo_original=image.filename,
        url=f"/uploads/{nome_arquivo_unico}"
    )
    return JSONResponse(content={
        "sucesso": True,
        "nome_arquivo": nome_arquivo_unico,
        "url": f"/uploads/{nome_arquivo_unico}"
    })

@app.get("/uploads/list")
async def listar_uploads():
    uploads = []
    for file_path in UPLOAD_DIR.glob("*"):
        if file_path.is_file():
            stat = file_path.stat()
            uploads.append({
                "nome_arquivo": file_path.name,
                "tamanho_mb": round(stat.st_size / (1024 * 1024), 2),
                "url": f"/uploads/{file_path.name}",
                "criado_em": stat.st_ctime
            })
    uploads.sort(key=lambda x: x["criado_em"], reverse=True)
    return JSONResponse(content={"uploads": uploads})


@app.delete("/uploads/{filename}")
async def delete_upload(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    file_path.unlink()
    return JSONResponse(content={"success": True, "message": f"{filename} deletado"})

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Image Upload API"}

@app.post("/login")
async def login(request: Request, email: str, senha: str):
    usuario = fazer_login(request, email, senha)
    return {"message": "Login realizado com sucesso", "usuario": usuario.email}

@app.post("/logout")
async def logout(request: Request):
    return fazer_logout(request)

@app.get("/perfil")
async def perfil(request: Request):
    usuario = obter_usuario_logado(request)
    return {"usuario": usuario.email}

@app.get("/")
async def index(request: Request):
    # Exemplo: produtos = obter_produtos_por_pagina(1, 12)
    return templates.TemplateResponse("menu/index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    # Executar servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)

