from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Imagem:
    id: Optional[int]
    usuario_id: int
    nome_arquivo: str
    nome_arquivo_original: str
    url: str
    criado_em: Optional[datetime] = None