from dataclasses import dataclass
from .profissao import Profissao
from .endereco import Endereco
from .imagem import Imagem
from typing import Optional

@dataclass
class Usuario:
    id: int
    nome : str
    email : str
    senha_hash : str
    data_nascimento : str
    cpf : str
    telefone : str
    endereco : Optional[Endereco] = None
    imagem : Optional[Imagem] = None
    experiencia : Optional[str] = None
    link_contato : Optional[str] = None
    profissao : Optional[Profissao] = None
    tipo : Optional[str] = None