from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uuid
import aiofiles
from PIL import Image
import io
import re

import uvicorn


from util.auth import SECRET_KEY, autenticar_usuario, hash_senha, obter_usuario_logado
from db.repo.imagem_repo import *
from db.repo.avaliacao_repo import *
from db.repo.usuario_repo import *
from db.repo.profissao_repo import *
from db.models.usuario import Usuario

criar_tabela_avaliacao()
criar_tabela_imagens()
criar_tabela_usuario()
criar_tabela_profissao()

# Configuração de diretórios
UPLOAD_DIR = Path("fastwork_repo/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Criar instância do FastAPI
app = FastAPI(title="Upload de Imagem API", version="1.0.0")
templates = Jinja2Templates(directory="Fastwork_repo/templates")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})

@app.get("/quero-contratar/{id}")
async def quero_contratar(request: Request, id: int):
    usuario = obter_usuario_por_id(id)
    response = templates.TemplateResponse("quero-contratar.html", {"request": request, "usuario": usuario})
    return response

@app.get("/cadastro")
async def read_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.post("/cadastro")
async def cadastrar_usuario(
    request: Request,
    nome: str = Form(),
    email: str = Form(),
    senha: str = Form(),
    foto: UploadFile = File(None),
    exp: str = Form(),
    cpf: str = Form(),
    telefone: str = Form(),
    link_contato: str = Form(),
    endereco: str = Form(),
    profissao: str = Form(),
    status: str = Form(),
    conf_senha: str = Form()
):
    if not validar_cpf(cpf):
        raise HTTPException(status_code=400, detail="CPF inválido")
    if senha != conf_senha:
        raise HTTPException(status_code=400, detail="As senhas não conferem")
    foto_nome = None
    if foto:
        contents = await foto.read()
        if not is_valid_image(foto, contents):
            raise HTTPException(status_code=400, detail="Arquivo inválido ou formato não suportado")
        foto_nome = f"{uuid.uuid4().hex}{Path(foto.filename).suffix.lower()}"
        caminho_arquivo = UPLOAD_DIR / foto_nome
        async with aiofiles.open(caminho_arquivo, 'wb') as arquivo:
            await arquivo.write(contents)
    usuario = Usuario(
        id=0,
        nome=nome,
        email=email,
        foto=foto_nome,
        exp=exp,
        cpf=cpf,
        telefone=telefone,
        link_contato=link_contato,
        endereco=endereco,
        profissao=profissao,
        status=status,
        senha=hash_senha(senha),
        tipo=0
    )
    usuario = inserir_usuario(usuario)
    if not usuario:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar usuário")
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login")
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def fazer_login(
    request: Request, 
    email: str = Form(), 
    senha: str = Form()):
    usuario = autenticar_usuario(email, senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    usuario_json = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": "admin" if usuario.tipo==1 else "user"
    }
    request.session["usuario"] = usuario_json
    return RedirectResponse(url="/", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/quero-trabalhar")
async def perfil(request: Request):
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        return RedirectResponse(url="/login", status_code=303)
    usuario = obter_usuario_por_id(usuario_json["id"])
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return templates.TemplateResponse("quero-trabalhar.html", {"request": request, "usuario": usuario})

@app.post("/quero-trabalhar")
async def atualizar_perfil(
    request: Request,
    nome: str = Form(),
    email: str = Form(),
    foto: UploadFile = File(None),
    exp: str = Form(),
    telefone: str = Form(),
    link_contato: str = Form(),
    endereco: str = Form(),
    profissao: str = Form(),
    status: str = Form(),
):
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    usuario = obter_usuario_por_id(usuario_json["id"])
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.nome = nome
    usuario.email = email
    usuario.foto = foto.filename if foto else None
    if foto:
        contents = await foto.read()
        if not is_valid_image(foto, contents):
            raise HTTPException(status_code=400, detail="Arquivo inválido ou formato não suportado")
        nome_arquivo_unico = f"{uuid.uuid4().hex}{Path(foto.filename).suffix.lower()}"
        caminho_arquivo = UPLOAD_DIR / nome_arquivo_unico
        async with aiofiles.open(caminho_arquivo, 'wb') as arquivo:
            await arquivo.write(contents)
        usuario.foto = nome_arquivo_unico
    usuario.exp = exp
    usuario.telefone = telefone
    usuario.link_contato = link_contato
    usuario.endereco = endereco
    usuario.profissao = profissao
    usuario.status = status
    if not atualizar_usuario(usuario):
        raise HTTPException(status_code=400, detail="Erro ao atualizar perfil")
    usuario_json = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "foto": usuario.foto,
        "exp": usuario.exp,
        "cpf": usuario.cpf,
        "telefone": usuario.telefone,
        "link_contato": usuario.link_contato,
        "endereco": usuario.endereco,
        "profissao": usuario.profissao,
        "status": usuario.status,
        "tipo": "admin" if usuario.tipo == 1 else "user"
    }
    request.session["usuario"] = usuario_json
    return RedirectResponse(url="/quero-trabalhar", status_code=303)

@app.get("/senha")
async def senha(request: Request):
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    usuario = obter_usuario_por_id(usuario_json["id"])
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return templates.TemplateResponse("senha/quero-trabalhar.html", {"request": request, "usuario": usuario})

@app.post("/senha")
async def atualizar_senha(
    request: Request,
    senha_atual: str = Form(),
    nova_senha: str = Form(),
    conf_nova_senha: str = Form()
):
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    usuario = obter_usuario_por_id(usuario_json["id"])
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not autenticar_usuario(usuario.email, senha_atual):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")
    if nova_senha != conf_nova_senha:
        raise HTTPException(status_code=400, detail="As novas senhas não conferem")
    usuario.senha = hash_senha(nova_senha)
    if not atualizar_usuario(usuario):
        raise HTTPException(status_code=400, detail="Erro ao atualizar senha")
    return RedirectResponse(url="/quero-trabalhar", status_code=303)


@app.get("/tela-inicio")
async def tela_inicio(request: Request):
    return templates.TemplateResponse("tela_inicio.html", {"request": request})


# Configurações de upload
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def is_valid_image(file: UploadFile, contents: bytes) -> bool:
    if not file.filename:  # Verificar se filename existe
        return False
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
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
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


if __name__ == "__main__":
    uvicorn.run(app, port=8000)

