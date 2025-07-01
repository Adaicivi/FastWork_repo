CREATE_TABLE_PROFISSAO = """
CREATE TABLE IF NOT EXISTS profissao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT NOT NULL
);
"""

INSERT_PROFISSAO = """
INSERT INTO profissao (nome, descricao)
VALUES (?, ?);
"""

UPDATE_PROFISSAO = """
UPDATE profissao
SET nome = ?, descricao = ?
WHERE id = ?;
"""

DELETE_PROFISSAO = """
DELETE FROM profissao
WHERE id = ?;
"""

GET_PROFISSAO_BY_ID = """
SELECT id, nome, descricao 
FROM profissao
WHERE id = ?;
"""

GET_ALL_PROFISSOES = """
SELECT id, nome, descricao 
FROM profissao
ORDER BY nome;
"""

SEARCH_PROFISSOES_BY_NOME = """
SELECT id, nome, descricao 
FROM profissao
WHERE nome LIKE ?
ORDER BY nome;
"""

SEARCH_PROFISSOES_BY_DESCRICAO = """
SELECT id, nome, descricao 
FROM profissao
WHERE descricao LIKE ?
ORDER BY nome;
"""

COUNT_PROFISSOES = """
SELECT COUNT(*) as total
FROM profissao;
"""

EXISTS_PROFISSAO = """
SELECT 1
FROM profissao
WHERE id = ?
LIMIT 1;
"""

EXISTS_PROFISSAO_BY_NOME = """
SELECT 1
FROM profissao
WHERE nome = ?
LIMIT 1;
"""