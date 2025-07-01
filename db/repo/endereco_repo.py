from typing import Optional
from util.database import obter_conexao
from db.sql.endereco_sql import *
from db.models.endereco import Endereco

def criar_tabela_enderecos() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CREATE_TABLE_ENDERECO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de endereços: {e}")
        return False

def inserir_endereco(endereco: Endereco) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERT_ENDERECO, (endereco.cidade, endereco.uf))
        return cursor.lastrowid

def atualizar_endereco(endereco: Endereco) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(UPDATE_ENDERECO, (endereco.cidade, endereco.uf, endereco.id))
        return (cursor.rowcount > 0)

def excluir_endereco(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETE_ENDERECO, (id,))
        return (cursor.rowcount > 0)

def obter_endereco_por_id(id: int) -> Optional[Endereco]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(GET_ENDERECO_BY_ID, (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Endereco(
                id=resultado["id"],
                cidade=resultado["cidade"],
                uf=resultado["uf"])
    return None