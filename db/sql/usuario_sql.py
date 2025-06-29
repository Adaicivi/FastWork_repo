CRIAR_TABELA_USUARIO = """
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(100) NOT NULL,
    imagem INTEGER DEFAULT NULL,
    exp VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    telefone VARCHAR(15) NOT NULL,
    link_contato VARCHAR(255) DEFAULT NULL,
    endereco_id INTEGER NOT NULL,
    profissao_id INT NOT NULL,
    tipo VARCHAR(20) NOT NULL DEFAULT 'b',
    FOREIGN KEY (endereco_id) REFERENCES endereco(id),
    FOREIGN KEY (profissao_id) REFERENCES profissao(id),
    FOREIGN KEY (imagem) REFERENCES imagem(id)
);
"""

INSERIR_USUARIO = """
INSERT INTO usuario (nome, email, senha_hash, imagem, exp, cpf, telefone, link_contato, endereco_id, profissao_id, tipo)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_USUARIO = """
UPDATE usuario
SET nome = ?, email = ?, senha_hash = ?, imagem = ?, exp = ?,  cpf = ?, telefone = ?, link_contato = ?, endereco_id = ?, profissao_id = ?, tipo = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_USUARIO = """
UPDATE usuario
SET tipo = ?
WHERE id = ?;
"""

BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO = """
SELECT u.nome, u.email, u.imagem, u.exp, u.cpf, u.telefone, p.nome AS profissao, u.link_contato, u.endereco_id u.tipo
FROM usuario u
JOIN profissao p ON u.profissao_id = p.id
WHERE u.profissao_id = ?;
"""


OBTER_USUARIO_POR_EMAIL_E_SENHA = """
SELECT u.id, u.nome, u.imagem, u.exp, u.cpf, u.telefone, p.nome AS profissao, u.link_contato, u.endereco_id u.tipo
FROM usuario u
JOIN profissao p ON u.profissao_id = p.id
WHERE u.email = ? AND u.senha_hash = ?;
"""

OBTER_USUARIO_POR_ID = """
SELECT u.nome, u.email, u.cpf, u.telefone, u.profissao_id, p.nome AS profissao, p.descricao AS profissao_descricao, u.tipo
FROM usuario u
JOIN profissao p ON u.profissao_id = p.id
WHERE u.id = ?;
"""

OBTER_USUARIO_POR_PAGINA = """
SELECT 
    u.nome, u.imagem, p.nome AS profissao, u.endereco_id,
    AVG(a.nota) AS media_avaliacao
FROM usuario u
JOIN profissao p ON u.profissao_id = p.id
LEFT JOIN avaliacao a ON a.usuario_id = u.id
GROUP BY u.id 
ORDER BY 
    CASE u.tipo 
        WHEN 'a' THEN 0 
        WHEN 'b' THEN 1 
        ELSE 2 
    END,
    media_avaliacao DESC
LIMIT ? OFFSET ?;
"""

DELETAR_USUARIO_POR_ID_SENHA = """
DELETE FROM usuario
WHERE id = ? AND senha_hash = ?;
"""