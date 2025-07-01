from typing import Optional
from db.data.database import obter_conexao
from db.sql.imagem_sql import *
from db.models.imagem import Imagem

def criar_tabela_imagens() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de imagens
            cursor.execute(CREATE_TABLE_IMAGEM)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de imagens: {e}")
        # Retorna False indicando falha
        return False

def inserir_imagem(imagem: Imagem) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir imagem com todos os campos
        cursor.execute(INSERT_IMAGEM, 
            (imagem.usuario_id, imagem.nome_arquivo, imagem.nome_arquivo_original, imagem.url))
        # Retorna o ID da imagem inserida
        return cursor.lastrowid

def atualizar_imagem(imagem: Imagem) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados da imagem pelo ID
        cursor.execute(UPDATE_IMAGEM, 
            (imagem.nome_arquivo, imagem.nome_arquivo_original, imagem.url, imagem.id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_imagem(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar imagem pelo ID
        cursor.execute(DELETE_IMAGEM, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_imagem_por_id(id: int) -> Optional[Imagem]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar imagem pelo ID
        cursor.execute(GET_IMAGEM_BY_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Imagem com dados do banco
            return Imagem(
                id=resultado["id"],
                usuario_id=resultado["usuario_id"],
                nome_arquivo=resultado["nome_arquivo"],
                nome_arquivo_original=resultado["nome_arquivo_original"],
                url=resultado["url"],
                criado_em=resultado["criado_em"])
    # Retorna None se não encontrou imagem
    return None