from typing import Optional
from util.database import obter_conexao
from db.sql.avaliacao_sql import CRIAR_TABELA_AVALIACAO 
from db.models.avaliacao import Avaliacao
from db.sql.avaliacao_sql import CRIAR_TABELA_AVALIACAO, INSERIR_AVALIACAO, ATUALIZAR_AVALIACAO,    BUSCAR_MEDIA_AVALIACAO_PROFISSIONAL, EXIBIR_AVALIACAO_ORDENADA

def criar_tabela_avaliacao() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_AVALIACAO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de avaliações: {e}")
        return False

def inserir_avaliacao(usuario_id: int, profissional_id: int, nota: float) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERIR_AVALIACAO, (usuario_id, profissional_id, nota))
        return cursor.lastrowid

def atualizar_avaliacao(avaliacao_id: int, usuario_id: int, profissional_id: int, nota: float) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_AVALIACAO, (usuario_id, profissional_id, nota, avaliacao_id))
        return (cursor.rowcount > 0)

def buscar_media_avaliacao_profissional(profissional_id: int) -> Optional[float]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(BUSCAR_MEDIA_AVALIACAO_PROFISSIONAL, (profissional_id,))
        resultado = cursor.fetchone()
        if resultado and resultado['media'] is not None:
            return resultado['media']
    return None

def obter_avaliacoes_ordenadas() -> list[Avaliacao]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXIBIR_AVALIACAO_ORDENADA)
        resultados = cursor.fetchall()
        return [Avaliacao(
            id=resultado["id"],
            usuario_id=resultado["usuario_id"],
            profissional_id=resultado["profissional_id"],
            nota=resultado["nota"],
            data_avaliacao=resultado["data_avaliacao"]
        ) for resultado in resultados]