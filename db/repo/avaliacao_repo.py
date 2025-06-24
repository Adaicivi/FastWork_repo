from data.database import obter_conexao
from sql.avaliacao_sql import CRIAR_TABELA_AVALIACAO, EXIBIR_AVALIACAO_ORDENADA, INSERIR_AVALIACAO, ATUALIZAR_AVALIACAO, BUSCAR_MEDIA_AVALIACAO
from models.avaliacao import Avaliacao


def criar_tabela_avaliacao():
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(CRIAR_TABELA_AVALIACAO,)

def inserir_avaliacao(usuario_id, profissional_id, nota) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERIR_AVALIACAO, (usuario_id, profissional_id, nota,))
        return cursor.lastrowid

def atualizar_avaliacao(avaliacao_id, usuario_id, profissional_id, nota) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_AVALIACAO, (usuario_id, profissional_id, nota, avaliacao_id))
    return cursor.rowcount > 0

def buscar_media_avaliacao() -> float:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(BUSCAR_MEDIA_AVALIACAO)
        resultado = cursor.fetchone()
    return resultado[0] if resultado else 0.0

def exibir_avaliacao_ordenada() -> list[Avaliacao]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXIBIR_AVALIACAO_ORDENADA)
        return cursor.fetchall()