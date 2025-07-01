# Imports organizados seguindo padrão do Código 1
from fastapi.responses import RedirectResponse, JSONResponse
import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request, File, UploadFile, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uuid
import aiofiles
from pathlib import Path
from typing import Optional


# Models
from db.models.usuario import Usuario
from db.models.imagem import Imagem


# Repositories  
from db.repo import (
    usuario_repo,
    imagem_repo,
    avaliacao_repo,
)
from db.sql.avaliacao_sql import BUSCAR_MEDIA_AVALIACAO_PROFISSIONAL


# Utils
from util import initializer
from util.auth import SECRET_KEY, autenticar_usuario, hash_senha
from util.validacao import validar_cpf, validar_imagem


# Configurações centralizadas
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
UPLOAD_DIR = Path("uploads")


# Cria as tabelas no banco de dados se não existirem
initializer.criar_tabelas()
# Insere dados iniciais no banco de dados


# Configura diretórios necessários
initializer.configurar_diretorios()


# Cria a instância do FastAPI para a aplicação web
app = FastAPI(title="Sistema de Contratação", version="1.0.0")
# Configura o Jinja2 para renderizar templates HTML
templates = Jinja2Templates(directory="templates")
# Adiciona o middleware de sessão para gerenciar sessões de usuário
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
# Configura arquivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")


# ============================================================================
# ROTAS PRINCIPAIS (seguindo padrão do Código 1)
# ============================================================================


@app.get("/")
def read_root(request: Request):
    # Obtém o usuário logado se existir
    usuario_logado = _obter_usuario_sessao(request)
    # Retorna a página inicial
    response = templates.TemplateResponse("menu.html", {
        "request": request,
        "usuario": usuario_logado
    })
    return response


@app.get("/usuarios")
def read_usuarios(request: Request, page: int = 1, profissao: Optional[str] = None):
    quantidade_por_pagina = 12
    usuarios = usuario_repo.obter_usuarios_por_pagina(page, quantidade_por_pagina)
    usuarios = sorted(usuarios, key=lambda u: (u.tipo != 'a', u.tipo))
    total_usuarios = usuario_repo.contar_usuarios_tipo_ab()
    total_paginas = (total_usuarios + quantidade_por_pagina - 1) // quantidade_por_pagina

    # Agrupa usuários por profissão
    PROFISSOES_VALIDAS = ["Limpeza", "Jardinagem", "Eletricidade", "Encanamento", "Construção"]
    usuarios_por_profissao = {prof: [] for prof in PROFISSOES_VALIDAS}
    for u in usuarios:
        if u.profissao in PROFISSOES_VALIDAS:
            usuarios_por_profissao[u.profissao].append(u)

    medias_avaliacao = {}
    for u in usuarios:
        if u.tipo in ['a', 'b']:
            media = avaliacao_repo.buscar_media_avaliacao_profissional(u.id)
            medias_avaliacao[u.id] = media
    usuario_logado = _obter_usuario_sessao(request)
    return templates.TemplateResponse("quero-contratar.html", {
        "request": request,
        "usuarios_por_profissao": usuarios_por_profissao,
        "pagina_atual": page,
        "total_paginas": total_paginas,
        "total_usuarios": total_usuarios,
        "medias_avaliacao": medias_avaliacao,
        "usuario_logado": usuario_logado,
        "filtro_profissao": profissao or "todos"
    })


