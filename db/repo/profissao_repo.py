from typing import Optional
from util.database import obter_conexao
from db.sql.profissao_sql import *
from db.models.profissao import Profissao

def criar_tabela_profissao() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_PROFISSAO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de profissões: {e}")
        return False

def inserir_profissao(nome: str, descricao: str) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERT_PROFISSAO, (nome, descricao))
        return cursor.lastrowid

def atualizar_profissao(profissao_id: int, nome: str, descricao: str) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_PROFISSAO, (nome, descricao, profissao_id))
        return (cursor.rowcount > 0)

def obter_profissao_por_id(profissao_id: int) -> Optional[Profissao]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(BUSCAR_PROFISSAO_POR_ID, (profissao_id,))
        resultado = cursor.fetchone()
        if resultado:
            return Profissao(
                id=resultado["id"],
                nome=resultado["nome"],
                descricao=resultado["descricao"])
    return None

def obter_profissoes_ordenadas() -> list[Profissao]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXIBIR_PROFISSAO_ORDENADA)
        resultados = cursor.fetchall()
        return [Profissao(
            id=resultado["id"],
            nome=resultado["nome"],
            descricao=resultado["descricao"]
        ) for resultado in resultados]