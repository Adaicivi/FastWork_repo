CREATE_TABLE_ENDERECO = """
CREATE TABLE IF NOT EXISTS Endereco (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cidade TEXT NOT NULL,
    uf TEXT NOT NULL CHECK (LENGTH(uf) = 2)
);
"""

INSERT_ENDERECO = """
INSERT INTO Endereco (cidade, uf)
VALUES (?, ?);
"""

UPDATE_ENDERECO = """
UPDATE Endereco
SET cidade = ?, uf = ?
WHERE id = ?;
"""

DELETE_ENDERECO = """
DELETE FROM Endereco
WHERE id = ?;
"""

GET_ENDERECO_BY_ID = """
SELECT id, cidade, uf
FROM Endereco
WHERE id = ?;
"""

GET_ALL_ENDERECOS = """
SELECT id, cidade, uf
FROM Endereco
ORDER BY cidade;
"""

SEARCH_ENDERECOS_BY_CIDADE = """
SELECT id, cidade, uf
FROM Endereco
WHERE cidade LIKE ?
ORDER BY cidade;
"""

SEARCH_ENDERECOS_BY_UF = """
SELECT id, cidade, uf
FROM Endereco
WHERE uf = ?
ORDER BY cidade;
"""

COUNT_ENDERECOS = """
SELECT COUNT(*) as total
FROM Endereco;
"""

EXISTS_ENDERECO = """
SELECT 1
FROM Endereco
WHERE id = ?
LIMIT 1;
"""