@app.get("/usuarios/{id}")
def read_usuario(request: Request, id: int):
    usuario = usuario_repo.obter_usuario_por_id(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario_logado = _obter_usuario_sessao(request)
    return templates.TemplateResponse("quero-contratar.html", {
        "request": request,
        "usuario": [usuario],
        "usuario_logado": usuario_logado
    })


# ============================================================================
# ROTAS DE AUTENTICAÇÃO (seguindo padrão do Código 1)
# ===========================================================================


@app.get("/cadastrar")
def read_cadastrar(request: Request):
    # Retorna a página de cadastro de usuário
    return templates.TemplateResponse("cadastro.html", {"request": request})


@app.post("/cadastrar")
async def cadastrar_usuario(
    request: Request,
    nome: str = Form(),
    email: str = Form(),
    cpf: str = Form(),
    telefone: str = Form(),
    data_nascimento: str = Form(),
    senha_hash: str = Form(),
    conf_senha: str = Form(),
    endereco: Optional[str] = Form(None)
):
    if not validar_cpf(cpf):
        raise HTTPException(status_code=400, detail="CPF inválido")
    if senha_hash != conf_senha:
        raise HTTPException(status_code=400, detail="As senhas não conferem")
    
    usuario = Usuario(
        id=0,
        nome=nome,
        email=email,
        senha_hash=hash_senha(senha_hash),
        cpf=cpf,
        telefone=telefone,
        data_nascimento=data_nascimento,
        experiencia=None,
        imagem=None,
        link_contato=None,
        endereco=endereco,  # Agora é string direta
        profissao=None,     # Agora é string direta
        tipo="c"
    )
    usuario_id = usuario_repo.inserir_usuario(usuario)
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar usuário")
    return RedirectResponse(url="/login", status_code=303)


@app.get("/login")
def read_login(request: Request):
    # Retorna a página de login
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(
    request: Request,
    email: str = Form(),
    senha_hash: str = Form()
):
    # Verifica se o email e senha_hash informados estão corretos
    usuario = autenticar_usuario(email, senha_hash)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
   
    # Se encontrou o usuário, cria um objeto JSON com os dados do usuário
    usuario_json = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo
    }
   
    # Armazena os dados do usuário na sessão
    request.session["usuario"] = usuario_json
    request.session["usuario_id"] = usuario.id
   
    # Redireciona para a página inicial
    return RedirectResponse(url="/usuarios", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    # Limpa a sessão do usuário
    request.session.clear()
    # Redireciona para a página inicial
    return RedirectResponse(url="/", status_code=303)


# ============================================================================
# ROTAS DE PERFIL (seguindo padrão do Código 1)
# ============================================================================


@app.get("/perfil")
async def perfil_usuario(request: Request):
    # Captura os dados do usuário da sessão (logado)
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
   
    # Busca os dados do usuário no repositório
    usuario = usuario_repo.obter_usuario_por_id(usuario_json["id"])
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
   
    # Retorna a página de perfil com os dados do usuário
    return templates.TemplateResponse("quero-trabalhar.html", {
        "request": request,
        "usuario": usuario
    })


@app.post("/perfil")
async def atualizar_perfil(
    request: Request,
    nome: str = Form(),
    email: str = Form(),
    telefone: str = Form(),
    experiencia: str = Form(None),
    link_contato: str = Form(None),
    endereco: str = Form(None),
    profissao: str = Form(None),
    tipo: str = Form("c"),
    imagem: UploadFile = File(None)
):
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    usuario = usuario_repo.obter_usuario_por_id(usuario_json["id"])
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    usuario.nome = nome
    usuario.email = email
    usuario.telefone = telefone
    usuario.experiencia = experiencia
    usuario.link_contato = link_contato
    usuario.tipo = tipo
    usuario.endereco = endereco  # Agora é string direta
    usuario.profissao = profissao  # Agora é string direta

    # Processa a imagem se enviada
    if imagem and imagem.filename:
        contents = await imagem.read()
        if not _validar_upload_imagem(imagem, contents):
            raise HTTPException(status_code=400, detail="Arquivo inválido ou formato não suportado")
        nome_arquivo_unico = f"{uuid.uuid4().hex}{Path(imagem.filename).suffix.lower()}"
        caminho_arquivo = UPLOAD_DIR / nome_arquivo_unico
        async with aiofiles.open(caminho_arquivo, 'wb') as arquivo:
            await arquivo.write(contents)
        # Crie o registro da imagem
        imagem_obj = Imagem(
            id=None,
            usuario_id=usuario.id,
            nome_arquivo=nome_arquivo_unico,
            nome_arquivo_original=imagem.filename,
            url=f"/uploads/{nome_arquivo_unico}",
            criado_em=None
        )
        imagem_id = imagem_repo.inserir_imagem(imagem_obj)
        if not imagem_id:
            raise HTTPException(status_code=400, detail="Erro ao salvar imagem")
        usuario.imagem = f"/uploads/{nome_arquivo_unico}"  # Salve a URL!

    usuario_repo.atualizar_usuario(usuario)
    usuario_json = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo
    }
    request.session["usuario"] = usuario_json
    return RedirectResponse(url="/perfil", status_code=303)


