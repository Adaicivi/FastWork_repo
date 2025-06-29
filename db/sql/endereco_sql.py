CREATE_TABLE_ENDERECO = """
CREATE TABLE IF NOT EXISTS Endereco (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cidade TEXT NOT NULL,
    uf TEXT NOT NULL
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
