import hashlib

def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()