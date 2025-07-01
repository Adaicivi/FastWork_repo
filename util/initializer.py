from db.repo import (
    avaliacao_repo,
    imagem_repo,
    usuario_repo,
    profissao_repo,
    endereco_repo
)
from config.settings import UPLOAD_DIR

def criar_tabelas():
    avaliacao_repo.criar_tabela_avaliacao()
    imagem_repo.criar_tabela_imagens()
    usuario_repo.criar_tabela_usuario()
    profissao_repo.criar_tabela_profissao()
    endereco_repo.criar_tabela_enderecos()

def configurar_diretorios():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.joinpath("static").mkdir(parents=True, exist_ok=True)