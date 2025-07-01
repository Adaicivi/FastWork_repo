import re
from pathlib import Path
from fastapi import UploadFile
from PIL import Image
import io
from config.settings import ALLOWED_EXTENSIONS

def validar_cpf(cpf: str) -> bool:
    # Exemplo simples, substitua por validação real se necessário
    cpf = re.sub(r'\D', '', cpf)
    return len(cpf) == 11 and cpf.isdigit()

def validar_imagem(file: UploadFile, contents: bytes) -> bool:
    if not file.filename:
        return False
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
    try:
        Image.open(io.BytesIO(contents))
        return True
    except Exception:
        return False