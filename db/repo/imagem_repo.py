from typing import Optional
from util.database import obter_conexao
from db.sql.imagem_sql import *
from db.models.imagem import Imagem

def criar_tabela_imagens() -> bool:
    try:

        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CREATE_TABLE_IMAGEM)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de imagens: {e}")
        return False

def inserir_imagem(imagem: Imagem) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERT_IMAGEM, 
            (imagem.usuario_id, imagem.nome_arquivo, imagem.nome_arquivo_original, imagem.url))
        return cursor.lastrowid

def atualizar_imagem(imagem: Imagem) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(UPDATE_IMAGEM, 
            (imagem.nome_arquivo, imagem.nome_arquivo_original, imagem.url, imagem.id))
        return (cursor.rowcount > 0)

def excluir_imagem(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETE_IMAGEM, (id,))
        return (cursor.rowcount > 0)

def obter_imagem_por_id(id: int) -> Optional[Imagem]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(GET_IMAGEM_BY_ID, (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Imagem(
                id=resultado["id"],
                usuario_id=resultado["usuario_id"],
                nome_arquivo=resultado["nome_arquivo"],
                nome_arquivo_original=resultado["nome_arquivo_original"],
                url=resultado["url"],
                criado_em=resultado["criado_em"])
    return None