@app.post("/perfil/plano")
async def escolher_plano(request: Request, plano: str = Form(...)):
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    usuario = usuario_repo.obter_usuario_por_id(usuario_json["id"])
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if plano == "basico":
        usuario.tipo = "b"
        usuario_repo.atualizar_tipo_usuario(usuario.id, "b")
        usuario_json["tipo"] = "b"
    elif plano == "premium":
        usuario.tipo = "a"
        usuario_repo.atualizar_tipo_usuario(usuario.id, "a")
        usuario_json["tipo"] = "a"
    else:
        raise HTTPException(status_code=400, detail="Plano inválido")

    request.session["usuario"] = usuario_json
    return RedirectResponse(url="/perfil", status_code=303)

@app.post("/perfil/ativar")
async def ativar_perfil_trabalho(request: Request, ativarPerfil: str = Form(...)):
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    usuario = usuario_repo.obter_usuario_por_id(usuario_json["id"])
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if ativarPerfil == "nao":
        usuario.tipo = "c"
        usuario_repo.atualizar_tipo_usuario(usuario.id, "c")
        usuario_json["tipo"] = "c"
        request.session["usuario"] = usuario_json
    # Se for "sim", não faz nada aqui, pois o plano será escolhido no modal
    return RedirectResponse(url="/perfil", status_code=303)


@app.get("/senha_hash")
async def senha_usuario(request: Request):
    # Captura os dados do usuário da sessão (logado)
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
   
    # Retorna a página de alteração de senha_hash
    return templates.TemplateResponse("senha_hash.html", {"request": request})


@app.post("/senha_hash")
async def atualizar_senha(
    request: Request,
    senha_atual: str = Form(),
    nova_senha: str = Form(),
    conf_nova_senha: str = Form()
):
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
   
    usuario = usuario_repo.obter_usuario_por_id(usuario_json["id"])
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
   
    # Verifica a senha_hash atual
    if not autenticar_usuario(usuario.email, senha_atual):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")
   
    # Verifica se as novas senhas conferem
    if nova_senha != conf_nova_senha:
        raise HTTPException(status_code=400, detail="As senhas não conferem")
   
    # Atualiza a senha_hash do usuário
    if not usuario_repo.atualizar_senha_usuario(usuario.id, hash_senha(nova_senha)):
        raise HTTPException(status_code=400, detail="Erro ao atualizar senha_hash")
   
    return RedirectResponse(url="/perfil", status_code=303)




# ============================================================================
# ROTAS DE UPLOAD DE IMAGEM (nova funcionalidade organizada)
# ============================================================================


