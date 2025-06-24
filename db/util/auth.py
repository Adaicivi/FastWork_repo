from typing import Optional
from fastapi import HTTPException, Request, Response
import hashlib

from models.usuario import Usuario
from repo import usuario_repo

SECRET_KEY = "729b9f5e3861e5173bb01c12e373a0da69bd3a35bfae7478bdf023811fbafff2"

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha_normal: str, senha_hashed: str) -> bool:
    return hash_senha(senha_normal) == senha_hashed

def autenticar_usuario(email: str, senha: str):
    usuario = usuario_repo.obter_usuario_por_email(email)
    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario


def fazer_login(request: Request, email: str, senha: str):
    usuario = autenticar_usuario(email, senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    request.session["usuario_id"] = usuario.id
    request.session["usuario_email"] = usuario.email
    return usuario

def fazer_logout(request: Request):
    request.session.clear()
    return {"message": "Logout realizado com sucesso"}

def obter_usuario_logado(request: Request) -> Optional[Usuario]:
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        raise HTTPException(status_code=401, detail="Não autenticado")
    
    usuario = usuario_repo.obter_usuario_por_id(usuario_id)
    if not usuario:
        request.session.clear()
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return usuario

if __name__ == "__main__":
    print("Senha do usuário:", hash_senha("123456"))