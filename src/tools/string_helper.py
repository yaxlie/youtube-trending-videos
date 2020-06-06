
def string2int(text):
    import hashlib
    hash_object = hashlib.sha256(text)
    hex_dig = hash_object.hexdigest()
    return hex_dig