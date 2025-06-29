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
    senha : str
    data_nascimento : str
    imagem : Optional[Imagem] = None
    exp : Optional[str] = None
    cpf : str
    telefone : str
    link_contato : Optional[str] = None
    endereco : Endereco
    profissao : Optional[Profissao] = None
    tipo : Optional[str] = None