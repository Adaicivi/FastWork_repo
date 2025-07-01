from typing import Optional
from db.data.database import obter_conexao
from db.sql.profissao_sql import *
from db.models.profissao import Profissao

def criar_tabela_profissao() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de profissões
            cursor.execute(CRIAR_TABELA_PROFISSAO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de profissões: {e}")
        # Retorna False indicando falha
        return False

def inserir_profissao(nome: str, descricao: str) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir profissão com nome e descrição
        cursor.execute(INSERT_PROFISSAO, (nome, descricao))
        # Retorna o ID da profissão inserida
        return cursor.lastrowid

def atualizar_profissao(profissao_id: int, nome: str, descricao: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados da profissão pelo ID
        cursor.execute(ATUALIZAR_PROFISSAO, (nome, descricao, profissao_id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_profissao_por_id(profissao_id: int) -> Optional[Profissao]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar profissão pelo ID
        cursor.execute(BUSCAR_PROFISSAO_POR_ID, (profissao_id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Profissao com dados do banco
            return Profissao(
                id=resultado["id"],
                nome=resultado["nome"],
                descricao=resultado["descricao"])
    # Retorna None se não encontrou profissão
    return None

def obter_profissoes_ordenadas() -> list[Profissao]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar profissões ordenadas
        cursor.execute(EXIBIR_PROFISSAO_ORDENADA)
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Profissao a partir dos resultados
        return [Profissao(
            id=resultado["id"],
            nome=resultado["nome"],
            descricao=resultado["descricao"]
        ) for resultado in resultados]