import hashlib
def generar_hash_sha1(texto):
    hash = hashlib.sha1()
    hash.update(texto.encode('utf-8'))
    return hash.hexdigest()