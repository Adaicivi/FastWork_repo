from typing import Optional
from db.data.database import obter_conexao
from db.sql.endereco_sql import *
from db.models.endereco import Endereco

def criar_tabela_enderecos() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de endereços
            cursor.execute(CREATE_TABLE_ENDERECO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de endereços: {e}")
        # Retorna False indicando falha
        return False

def inserir_endereco(endereco: Endereco) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir endereço com cidade e UF
        cursor.execute(INSERT_ENDERECO, (endereco.cidade, endereco.uf))
        # Retorna o ID do endereço inserido
        return cursor.lastrowid

def atualizar_endereco(endereco: Endereco) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do endereço pelo ID
        cursor.execute(UPDATE_ENDERECO, (endereco.cidade, endereco.uf, endereco.id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_endereco(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar endereço pelo ID
        cursor.execute(DELETE_ENDERECO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_endereco_por_id(id: int) -> Optional[Endereco]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar endereço pelo ID
        cursor.execute(GET_ENDERECO_BY_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Endereco com dados do banco
            return Endereco(
                id=resultado["id"],
                cidade=resultado["cidade"],
                uf=resultado["uf"])
    # Retorna None se não encontrou endereço
    return None