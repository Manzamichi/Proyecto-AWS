 #Escribe un programa que reciba un texto y transforme lenguaje natural a
  #"lenguaje hacker" (conocido realmente como "leet" o "1337"). Este lenguaje
   #se caracteriza por sustituir caracteres alfanuméricos.
  #- Utiliza esta tabla (https://www.gamehouse.com/blog/leet-speak-cheat-sheet/) 
   #con el alfabeto y los números en "leet".
    #(Usa la primera opción de cada transformación. Por ejemplo "4" para la "a")
def convertirLeet(palabra):
    palabraMayuscula = palabra.upper()
    arrayPalabra = list(palabraMayuscula)
    for i in range(len(arrayPalabra)):
        if arrayPalabra[i] == 'A':
            arrayPalabra[i] = '4'
        elif arrayPalabra[i] == 'B':
            arrayPalabra[i] = 'l3'
        elif arrayPalabra[i] == 'C':
            arrayPalabra[i] = '['
        elif arrayPalabra[i] == 'D':
            arrayPalabra[i] = ')'
        elif arrayPalabra[i] == 'E':
            arrayPalabra[i] = '3'
        elif arrayPalabra[i] == 'F':
            arrayPalabra[i] = '|='
        elif arrayPalabra[i] == 'G':
            arrayPalabra[i] = '&'
        elif arrayPalabra[i] == 'H':
            arrayPalabra[i] = '#'
        elif arrayPalabra[i] == 'I':
            arrayPalabra[i] = '1'
        elif arrayPalabra[i] == 'J':
            arrayPalabra[i] = ',_|'
        elif arrayPalabra[i] == 'K':
            arrayPalabra[i] = ">|"
        elif arrayPalabra[i] == 'L':
            arrayPalabra[i] = '1'
        elif arrayPalabra[i] == 'M':
            arrayPalabra[i] = 'JVI'
        elif arrayPalabra[i] == "N":
            arrayPalabra[i] = '^/'
        elif arrayPalabra[i] == 'O':
            arrayPalabra[i] = '0'
        elif arrayPalabra[i] == 'P':
            arrayPalabra[i] = '|*'
        elif arrayPalabra[i] == 'Q':
            arrayPalabra[i] = '(_,)'
        elif arrayPalabra[i] == 'R':
            arrayPalabra[i] = 'I2'
        elif arrayPalabra[i] == 'S':
            arrayPalabra[i] = '5'
        elif arrayPalabra[i] == 'T':
            arrayPalabra[i] = '7'
        elif arrayPalabra[i] == 'U':
            arrayPalabra[i] = '(_)'
        elif arrayPalabra[i] == 'V':
            arrayPalabra[i] = '\/'
        elif arrayPalabra[i] == 'W':
            arrayPalabra[i] = '\/\/'
        elif arrayPalabra[i] == 'X':
            arrayPalabra[i] = '><'
        elif arrayPalabra[i] == 'Y':
            arrayPalabra[i] = 'j'
        elif arrayPalabra[i] == 'Z':
            arrayPalabra[i] = '2'

    palabraLeet =''.join(map(str, arrayPalabra))
    return palabraLeet

print(convertirLeet('abc'))
print(convertirLeet('Parangaricutirimicuaro'))
print(convertirLeet('manzanero'))