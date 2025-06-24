from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request

from Fastwork_last_version.util.auth import SECRET_KEY, fazer_login, fazer_logout, obter_usuario_logado

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

#
