CRIAR_TABELA_AVALIACAO = """
CREATE TABLE IF NOT EXISTS avaliacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INT NOT NULL,
    profissional_id INT NOT NULL,
    nota FLOAT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (profissional_id) REFERENCES usuario(id)
);
"""

INSERIR_AVALIACAO = """
INSERT INTO avaliacao (usuario_id, profissional_id, nota)
VALUES (?, ?, ?);
"""

ATUALIZAR_AVALIACAO = """
UPDATE avaliacao
SET usuario_id = ?, profissional_id = ?, nota = ?
WHERE id = ?;
"""

BUSCAR_MEDIA_AVALIACAO_PROFISSIONAL = """
SELECT AVG(nota) AS media
FROM avaliacao a
JOIN usuario u ON a.profissional_id = u.id
WHERE a.profissional_id = ?;
"""

EXIBIR_AVALIACAO_ORDENADA = """
SELECT id, usuario_id, profissional_id, nota FROM avaliacao
ORDER BY nota DESC;
"""
