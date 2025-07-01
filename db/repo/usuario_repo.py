from typing import Optional
from db.data.database import obter_conexao
from db.sql.usuario_sql import *
from db.models.usuario import Usuario
from db.models.endereco import Endereco
from db.models.profissao import Profissao

def criar_tabela_usuarios() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de usuários
            cursor.execute(CRIAR_TABELA_USUARIO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de usuários: {e}")
        # Retorna False indicando falha
        return False

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir usuário com todos os campos
        cursor.execute(INSERIR_USUARIO, 
            (usuario.nome, usuario.email, usuario.senha, usuario.data_nascimento,
             usuario.imagem, usuario.experiencia, usuario.cpf, usuario.telefone,
             usuario.link_contato, 
             usuario.endereco.id if usuario.endereco else None,
             usuario.profissao.id if usuario.profissao else None,
             usuario.tipo))
        # Retorna o ID do usuário inserido
        return cursor.lastrowid

def atualizar_usuario(usuario: Usuario) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do usuário pelo ID
        cursor.execute(ATUALIZAR_USUARIO, 
            (usuario.nome, usuario.email, usuario.senha, usuario.data_nascimento,
             usuario.imagem, usuario.experiencia, usuario.cpf, usuario.telefone,
             usuario.link_contato,
             usuario.endereco.id if usuario.endereco else None,
             usuario.profissao.id if usuario.profissao else None,
             usuario.tipo, usuario.id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def atualizar_tipo_usuario(usuario_id: int, tipo: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar tipo do usuário
        cursor.execute(ATUALIZAR_TIPO_USUARIO, (tipo, usuario_id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_usuario(usuario_id: int, senha_hash: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar usuário pelo ID e senha
        cursor.execute(DELETAR_USUARIO_POR_ID_SENHA, (usuario_id, senha_hash))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_usuario_por_id(usuario_id: int) -> Optional[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo ID
        cursor.execute(OBTER_USUARIO_POR_ID, (usuario_id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Usuario com dados do banco
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                email=resultado["email"],
                senha=resultado["senha_hash"],
                data_nascimento=resultado["data_nascimento"],
                cpf=resultado["cpf"],
                telefone=resultado["telefone"],
                # Cria objeto Endereco se existir dados de endereço
                endereco=Endereco(
                    id=resultado["endereco_id"],
                    cidade=resultado["endereco_cidade"],
                    uf=resultado["endereco_uf"]
                ) if resultado["endereco_id"] else None,
                imagem=resultado["url_imagem"],
                experiencia=resultado["experiencia"],
                link_contato=resultado["link_contato"],
                # Cria objeto Profissao se existir dados de profissão
                profissao=Profissao(
                    id=resultado["profissao_id"],
                    nome=resultado["profissao"],
                    descricao=resultado["profissao_descricao"]
                ) if resultado["profissao_id"] else None,
                tipo=resultado["tipo"])
    # Retorna None se não encontrou usuário
    return None

def obter_usuarios_por_profissao(profissao_id: int) -> list[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários por profissão ordenados
        cursor.execute(BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO, (profissao_id,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Usuario a partir dos resultados
        return [Usuario(
            nome=resultado["nome"],
            email=resultado["email"],
            imagem=resultado["imagem"],
            experiencia=resultado["experiencia"],
            cpf=resultado["cpf"],
            telefone=resultado["telefone"],
            data_nascimento=resultado["data_nascimento"],
            # Cria objeto Profissao com nome da profissão
            profissao=Profissao(nome=resultado["profissao"]),
            link_contato=resultado["link_contato"],
            # Cria objeto Endereco se existir ID de endereço
            endereco=Endereco(id=resultado["endereco_id"]) if resultado["endereco_id"] else None,
            tipo=resultado["tipo"]
        ) for resultado in resultados]

def obter_usuarios_por_pagina(numero_pagina: int, quantidade: int) -> list[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = quantidade
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * limite
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários com paginação
        cursor.execute(OBTER_USUARIO_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Usuario a partir dos resultados
        return [Usuario(
            id=resultado["id"],
            nome=resultado["nome"],
            email=resultado["email"],
            senha=resultado["senha_hash"],
            data_nascimento=resultado["data_nascimento"],
            cpf=resultado["cpf"],
            telefone=resultado["telefone"],
            # Cria objeto Endereco se existir dados de endereço
            endereco=Endereco(
                id=resultado["endereco_id"],
                cidade=resultado["endereco_cidade"],
                uf=resultado["endereco_uf"]
            ) if resultado["endereco_id"] else None,
            imagem=resultado["imagem"],
            experiencia=resultado["experiencia"],
            link_contato=resultado["link_contato"],
            # Cria objeto Profissao se existir dados de profissão
            profissao=Profissao(
                id=resultado["profissao_id"],
                nome=resultado["profissao"],
                descricao=resultado["profissao_descricao"]
            ) if resultado["profissao_id"] else None,
            tipo=resultado["tipo"]
        ) for resultado in resultados]