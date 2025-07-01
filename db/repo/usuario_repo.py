from typing import Optional
from util.database import obter_conexao
from db.sql.usuario_sql import *
from db.models.usuario import Usuario
from db.models.endereco import Endereco
from db.models.profissao import Profissao

def criar_tabela_usuarios() -> bool:
    try: 
        with obter_conexao() as conexao:            
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_USUARIO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de usuários: {e}")
        return False

def inserir_usuario(usuario: Usuario) -> Optional[int]:  
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERIR_USUARIO, 
            (usuario.nome, usuario.email, usuario.senha, usuario.data_nascimento,
             usuario.imagem, usuario.experiencia, usuario.cpf, usuario.telefone,
             usuario.link_contato, 
             usuario.endereco.id if usuario.endereco else None,
             usuario.profissao.id if usuario.profissao else None,
             usuario.tipo))
        return cursor.lastrowid

def atualizar_usuario(usuario: Usuario) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_USUARIO, 
            (usuario.nome, usuario.email, usuario.senha, usuario.data_nascimento,
             usuario.imagem, usuario.experiencia, usuario.cpf, usuario.telefone,
             usuario.link_contato,
             usuario.endereco.id if usuario.endereco else None,
             usuario.profissao.id if usuario.profissao else None,
             usuario.tipo, usuario.id))
        return (cursor.rowcount > 0)

def atualizar_tipo_usuario(usuario_id: int, tipo: str) -> bool:  
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_TIPO_USUARIO, (tipo, usuario_id))
        return (cursor.rowcount > 0)

def excluir_usuario(usuario_id: int, senha_hash: str) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETAR_USUARIO_POR_ID_SENHA, (usuario_id, senha_hash))
        return (cursor.rowcount > 0)

def obter_usuario_por_id(usuario_id: int) -> Optional[Usuario]: 
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
                data_nascimento=resultado["data_nascimento"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                endereco=Endereco(
                    id=resultado["endereco_id"],
                    cidade=resultado["endereco_cidade"],
                    uf=resultado["endereco_uf"]
                ) if resultado["endereco_id"] else None,
                imagem=resultado["url_imagem"],
                experiencia=resultado["experiencia"],
                link_contato=resultado["link_contato"],
                profissao=Profissao(
                    id=resultado["profissao_id"],
                    nome=resultado["profissao"],
                    descricao=resultado["profissao_descricao"]
                ) if resultado["profissao_id"] else None,
                tipo=resultado["tipo"])
    return None

def obter_usuarios_por_profissao(profissao_id: int) -> list[Usuario]:
    with obter_conexao() as conexao:      
        cursor = conexao.cursor()
        cursor.execute(BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO, (profissao_id,))
        resultados = cursor.fetchall()
        return [Usuario(
            nome=resultado["nome"],
            email=resultado["email"],
            imagem=resultado["imagem"],
            experiencia=resultado["experiencia"],
            cpf=resultado["cpf"],
            telefone=resultado["telefone"],
            data_nascimento=resultado["data_nascimento"],
            profissao=Profissao(nome=resultado["profissao"]),
            link_contato=resultado["link_contato"],
            endereco=Endereco(id=resultado["endereco_id"]) if resultado["endereco_id"] else None,
            tipo=resultado["tipo"]
        ) for resultado in resultados]

def obter_usuarios_por_pagina(numero_pagina: int, quantidade: int) -> list[Usuario]:
    with obter_conexao() as conexao:
        limite = quantidade
        offset = (numero_pagina - 1) * limite
        cursor = conexao.cursor()
        cursor.execute(OBTER_USUARIO_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [Usuario(
            id=resultado["id"],
            nome=resultado["nome"],
            email=resultado["email"],
            senha=resultado["senha_hash"],
            data_nascimento=resultado["data_nascimento"],
            cpf=resultado["cpf"],
            telefone=resultado["telefone"],
            endereco=Endereco(
                id=resultado["endereco_id"],
                cidade=resultado["endereco_cidade"],
                uf=resultado["endereco_uf"]
            ) if resultado["endereco_id"] else None,
            imagem=resultado["imagem"],
            experiencia=resultado["experiencia"],
            link_contato=resultado["link_contato"],
            profissao=Profissao(
                id=resultado["profissao_id"],
                nome=resultado["profissao"],
                descricao=resultado["profissao_descricao"]
            ) if resultado["profissao_id"] else None,
            tipo=resultado["tipo"]
        ) for resultado in resultados]