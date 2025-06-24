from dataclasses import dataclass
from models.profissao import Profissao

@dataclass
class Usuario:
    id: int
    nome : str
    email : str
    senha : str
    cpf : str
    telefone : str
    profissao : Profissao
    status : str
    avaliacao : float