from typing import Optional
from db.data.database import obter_conexao
from db.sql.avaliacao_sql import *
from db.models.avaliacao import Avaliacao

def criar_tabela_avaliacao() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de avaliações
            cursor.execute(CRIAR_TABELA_AVALIACAO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de avaliações: {e}")
        # Retorna False indicando falha
        return False

def inserir_avaliacao(usuario_id: int, profissional_id: int, nota: float) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir nova avaliação
        cursor.execute(INSERIR_AVALIACAO, (usuario_id, profissional_id, nota))
        # Retorna o ID da avaliação inserida
        return cursor.lastrowid

def atualizar_avaliacao(avaliacao_id: int, usuario_id: int, profissional_id: int, nota: float) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados da avaliação pelo ID
        cursor.execute(ATUALIZAR_AVALIACAO, (usuario_id, profissional_id, nota, avaliacao_id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def buscar_media_avaliacao_profissional(profissional_id: int) -> Optional[float]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar média de avaliações do profissional
        cursor.execute(BUSCAR_MEDIA_AVALIACAO_PROFISSIONAL, (profissional_id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Retorna a média das avaliações
            return resultado['media']
    # Retorna None se não encontrou resultado
    return None

def obter_avaliacoes_ordenadas() -> list[Avaliacao]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar avaliações ordenadas
        cursor.execute(EXIBIR_AVALIACAO_ORDENADA)
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Avaliacao a partir dos resultados
        return [Avaliacao(
            id=resultado["id"],
            usuario_id=resultado["usuario_id"],
            profissional_id=resultado["profissional_id"],
            nota=resultado["nota"],
            data_avaliacao=resultado["data_avaliacao"]
        ) for resultado in resultados]