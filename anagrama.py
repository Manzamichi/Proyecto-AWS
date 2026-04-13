print ("es un anagrama?")
def esAnagrama(palabra1, palabra2):
    palabra1.lower()
    palabra2.lower()
    if palabra1 == palabra2:
        return False
    elif len(palabra1) != len(palabra2):
        return False
    else:
        palabra1Ordenada = sorted(palabra1)
        palabra2Ordenada = sorted(palabra2)
        if palabra1Ordenada == palabra2Ordenada:
            return True
        else:
            return False

print(esAnagrama('hola', 'HOLA'))
print(esAnagrama('calor', 'color'))
print(esAnagrama('amor', 'roma'))
print(esAnagrama('caldito', 'ditolac'))