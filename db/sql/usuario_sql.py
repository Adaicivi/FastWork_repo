CRIAR_TABELA_USUARIO = """
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    telefone VARCHAR(15) NOT NULL,
    profissao_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    avaliacao FLOAT DEFAULT 0,
    FOREIGN KEY (profissao_id) REFERENCES profissao(id)
);
"""

INSERIR_USUARIO = """
INSERT INTO usuario (nome, email, senha, cpf, telefone, profissao_id, status)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_USUARIO = """
UPDATE usuario
SET nome = ?, email = ?, senha = ?, cpf = ?, telefone = ?, profissao_id = ?, status = ?
WHERE id = ?;
"""

INSERIR_AVALIACAO_USUARIO = """
INSERT INTO usuario (avaliacao)
VALUES (?);
"""

ATUALIZAR_STATUS_USUARIO = """
UPDATE usuario
SET status = ?
WHERE id = ?;
"""

BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO = """
SELECT u.id, u.nome, u.email, u.cpf, u.telefone, p.nome AS profissao, u.status
FROM usuario u
JOIN profissao p ON u.profissao_id = p.id
WHERE u.profissao_id = ?;
"""

BUSCAR_USUARIOS_ORDENADOS_POR_AVALIACAO = """
SELECT u.id, u.nome, u.email, u.cpf, u.telefone, p.nome AS profissao, u.status
FROM usuario u
JOIN profissao p ON u.profissao_id = p.id
ORDER BY u.avaliacao DESC;
"""

OBTER_USUARIO_POR_EMAIL = """
SELECT u.id, u.nome, u.email, u.senha, u.cpf, u.telefone, u.profissao_id, p.nome AS profissao, p.descricao AS profissao_descricao, u.status, u.avaliacao
FROM usuario u
JOIN profissao p ON u.profissao_id = p.id
WHERE u.email = ?;
"""

OBTER_USUARIO_POR_ID = """
SELECT u.id, u.nome, u.email, u.senha, u.cpf, u.telefone, u.profissao_id, p.nome AS profissao, p.descricao AS profissao_descricao, u.status, u.avaliacao
FROM usuario u
JOIN profissao p ON u.profissao_id = p.id
WHERE u.id = ?;
"""

DELETAR_USUARIO = """DELETE FROM usuario
WHERE id = ?;
"""