from dataclasses import dataclass

@dataclass
class Avaliacao:
    id: int
    usuario_id: int
    profissional_id: int
    nota: float