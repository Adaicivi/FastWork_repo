CRIAR_TABELA_USUARIO = """
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    telefone VARCHAR(15) NOT NULL,
    data_nascimento DATE NOT NULL,
    experiencia VARCHAR(255),
    imagem INTEGER DEFAULT NULL,
    link_contato VARCHAR(255) DEFAULT NULL,
    endereco VARCHAR(255) DEFAULT NULL,
    profissao VARCHAR(255) DEFAULT NULL,
    tipo VARCHAR(20) DEFAULT 'c',
    FOREIGN KEY (imagem) REFERENCES imagem(id)
);
"""



INSERIR_USUARIO = """
INSERT INTO usuario (nome, email, senha_hash, cpf, telefone, data_nascimento, experiencia, imagem, link_contato, endereco, profissao, tipo)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_USUARIO = """
UPDATE usuario
SET nome = ?, email = ?, senha_hash = ?, cpf = ?, telefone = ?, data_nascimento = ?, experiencia = ?, imagem = ?, link_contato = ?, endereco = ?, profissao = ?, tipo = ?
WHERE id = ?;
"""

ATUALIZAR_SENHA_USUARIO = """
UPDATE usuario
SET senha_hash = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_USUARIO = """
UPDATE usuario
SET tipo = ?
WHERE id = ?;
"""

BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO = """
SELECT u.nome, u.email, u.imagem, i.url AS url_imagem, u.experiencia, u.cpf, u.telefone, u.data_nascimento, u.profissao, u.link_contato, u.endereco, u.tipo
FROM usuario u
WHERE u.profissao = ?;
"""
OBTER_USUARIO_POR_EMAIL = """
SELECT u.id, u.nome, u.email, u.senha_hash, u.cpf, u.telefone, u.data_nascimento, u.experiencia, u.imagem, i.url AS url_imagem, u.link_contato, u.endereco, u.profissao, u.tipo
FROM usuario u
LEFT JOIN imagem i ON u.imagem = i.id
WHERE u.email = ?;
"""

OBTER_USUARIO_POR_ID = """
SELECT u.id, u.nome, u.email, u.senha_hash, u.cpf, u.telefone, u.data_nascimento, u.experiencia, u.imagem, i.url AS url_imagem, u.link_contato, u.endereco, u.profissao, u.tipo
FROM usuario u
LEFT JOIN imagem i ON u.imagem = i.id
WHERE u.id = ?;
"""

OBTER_USUARIO_POR_PAGINA = """
SELECT u.id, u.nome, u.email, u.senha_hash, u.cpf, u.telefone, u.data_nascimento, u.experiencia, u.imagem, i.url AS url_imagem, u.link_contato, u.endereco, u.profissao, u.tipo, AVG(a.nota) AS media_avaliacao
FROM usuario u
LEFT JOIN avaliacao a ON a.profissional_id = u.id
LEFT JOIN imagem i ON u.imagem = i.id
WHERE u.tipo IN ('a', 'b')
GROUP BY u.id, u.nome, u.email, u.senha_hash, u.cpf, u.telefone, u.data_nascimento, u.experiencia, u.imagem, i.url, u.link_contato, u.endereco, u.profissao, u.tipo
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

CONTAR_USUARIOS_TIPO_AB = """
SELECT COUNT(*) AS total
FROM usuario
WHERE tipo IN ('a', 'b');
"""

