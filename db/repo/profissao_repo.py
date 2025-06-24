from data.database import obter_conexao
from sql.profissao_sql import CRIAR_TABELA_PROFISSAO, EXIBIR_PROFISSAO_ORDENADA, INSERT_PROFISSAO, BUSCAR_PROFISSAO_POR_ID, ATUALIZAR_PROFISSAO
from models.profissao import Profissao


def criar_tabela_profissao():
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute (CRIAR_TABELA_PROFISSAO,)

def inserir_profissao(nome, descricao) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERT_PROFISSAO, (nome, descricao))
        return cursor.lastrowid

def buscar_profissao_por_id(profissao_id) -> Profissao:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(BUSCAR_PROFISSAO_POR_ID, (profissao_id,))
    return cursor.fetchone()

def atualizar_profissao(profissao_id, nome, descricao):
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_PROFISSAO, (nome, descricao, profissao_id))
    return cursor.rowcount

def exibir_profissao_ordenada() -> list[Profissao]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXIBIR_PROFISSAO_ORDENADA)
        return cursor.fetchall()
