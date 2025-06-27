from data.database import obter_conexao
from db.models.endereco import Endereco
from db.sql.usuario_sql import ATUALIZAR_STATUS_USUARIO, ATUALIZAR_USUARIO, BUSCAR_USUARIOS_ORDENADOS_POR_AVALIACAO, BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO, CRIAR_TABELA_USUARIO, DELETAR_USUARIO_POR_ID_SENHA, INSERIR_AVALIACAO_USUARIO, INSERIR_USUARIO, OBTER_USUARIO_POR_EMAIL_E_SENHA, OBTER_USUARIO_POR_ID
from models.usuario import Usuario
from models.profissao import Profissao

def criar_tabela_usuario():
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(CRIAR_TABELA_USUARIO)
    
def inserir_usuario(usuario: Usuario) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            INSERIR_USUARIO,
             (usuario.nome, usuario.email, usuario.senha, usuario.foto, usuario.exp, usuario.cpf, usuario.telefone, usuario.link_contato ,usuario.endereco.id, usuario.profissao.id, usuario.status, usuario.id)
        )
        return cursor.lastrowid
    
def atualizar_usuario(usuario: Usuario) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            ATUALIZAR_USUARIO,
            (usuario.nome, usuario.email, usuario.senha, usuario.foto, usuario.exp, usuario.cpf, usuario.telefone, usuario.link_contato ,usuario.endereco.id, usuario.profissao.id, usuario.status, usuario.id)
        )
        return cursor.rowcount > 0
    
def inserir_avaliacao_usuario(usuario_id: int, avaliacao: float) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            INSERIR_AVALIACAO_USUARIO,
            (avaliacao, usuario_id)
        )
        return cursor.rowcount > 0
    
def atualizar_status_usuario(usuario_id: int, status: str) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            ATUALIZAR_STATUS_USUARIO,
            (status, usuario_id)
        )
        return cursor.rowcount > 0
    
def buscar_usuarios_ordenados_por_profissao(profissao_id: int) -> list:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO,
            (profissao_id,)
        )
        return cursor.fetchall()

def buscar_usuarios_ordenados_por_avaliacao() -> list:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(BUSCAR_USUARIOS_ORDENADOS_POR_AVALIACAO)
        return cursor.fetchall()

def obter_usuario_por_email(email: str) -> Usuario:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_USUARIO_POR_EMAIL_E_SENHA, (email,))
        resultado = cursor.fetchone()
        if resultado:
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                email=resultado["email"],
                senha=resultado["senha_hash"],
                foto=resultado["foto"],
                exp=resultado["exp"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                link_contato=resultado["link_contato"],
                endereco=Endereco(
                    id=resultado["id"],
                    cidade=resultado["cidade"],
                    uf=resultado["uf"]),
                profissao=Profissao(
                    id=resultado["id"],
                    nome=resultado["nome"],
                    descricao=resultado["descricao"]
                ),
                status=resultado["status"],
                avaliacao=resultado["avaliacao"]
            )
        return None

def obter_usuario_por_id(usuario_id: int) -> Usuario:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_USUARIO_POR_ID, (usuario_id,))
        resultado = cursor.fetchone()
        if resultado:
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                email=resultado["email"],
                senha=resultado["senha_hash"],
                foto=resultado["foto"],
                exp=resultado["exp"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                link_contato=resultado["link_contato"],
                endereco=Endereco(
                    id=resultado["id"],
                    cidade=resultado["cidade"],
                    uf=resultado["uf"]),
                profissao=Profissao(
                    id=resultado["id"],
                    nome=resultado["nome"],
                    descricao=resultado["descricao"]
                ),
                status=resultado["status"],
                avaliacao=resultado["avaliacao"]
            )
        return None
    
def deletar_usuario(usuario_id: int) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETAR_USUARIO_POR_ID_SENHA, (usuario_id,))
        return cursor.rowcount > 0