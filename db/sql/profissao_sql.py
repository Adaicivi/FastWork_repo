CRIAR_TABELA_PROFISSAO = """
CREATE TABLE IF NOT EXISTS profissao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL
);
"""

INSERT_PROFISSAO = """
INSERT INTO profissao (nome, descricao)
VALUES (?, ?);
"""

ATUALIZAR_PROFISSAO = """
UPDATE profissao
SET nome = ?, descricao = ?
WHERE id = ?;
"""

BUSCAR_PROFISSAO_POR_ID = """
SELECT nome, descricao FROM profissao
WHERE id = ?;
"""

EXIBIR_PROFISSAO_ORDENADA = """
SELECT id, nome, descricao FROM profissao
ORDER BY nome;
"""