@app.get("/usuarios/imagem/{id}")
async def gerenciar_imagem_usuario(request: Request, id: int):
    # Verifica se é o próprio usuário ou admin
    usuario_json = request.session.get("usuario")
    if not usuario_json or (usuario_json["id"] != id and usuario_json.get("tipo") != "admin"):
        raise HTTPException(status_code=403, detail="Acesso negado")
   
    # Busca o usuário
    usuario = usuario_repo.obter_usuario_por_id(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
   
    # Retorna página de gerenciamento de imagem
    return templates.TemplateResponse("gerenciar_imagem.html", {
        "request": request,
        "usuario": usuario
    })


@app.post("/usuarios/imagem/{id}")
async def atualizar_imagem_usuario(
    request: Request,
    id: int,
    imagem: UploadFile = File(...)
):
    # Verifica se é o próprio usuário ou admin
    usuario_json = request.session.get("usuario")
    if not usuario_json or (usuario_json["id"] != id and usuario_json.get("tipo") != "admin"):
        raise HTTPException(status_code=403, detail="Acesso negado")
   
    # Busca o usuário
    usuario = usuario_repo.obter_usuario_por_id(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
   
    # Valida e processa a imagem
    contents = await imagem.read()
    if not _validar_upload_imagem(imagem, contents):
        raise HTTPException(status_code=400, detail="Arquivo inválido ou formato não suportado")
   
    # Salva o arquivo
    nome_arquivo_unico = f"{uuid.uuid4().hex}{Path(imagem.filename).suffix.lower()}"
    caminho_arquivo = UPLOAD_DIR / nome_arquivo_unico
   
    async with aiofiles.open(caminho_arquivo, 'wb') as arquivo:
        await arquivo.write(contents)
   
    # Cria registro da imagem no banco (opcional)
    imagem_obj = Imagem(
        id=None,
        usuario_id=id,
        nome_arquivo=nome_arquivo_unico,
        nome_arquivo_original=imagem.filename,
        url=f"/uploads/{nome_arquivo_unico}",
        criado_em=None
    )
    imagem_id = imagem_repo.inserir_imagem(imagem_obj)
    if not imagem_id:
        raise HTTPException(status_code=400, detail="Erro ao salvar imagem")
    # Salve a URL, não o ID!
    usuario.imagem = f"/uploads/{nome_arquivo_unico}"
    if not usuario_repo.atualizar_usuario(usuario):
        raise HTTPException(status_code=400, detail="Erro ao atualizar imagem do usuário")
   
    # Redireciona para o perfil
    return RedirectResponse(url="/perfil", status_code=303)


@app.delete("/usuarios/imagem/{id}")
async def excluir_imagem_usuario(request: Request, id: int):
    # Verifica se é o próprio usuário ou admin
    usuario_json = request.session.get("usuario")
    if not usuario_json or (usuario_json["id"] != id and usuario_json.get("tipo") != "admin"):
        raise HTTPException(status_code=403, detail="Acesso negado")
   
    # Busca o usuário
    usuario = usuario_repo.obter_usuario_por_id(id)
    if not usuario or not usuario.imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
   
    # Remove o arquivo físico
    imagem = imagem_repo.obter_imagem_por_id(usuario.imagem)
    if imagem:
        caminho_arquivo = UPLOAD_DIR / imagem.nome_arquivo
        if caminho_arquivo.exists():
            caminho_arquivo.unlink()
   
    # Remove a referência do usuário
    usuario.imagem = None
    usuario_repo.atualizar_usuario(usuario)
   
    return JSONResponse(content={"success": True, "message": "Imagem removida"})




# ============================================================================
# ROTAS DE API (funcionalidades extras organizadas)
# ============================================================================


@app.get("/api/uploads/list")
async def listar_uploads():
    # Lista todos os uploads disponíveis
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


@app.get("/api/health")
async def health_check():
    # Endpoint de verificação de saúde da aplicação
    return {"status": "healthy", "service": "Sistema de Contratação"}


# ============================================================================
# FUNÇÕES AUXILIARES (centralizadas)
# ============================================================================


def _obter_usuario_sessao(request: Request):
    """Obtém o usuário da sessão sem lançar exceção"""
    try:
        usuario_json = request.session.get("usuario")
        if usuario_json:
            return usuario_repo.obter_usuario_por_id(usuario_json["id"])
    except Exception:
        pass
    return None


def _validar_upload_imagem(file: UploadFile, contents: bytes) -> bool:
    """Valida se o arquivo de upload é uma imagem válida"""
    if not file.filename:
        return False
   
    # Verifica extensão
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
   
    # Verifica tamanho
    if len(contents) > MAX_FILE_SIZE:
        return False
   
    # Usa validação personalizada se disponível
    try:
        return validar_imagem(file, contents)
    except Exception:
        return False


# ============================================================================
# CONFIGURAÇÃO DE EXECUÇÃO
# ============================================================================


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)

@app.post("/avaliar/{id}")
async def avaliar_profissional(
    request: Request,
    id: int,
    nota: int = Form(...)
):
    usuario_json = request.session.get("usuario")
    if not usuario_json:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    if usuario_json["id"] == id:
        raise HTTPException(status_code=400, detail="Você não pode se autoavaliar.")

    if avaliacao_repo.ja_avaliou(usuario_json["id"], id):
        raise HTTPException(status_code=400, detail="Você já avaliou este profissional.")

    sucesso = avaliacao_repo.inserir_avaliacao(
        usuario_id=usuario_json["id"],
        profissional_id=id,
        nota=nota
    )
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro ao registrar avaliação.")
    return RedirectResponse(url="/usuarios", status_code=status.HTTP_303_SEE_OTHER)