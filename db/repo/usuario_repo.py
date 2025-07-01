from typing import Optional
from util.database import obter_conexao
from db.sql.usuario_sql import ATUALIZAR_SENHA_USUARIO, ATUALIZAR_TIPO_USUARIO, ATUALIZAR_USUARIO, BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO, CONTAR_USUARIOS_TIPO_AB, CRIAR_TABELA_USUARIO, DELETAR_USUARIO_POR_ID_SENHA, INSERIR_USUARIO, OBTER_USUARIO_POR_EMAIL, OBTER_USUARIO_POR_ID, OBTER_USUARIO_POR_PAGINA  
from db.models.usuario import Usuario

def criar_tabela_usuario() -> bool:
    try: 
        with obter_conexao() as conexao:            
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_USUARIO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de usuários: {e}")
        return False

def inserir_usuario(usuario: Usuario) -> Optional[int]:  
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(INSERIR_USUARIO, 
                (usuario.nome, usuario.email, usuario.senha_hash, usuario.cpf, 
                 usuario.telefone, usuario.data_nascimento, usuario.experiencia, 
                 usuario.imagem, usuario.link_contato, usuario.endereco,
                 usuario.profissao, usuario.tipo))
            return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        return None

def atualizar_usuario(usuario: Usuario) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_USUARIO, (
                usuario.nome,
                usuario.email,
                usuario.senha_hash,
                usuario.cpf,
                usuario.telefone,
                usuario.data_nascimento,
                usuario.experiencia,
                usuario.imagem,
                usuario.link_contato,
                usuario.endereco,
                usuario.profissao,
                usuario.tipo,
                usuario.id
            ))
            return (cursor.rowcount > 0)
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        return False

def atualizar_senha_usuario(usuario_id: int, nova_senha_hash: str) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_SENHA_USUARIO, (nova_senha_hash, usuario_id))
            return (cursor.rowcount > 0)
    except Exception as e:
        print(f"Erro ao atualizar senha do usuário: {e}")
        return False

def atualizar_tipo_usuario(usuario_id: int, tipo: str) -> bool:  
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_TIPO_USUARIO, (tipo, usuario_id))
            return (cursor.rowcount > 0)
    except Exception as e:
        print(f"Erro ao atualizar tipo do usuário: {e}")
        return False

def excluir_usuario(usuario_id: int, senha_hash: str) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(DELETAR_USUARIO_POR_ID_SENHA, (usuario_id, senha_hash))
            return (cursor.rowcount > 0)
    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")
        return False

def obter_usuario_por_id(usuario_id: int) -> Optional[Usuario]: 
    try:
        with obter_conexao() as conexao:   
            cursor = conexao.cursor()
            cursor.execute(OBTER_USUARIO_POR_ID, (usuario_id,))
            resultado = cursor.fetchone()
            if resultado:
                return Usuario(
                    id=resultado["id"],
                    nome=resultado["nome"],
                    email=resultado["email"],
                    senha_hash=resultado["senha_hash"],
                    data_nascimento=resultado["data_nascimento"],
                    cpf=resultado["cpf"],
                    telefone=resultado["telefone"],
                    endereco=resultado["endereco"],
                    imagem=resultado["imagem"],
                    experiencia=resultado["experiencia"],
                    link_contato=resultado["link_contato"],
                    profissao=resultado["profissao"],
                    tipo=resultado["tipo"])
            return None
    except Exception as e:
        print(f"Erro ao obter usuário por ID: {e}")
        return None

def obter_usuario_por_email(email: str) -> Optional[Usuario]:
    try:
        with obter_conexao() as conexao:   
            cursor = conexao.cursor()
            cursor.execute(OBTER_USUARIO_POR_EMAIL, (email,))
            resultado = cursor.fetchone()
            if resultado:
                return Usuario(
                    id=resultado["id"],
                    nome=resultado["nome"],
                    email=resultado["email"],
                    senha_hash=resultado["senha_hash"],
                    data_nascimento=resultado["data_nascimento"],
                    cpf=resultado["cpf"],
                    telefone=resultado["telefone"],
                    endereco=resultado["endereco"],
                    imagem=resultado["imagem"],
                    experiencia=resultado["experiencia"],
                    link_contato=resultado["link_contato"],
                    profissao=resultado["profissao"],
                    tipo=resultado["tipo"])
            return None
    except Exception as e:
        print(f"Erro ao obter usuário por email: {e}")
        return None

def obter_usuarios_por_profissao(profissao: str) -> list[Usuario]:
    try:
        with obter_conexao() as conexao:      
            cursor = conexao.cursor()
            cursor.execute(BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO, (profissao,))
            resultados = cursor.fetchall()
            return [Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                email=resultado["email"],
                senha_hash=resultado["senha_hash"],
                data_nascimento=resultado["data_nascimento"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                endereco=resultado["endereco"],
                imagem=resultado["imagem"],
                experiencia=resultado["experiencia"],
                link_contato=resultado["link_contato"],
                profissao=resultado["profissao"],
                tipo=resultado["tipo"]
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter usuários por profissão: {e}")
        return []

def obter_usuarios_por_pagina(numero_pagina: int, quantidade: int) -> list[Usuario]:
    try:
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
                senha_hash=resultado["senha_hash"],
                data_nascimento=resultado["data_nascimento"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                endereco=resultado["endereco"],
                imagem=resultado["imagem"],
                experiencia=resultado["experiencia"],
                link_contato=resultado["link_contato"],
                profissao=resultado["profissao"],
                tipo=resultado["tipo"]
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter usuários por página: {e}")
        return []
    
def contar_usuarios_tipo_ab() -> int:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CONTAR_USUARIOS_TIPO_AB)
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar usuários: {e}")
        return 0

def obter_usuarios_por_profissao_nome(nome_profissao: str) -> list[Usuario]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT * FROM usuario 
                WHERE profissao = ? AND tipo IN ('a', 'b')
                ORDER BY nome
            """, (nome_profissao,))
            resultados = cursor.fetchall()
            return [Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                email=resultado["email"],
                senha_hash=resultado["senha_hash"],
                data_nascimento=resultado["data_nascimento"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                endereco=resultado["endereco"],
                imagem=resultado["imagem"],
                experiencia=resultado["experiencia"],
                link_contato=resultado["link_contato"],
                profissao=resultado["profissao"],
                tipo=resultado["tipo"]
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter usuários por profissão: {e}")
        return []