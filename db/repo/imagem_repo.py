from typing import Optional
from data.database import obter_conexao
from sql.imagem_sql import *
from models.imagem import Imagem

def criar_tabela_imagens() -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(CREATE_TABLE_IMAGEM)
        return (cursor.rowcount > 0)

def inserir_imagem(imagem: Imagem) -> Imagem:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            INSERT_IMAGEM,
            (imagem.usuario_id, imagem.nome_arquivo, imagem.nome_arquivo_original, imagem.url)
        )
        imagem.id = cursor.lastrowid
        return imagem

def atualizar_imagem(imagem: Imagem) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            UPDATE_IMAGEM,
            (imagem.nome_arquivo, imagem.nome_arquivo_original, imagem.url, imagem.id)
        )
        return cursor.rowcount > 0

def excluir_imagem(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(DELETE_IMAGEM, (id,))
        return cursor.rowcount > 0

def obter_imagem_por_id(id: int) -> Optional[Imagem]:
    with obter_conexao() as conexao:
        conexao.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
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
                criado_em=resultado["criado_em"]
            )
    return None
