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
                 usuario.imagem, usuario.link_contato,
                 usuario.endereco.id if usuario.endereco else None,
                 usuario.profissao.id if usuario.profissao else None,
                 usuario.tipo))
            return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        return None

def atualizar_usuario(usuario: Usuario) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
<<<<<<< HEAD
            cursor.execute(ATUALIZAR_USUARIO, (
                usuario.nome,
                usuario.email,
                usuario.senha_hash,
                usuario.cpf,
                usuario.telefone,
                usuario.data_nascimento,
                usuario.experiencia,
                usuario.imagem if isinstance(usuario.imagem, int) else (usuario.imagem.id if usuario.imagem else None),
                usuario.link_contato,
                usuario.endereco.id if usuario.endereco else None,
                usuario.profissao.id if usuario.profissao else None,
                usuario.tipo,
                usuario.id
            ))
=======
            cursor.execute(ATUALIZAR_USUARIO, 
                (usuario.nome, usuario.email, usuario.senha_hash, usuario.cpf,
                 usuario.telefone, usuario.data_nascimento, usuario.experiencia,
                 usuario.imagem.id if hasattr(usuario.imagem, 'id') else usuario.imagem,  # Corrigido
                 usuario.link_contato,
                 usuario.endereco.id if usuario.endereco and hasattr(usuario.endereco, 'id') else None,  # Corrigido
                 usuario.profissao.id if usuario.profissao and hasattr(usuario.profissao, 'id') else None,  # Corrigido
                 usuario.tipo, usuario.id))
>>>>>>> 452ab383a8345ecf8acbb4fda2b27cca8631d297
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
                    endereco=Endereco(
                        id=resultado["endereco_id"],
                        cidade=resultado["endereco_cidade"],
                        uf=resultado["endereco_uf"]
                    ) if resultado["endereco_id"] else None,
                    imagem=resultado["url_imagem"],
                    experiencia=resultado["experiencia"],
                    link_contato=resultado["link_contato"],
                    profissao=Profissao(
                        id=resultado["profissao"],
                        nome=resultado["profissao"],
                        descricao=resultado["profissao_descricao"]
                    ) if resultado["profissao"] else None,
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
                    endereco=Endereco(
                        id=resultado["endereco_id"],
                        cidade=resultado["endereco_cidade"],
                        uf=resultado["endereco_uf"]
                    ) if resultado["endereco_id"] else None,
                    imagem=resultado["url_imagem"],
                    experiencia=resultado["experiencia"],
                    link_contato=resultado["link_contato"],
                    profissao=Profissao(
                        id=resultado["profissao"],
                        nome=resultado["profissao"],
                        descricao=resultado["profissao_descricao"]
                    ) if resultado["profissao"] else None,
                    tipo=resultado["tipo"])
            return None
    except Exception as e:
        print(f"Erro ao obter usuário por email: {e}")
        return None

def obter_usuarios_por_profissao(profissao: int) -> list[Usuario]:
    try:
        with obter_conexao() as conexao:      
            cursor = conexao.cursor()
            cursor.execute(BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO, (profissao,))
            resultados = cursor.fetchall()
            return [Usuario(
                nome=resultado["nome"],
                email=resultado["email"],
                imagem=resultado["url_imagem"], 
                experiencia=resultado["experiencia"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                data_nascimento=resultado["data_nascimento"],
                profissao=Profissao(nome=resultado["profissao"]),
                link_contato=resultado["link_contato"],
                endereco=Endereco(id=resultado["endereco_id"]) if resultado["endereco_id"] else None,
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
                endereco=Endereco(
                    id=resultado["endereco_id"],
                    cidade=resultado["endereco_cidade"],
                    uf=resultado["endereco_uf"]
                ) if resultado["endereco_id"] else None,
                imagem=resultado["url_imagem"],
                experiencia=resultado["experiencia"],
                link_contato=resultado["link_contato"],
                profissao=Profissao(
                    id=resultado["profissao"],
                    nome=resultado["profissao"],
                    descricao=resultado["profissao_descricao"]
                ) if resultado["profissao"] else None,
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
                SELECT u.*, p.nome as profissao, p.descricao as profissao_descricao, i.url as url_imagem, e.cidade as endereco_cidade, e.uf as endereco_uf
                FROM usuario u
                JOIN profissao p ON u.profissao = p.id
                LEFT JOIN imagem i ON u.imagem = i.id
                LEFT JOIN endereco e ON u.endereco = e.id
                WHERE p.nome = ? AND u.tipo IN ('a', 'b')
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
                endereco=Endereco(
                    id=resultado["endereco_id"],
                    cidade=resultado["endereco_cidade"],
                    uf=resultado["endereco_uf"]
                ) if resultado["endereco_id"] else None,
                imagem=resultado["url_imagem"],
                experiencia=resultado["experiencia"],
                link_contato=resultado["link_contato"],
                profissao=Profissao(
                    id=resultado["profissao"],
                    nome=resultado["profissao"],
                    descricao=resultado["profissao_descricao"]
                ) if resultado["profissao"] else None,
                tipo=resultado["tipo"]
            ) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter usuários por profissão: {e}")
        return []