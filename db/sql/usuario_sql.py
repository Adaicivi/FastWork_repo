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
    endereco_id INT,
    profissao_id INT,
    tipo VARCHAR(20) DEFAULT 'c',
    FOREIGN KEY (endereco_id) REFERENCES endereco(id),
    FOREIGN KEY (profissao_id) REFERENCES profissao(id),
    FOREIGN KEY (imagem) REFERENCES imagem(id)
);
"""

INSERIR_USUARIO = """
INSERT INTO usuario (nome, email, senha_hash, cpf, telefone, data_nascimento, experiencia, imagem, link_contato, endereco_id, profissao_id, tipo)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_USUARIO = """
UPDATE usuario
SET nome = ?, email = ?, senha_hash = ?, cpf = ?, telefone = ?, data_nascimento = ?, experiencia = ?, imagem = ?, link_contato = ?, endereco_id = ?, profissao_id = ?, tipo = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_USUARIO = """
UPDATE usuario
SET tipo = ?
WHERE id = ?;
"""

BUSCAR_USUARIOS_ORDENADOS_POR_PROFISSAO = """
SELECT u.nome, u.email, u.imagem, u.experiencia, u.cpf, u.telefone, u.data_nascimento, p.nome AS profissao, u.link_contato, u.endereco_id, u.tipo
FROM usuario u
JOIN profissao p ON u.profissao_id = p.id
WHERE u.profissao_id = ?;
"""

OBTER_USUARIO_POR_EMAIL = """
SELECT u.id, u.nome, u.email, u.senha_hash, u.cpf, u.telefone, u.data_nascimento, u.experiencia, u.imagem, i.url AS url_imagem, u.link_contato, u.endereco_id, e.cidade AS endereco_cidade, e.uf AS endereco_uf, u.profissao_id, p.nome AS profissao, p.descricao AS profissao_descricao, u.tipo
FROM usuario u
LEFT JOIN profissao p ON u.profissao_id = p.id
LEFT JOIN endereco e ON u.endereco_id = e.id
LEFT JOIN imagem i ON u.imagem = i.id
WHERE u.email = ?;
"""

OBTER_USUARIO_POR_ID = """
SELECT u.id, u.nome, u.email, u.senha_hash, u.cpf, u.telefone, u.data_nascimento, u.experiencia, u.imagem, i.url AS url_imagem, u.link_contato, u.endereco_id, e.cidade AS endereco_cidade, e.uf AS endereco_uf, u.profissao_id, p.nome AS profissao, p.descricao AS profissao_descricao, u.tipo
FROM usuario u
LEFT JOIN profissao p ON u.profissao_id = p.id
LEFT JOIN endereco e ON u.endereco_id = e.id
LEFT JOIN imagem i ON u.imagem = i.id
WHERE u.id = ?;
"""

OBTER_USUARIO_POR_PAGINA = """
SELECT u.id, u.nome, u.email, u.senha_hash, u.cpf, u.telefone, u.data_nascimento, u.experiencia, u.imagem, i.url AS url_imagem, u.link_contato, u.endereco_id, e.cidade AS endereco_cidade, e.uf AS endereco_uf, u.profissao_id, p.nome AS profissao, p.descricao AS profissao_descricao, u.tipo, AVG(a.nota) AS media_avaliacao
FROM usuario u
JOIN profissao p ON u.profissao_id = p.id
LEFT JOIN avaliacao a ON a.usuario_id = u.id
LEFT JOIN endereco e ON u.endereco_id = e.id
LEFT JOIN imagem i ON u.imagem = i.id
WHERE u.tipo IN ('a', 'b')
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