CREATE_TABLE_IMAGEM = """
CREATE TABLE IF NOT EXISTS imagem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    nome_arquivo TEXT NOT NULL,
    nome_arquivo_original TEXT,
    url TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);
"""

INSERT_IMAGEM = """
INSERT INTO imagem (usuario_id, nome_arquivo, nome_arquivo_original, url)
VALUES (?, ?, ?, ?)
"""

UPDATE_IMAGEM = """
UPDATE imagem
SET nome_arquivo = ?, nome_arquivo_original = ?, url = ?
WHERE id = ?
"""

DELETE_IMAGEM = """
DELETE FROM imagem
WHERE id = ?
"""

GET_IMAGEM_BY_ID = """
SELECT id, usuario_id, nome_arquivo, nome_arquivo_original, url, criado_em
FROM imagem
WHERE id = ?
"""

