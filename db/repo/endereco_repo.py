from db.sql.endereco_sql import *
from db.data.database import obter_conexao
from db.models.endereco import Endereco

def criar_tabela_enderecos() -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(CREATE_TABLE_ENDERECO)
        return (cursor.rowcount > 0)
    
def inserir_endereco(endereco: Endereco) -> Endereco:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERT_ENDERECO, 
            (endereco.cidade, endereco.uf))
        endereco.id = cursor.lastrowid
        return endereco
    
def atualizar_endereco(endereco: Endereco) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(UPDATE_ENDERECO, 
            (endereco.cidade, endereco.uf, endereco.id))
        return (cursor.rowcount > 0)
    
def excluir_endereco(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETE_ENDERECO, (id,))
        return (cursor.rowcount > 0)

def obter_endereco_por_id(id: int) -> Endereco:
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

