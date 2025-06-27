from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
from pathlib import Path
import uuid
from typing import List
import aiofiles
from PIL import Image
import io

from util.auth import SECRET_KEY, fazer_login, fazer_logout, obter_usuario_logado

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

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

# Criar instância do FastAPI
app = FastAPI(title="Upload de Imagem API", version="1.0.0")

# Configuração de diretórios
UPLOAD_DIR = Path("uploads")
STATIC_DIR = Path("static")
TEMPLATES_DIR = Path("templates")

# Criar diretórios se não existirem
UPLOAD_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")

# Configurações
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def validate_image(file: UploadFile) -> bool:
    """Valida se o arquivo é uma imagem válida"""
    # Verificar extensão
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False
    
    # Verificar se é realmente uma imagem
    try:
        # Ler o conteúdo do arquivo
        contents = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        # Tentar abrir com PIL
        Image.open(io.BytesIO(contents))
        return True
    except Exception:
        return False

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal com o modal de upload"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    """Endpoint para upload de imagem"""
    try:
        # Verificar se um arquivo foi enviado
        if not image.filename:
            raise HTTPException(status_code=400, detail="Nenhum arquivo foi enviado")
        
        # Verificar tamanho do arquivo
        contents = await image.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"Arquivo muito grande. Máximo permitido: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Reset file pointer para validação
        await image.seek(0)
        
        # Validar se é uma imagem
        if not validate_image(image):
            raise HTTPException(
                status_code=400, 
                detail="Arquivo não é uma imagem válida ou formato não suportado"
            )
        
        # Gerar nome único para o arquivo
        file_ext = Path(image.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Reset file pointer para salvar
        await image.seek(0)
        
        # Salvar arquivo
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(contents)
        
        # Obter informações do arquivo
        file_size_mb = len(contents) / (1024 * 1024)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Imagem enviada com sucesso!",
                "filename": unique_filename,
                "original_filename": image.filename,
                "size_mb": round(file_size_mb, 2),
                "url": f"/uploads/{unique_filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@app.get("/uploads/list")
async def list_uploads():
    """Listar todas as imagens enviadas"""
    try:
        uploads = []
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                uploads.append({
                    "filename": file_path.name,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "url": f"/uploads/{file_path.name}",
                    "created_at": stat.st_ctime
                })
        
        # Ordenar por data de criação (mais recente primeiro)
        uploads.sort(key=lambda x: x["created_at"], reverse=True)
        
        return JSONResponse(content={"uploads": uploads})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar uploads: {str(e)}")

@app.delete("/uploads/{filename}")
async def delete_upload(filename: str):
    """Deletar uma imagem específica"""
    try:
        file_path = UPLOAD_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        
        file_path.unlink()  # Deletar arquivo
        
        return JSONResponse(content={
            "success": True,
            "message": f"Arquivo {filename} deletado com sucesso"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar arquivo: {str(e)}")

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy", "service": "Image Upload API"}

if __name__ == "__main__":
    import uvicorn
    # Executar servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)

