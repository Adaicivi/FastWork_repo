from db.data.database import obter_conexao
from db.models.endereco import Endereco
from db.sql.usuario_sql import ATUALIZAR_TIPO_USUARIO, ATUALIZAR_USUARIO, BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO, CRIAR_TABELA_USUARIO, DELETAR_USUARIO_POR_ID_SENHA, INSERIR_USUARIO, OBTER_USUARIO_POR_ID, OBTER_USUARIO_POR_PAGINA
from db.models.usuario import Usuario
from db.models.profissao import Profissao
from db.models.endereco import Endereco

def criar_tabela_usuario():
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(CRIAR_TABELA_USUARIO)
    
def inserir_usuario(usuario: Usuario) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            INSERIR_USUARIO,
            (
                usuario.nome,
                usuario.email,
                usuario.senha,
                usuario.data_nascimento,
                usuario.imagem,
                usuario.experiencia,
                usuario.cpf,
                usuario.telefone,
                usuario.link_contato,
                usuario.endereco.id if usuario.endereco else None,  
                usuario.profissao.id if usuario.profissao else None,
                usuario.tipo
            )
        )
        return cursor.lastrowid
    
def atualizar_usuario(usuario: Usuario) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            ATUALIZAR_USUARIO,
            (
                usuario.nome,
                usuario.email,
                usuario.senha,
                usuario.data_nascimento,
                usuario.imagem,
                usuario.experiencia,
                usuario.cpf,
                usuario.telefone,
                usuario.link_contato,
                usuario.endereco.id if usuario.endereco else None,  
                usuario.profissao.id if usuario.profissao else None,
                usuario.tipo,
                usuario.id
            )
        )
        return cursor.lastrowid
    
def atualizar_tipo_usuario(usuario_id: int, tipo: str) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            ATUALIZAR_TIPO_USUARIO,
            (tipo, usuario_id)
        )
        return cursor.lastrowid
    
def buscar_usuarios_ordenados_por_profissao(profissao_id: int) -> list:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO,
            (profissao_id,))
        resultados = cursor.fetchall()
        usuarios = []
        for resultado in resultados:
            usuarios.append(Usuario(
                nome=resultado["nome"],
                email=resultado["email"],
                imagem=resultado["imagem"],
                experiencia=resultado["experiencia"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                data_nascimento=resultado["data_nascimento"],
                profissao=Profissao(
                    nome=resultado["profissao"]
                ),
                link_contato=resultado["link_contato"],
                endereco=Endereco(
                    id=resultado["endereco_id"]
                ) if resultado["endereco_id"] else None,
                tipo=resultado["tipo"]
            ))
        return usuarios

def obter_usuario_por_id(usuario_id: int) -> Usuario:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_USUARIO_POR_ID, (usuario_id,))
        resultado = cursor.fetchone()
        if resultado:
            return Usuario(
                id=usuario_id,
                nome=resultado["nome"],
                email=resultado["email"],
                senha=resultado("senha_hash"),
                data_nascimento=resultado["data_nascimento"],
                imagem=resultado("url_imagem"),
                experiencia=resultado("experiencia"),
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                link_contato=resultado("link_contato"),
                endereco=Endereco(
                    id=resultado("endereco_id"),
                    cidade=resultado("endereco_cidade"),
                    uf=resultado("endereco_uf")
                ) if resultado("endereco_id") else None,
                profissao=Profissao(
                    id=resultado("profissao_id"),
                    nome=resultado("profissao"),
                    descricao=resultado("profissao_descricao")
                ) if resultado("profissao_id") else None,
                tipo=resultado["tipo"]
            )
        return None


def obter_usuario_por_pagina(numero_pagina, quantidade) -> list:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        limite = quantidade
        offset = (numero_pagina - 1) * limite
        cursor.execute(OBTER_USUARIO_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        usuarios = []
        for resultado in resultados:
            usuarios.append(Usuario(
                nome=resultado["nome"],
                imagem=resultado["imagem"],
                data_nascimento=resultado["data_nascimento"],
                profissao=Profissao(
                    nome=resultado["profissao"]
                ),
                endereco=Endereco(
                    id=resultado["endereco_id"]
                )
            ))
        return usuarios
    
def deletar_usuario(usuario_id: int, senha_hash: str) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETAR_USUARIO_POR_ID_SENHA, (usuario_id, senha_hash))
        return cursor.rowcount > 0
