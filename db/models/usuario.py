from dataclasses import dataclass
from .profissao import Profissao
from .endereco import Endereco
from .imagem import Imagem

@dataclass
class Usuario:
    id: int
    nome : str
    email : str
    senha : str
    foto : Imagem
    exp : str
    cpf : str
    telefone : str
    link_contato : str
    endereco : Endereco
    profissao : Profissao
    tipo : str