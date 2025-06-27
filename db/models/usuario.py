from dataclasses import dataclass
from models.profissao import Profissao
from models.endereco import Endereco

@dataclass
class Usuario:
    id: int
    nome : str
    email : str
    senha : str
    foto : str
    exp : str
    cpf : str
    telefone : str
    link_contato : str
    endereco : Endereco
    profissao : Profissao
    status : str
    avaliacao : float