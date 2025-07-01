from typing import Optional, List
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
    if not endereco:
        raise ValueError("Endereço não pode ser None")
    
    if not endereco.cidade or not endereco.cidade.strip():
        raise ValueError("Cidade é obrigatória")
    
    if not endereco.uf or len(endereco.uf.strip()) != 2:
        raise ValueError("UF deve ter exatamente 2 caracteres")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(INSERT_ENDERECO, (
                endereco.cidade.strip(),
                endereco.uf.strip().upper()
            ))
            return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir endereço: {e}")
        return None

def atualizar_endereco(endereco: Endereco) -> bool:
    if not endereco:
        raise ValueError("Endereço não pode ser None")
    
    if not endereco.id or endereco.id <= 0:
        raise ValueError("ID deve ser um número positivo")
    
    if not endereco.cidade or not endereco.cidade.strip():
        raise ValueError("Cidade é obrigatória")
    
    if not endereco.uf or len(endereco.uf.strip()) != 2:
        raise ValueError("UF deve ter exatamente 2 caracteres")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(UPDATE_ENDERECO, (
                endereco.cidade.strip(),
                endereco.uf.strip().upper(),
                endereco.id
            ))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar endereço: {e}")
        return False

def excluir_endereco(id: int) -> bool:
    if not id or id <= 0:
        raise ValueError("ID deve ser um número positivo")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(DELETE_ENDERECO, (id,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir endereço: {e}")
        return False

def obter_endereco_por_id(id: int) -> Optional[Endereco]:
    if not id or id <= 0:
        raise ValueError("ID deve ser um número positivo")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(GET_ENDERECO_BY_ID, (id,))
            resultado = cursor.fetchone()
            
            if resultado:
                return Endereco(
                    id=resultado["id"],
                    cidade=resultado["cidade"],
                    uf=resultado["uf"]
                )
        return None
    except Exception as e:
        print(f"Erro ao obter endereço: {e}")
        return None

def listar_todos_enderecos() -> List[Endereco]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(GET_ALL_ENDERECOS)
            resultados = cursor.fetchall()
            
            return [
                Endereco(
                    id=resultado["id"],
                    cidade=resultado["cidade"],
                    uf=resultado["uf"]
                )
                for resultado in resultados
            ]
    except Exception as e:
        print(f"Erro ao listar endereços: {e}")
        return []

def buscar_enderecos_por_cidade(cidade: str) -> List[Endereco]:
    if not cidade or not cidade.strip():
        raise ValueError("Cidade deve ser informada")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SEARCH_ENDERECOS_BY_CIDADE, (f"%{cidade.strip()}%",))
            resultados = cursor.fetchall()
            
            return [
                Endereco(
                    id=resultado["id"],
                    cidade=resultado["cidade"],
                    uf=resultado["uf"]
                )
                for resultado in resultados
            ]
    except Exception as e:
        print(f"Erro ao buscar endereços por cidade: {e}")
        return []

def buscar_enderecos_por_uf(uf: str) -> List[Endereco]:
    if not uf or len(uf.strip()) != 2:
        raise ValueError("UF deve ter exatamente 2 caracteres")
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SEARCH_ENDERECOS_BY_UF, (uf.strip().upper(),))
            resultados = cursor.fetchall()
            
            return [
                Endereco(
                    id=resultado["id"],
                    cidade=resultado["cidade"],
                    uf=resultado["uf"]
                )
                for resultado in resultados
            ]
    except Exception as e:
        print(f"Erro ao buscar endereços por UF: {e}")
        return []

def contar_enderecos() -> int:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(COUNT_ENDERECOS)
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar endereços: {e}")
        return 0

def endereco_existe(id: int) -> bool:
    if not id or id <= 0:
        return False
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXISTS_ENDERECO, (id,))
            return cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar existência do endereço: {e}")
        return False