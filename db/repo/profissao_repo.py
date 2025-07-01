from typing import Optional, List
from util.database import obter_conexao
from db.sql.profissao_sql import *
from db.models.profissao import Profissao

def criar_tabela_profissao() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CREATE_TABLE_PROFISSAO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de profissões: {e}")
        return False

def inserir_profissao(profissao: Profissao) -> Optional[int]:
    if not profissao:
        raise ValueError("Profissão não pode ser None")
    
    if not profissao.nome or not profissao.nome.strip():
        raise ValueError("Nome da profissão é obrigatório")
    
    if not profissao.descricao or not profissao.descricao.strip():
        raise ValueError("Descrição da profissão é obrigatória")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(INSERT_PROFISSAO, (
                profissao.nome.strip(),
                profissao.descricao.strip()
            ))
            return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir profissão: {e}")
        return None

def inserir_profissao_simples(nome: str, descricao: str) -> Optional[int]:
    if not nome or not nome.strip():
        raise ValueError("Nome da profissão é obrigatório")
    
    if not descricao or not descricao.strip():
        raise ValueError("Descrição da profissão é obrigatória")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(INSERT_PROFISSAO, (nome.strip(), descricao.strip()))
            return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir profissão: {e}")
        return None

def atualizar_profissao(profissao: Profissao) -> bool:
    if not profissao:
        raise ValueError("Profissão não pode ser None")
    
    if not profissao.id or profissao.id <= 0:
        raise ValueError("ID deve ser um número positivo")
    
    if not profissao.nome or not profissao.nome.strip():
        raise ValueError("Nome da profissão é obrigatório")
    
    if not profissao.descricao or not profissao.descricao.strip():
        raise ValueError("Descrição da profissão é obrigatória")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(UPDATE_PROFISSAO, (
                profissao.nome.strip(),
                profissao.descricao.strip(),
                profissao.id
            ))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar profissão: {e}")
        return False

def atualizar_profissao_simples(profissao_id: int, nome: str, descricao: str) -> bool:
    if not profissao_id or profissao_id <= 0:
        raise ValueError("ID deve ser um número positivo")
    
    if not nome or not nome.strip():
        raise ValueError("Nome da profissão é obrigatório")
    
    if not descricao or not descricao.strip():
        raise ValueError("Descrição da profissão é obrigatória")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(UPDATE_PROFISSAO, (nome.strip(), descricao.strip(), profissao_id))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar profissão: {e}")
        return False

def excluir_profissao(id: int) -> bool:
    if not id or id <= 0:
        raise ValueError("ID deve ser um número positivo")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(DELETE_PROFISSAO, (id,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir profissão: {e}")
        return False

def obter_profissao_por_id(profissao_id: int) -> Optional[Profissao]:
    if not profissao_id or profissao_id <= 0:
        raise ValueError("ID deve ser um número positivo")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(GET_PROFISSAO_BY_ID, (profissao_id,))
            resultado = cursor.fetchone()
            
            if resultado:
                return Profissao(
                    id=resultado["id"],
                    nome=resultado["nome"],
                    descricao=resultado["descricao"]
                )
        return None
    except Exception as e:
        print(f"Erro ao obter profissão: {e}")
        return None

def listar_todas_profissoes() -> List[Profissao]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(GET_ALL_PROFISSOES)
            resultados = cursor.fetchall()
            
            return [
                Profissao(
                    id=resultado["id"],
                    nome=resultado["nome"],
                    descricao=resultado["descricao"]
                )
                for resultado in resultados
            ]
    except Exception as e:
        print(f"Erro ao listar profissões: {e}")
        return []

def obter_profissoes_ordenadas() -> List[Profissao]:
    return listar_todas_profissoes()

def buscar_profissoes_por_nome(nome: str) -> List[Profissao]:
    if not nome or not nome.strip():
        raise ValueError("Nome deve ser informado")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SEARCH_PROFISSOES_BY_NOME, (f"%{nome.strip()}%",))
            resultados = cursor.fetchall()
            
            return [
                Profissao(
                    id=resultado["id"],
                    nome=resultado["nome"],
                    descricao=resultado["descricao"]
                )
                for resultado in resultados
            ]
    except Exception as e:
        print(f"Erro ao buscar profissões por nome: {e}")
        return []

def buscar_profissoes_por_descricao(descricao: str) -> List[Profissao]:
    if not descricao or not descricao.strip():
        raise ValueError("Descrição deve ser informada")
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SEARCH_PROFISSOES_BY_DESCRICAO, (f"%{descricao.strip()}%",))
            resultados = cursor.fetchall()
            
            return [
                Profissao(
                    id=resultado["id"],
                    nome=resultado["nome"],
                    descricao=resultado["descricao"]
                )
                for resultado in resultados
            ]
    except Exception as e:
        print(f"Erro ao buscar profissões por descrição: {e}")
        return []

def contar_profissoes() -> int:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(COUNT_PROFISSOES)
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar profissões: {e}")
        return 0

def profissao_existe(id: int) -> bool:
    if not id or id <= 0:
        return False
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXISTS_PROFISSAO, (id,))
            return cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar existência da profissão: {e}")
        return False

def profissao_existe_por_nome(nome: str) -> bool:
    if not nome or not nome.strip():
        return False
    
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXISTS_PROFISSAO_BY_NOME, (nome.strip(),))
            return cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar existência da profissão por nome: {e}")
        return False