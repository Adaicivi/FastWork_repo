from dataclasses import dataclass
from datetime import datetime
from .imagem import Imagem
from typing import Optional

@dataclass
class Usuario:
    id: int
    nome : str
    email : str
    senha_hash : str
    data_nascimento : datetime
    cpf : str
    telefone : str
    endereco : Optional[str] =None
    imagem : Optional[Imagem] = None
    experiencia : Optional[str] = None
    link_contato : Optional[str] = None
    profissao : Optional[str] = None
    tipo : Optional[str] = None