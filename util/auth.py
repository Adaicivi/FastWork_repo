import hashlib
from typing import Optional
from fastapi import HTTPException, Request
from db.repo import usuario_repo
from db.models.usuario import Usuario

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

def obter_usuario_logado(request: Request) -> Optional[Usuario]:
    usuario = request.session.get("usuario")
    if not usuario:
        raise HTTPException(status_code=401, detail="Não autenticado")
    return usuario

