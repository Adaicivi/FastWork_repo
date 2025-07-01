from util.database import obter_conexao
from db.sql.avaliacao_sql import BUSCAR_MEDIA_AVALIACAO_PROFISSIONAL, CRIAR_TABELA_AVALIACAO, EXIBIR_AVALIACAO_ORDENADA, INSERIR_AVALIACAO, ATUALIZAR_AVALIACAO
from db.models.avaliacao import Avaliacao


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

def buscar_media_avaliacao(usuario_id: int) -> float:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(BUSCAR_MEDIA_AVALIACAO_PROFISSIONAL, usuario_id,)
        resultado = cursor.fetchone()
        if resultado:
            return resultado['media']

def exibir_avaliacao_ordenada() -> list[Avaliacao]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXIBIR_AVALIACAO_ORDENADA)
        return cursor.fetchall()