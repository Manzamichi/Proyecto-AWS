# /*
#  * Llamar a una API es una de las tareas más comunes en programación.
#  *
#  * Implementa una llamada HTTP a una API (la que tú quieras) y muestra su
#  * resultado a través de la terminal. Por ejemplo: Pokémon, Marvel...
#  *
#  * Aquí tienes un listado de posibles APIs: 
#  * https://github.com/public-apis/public-apis
#  */

import requests

URL = "https://pokeapi.co/api/v2/pokemon/"

def llamada_api(pokemon):
    try:
        url_pokemon = requests.get(URL + pokemon)
        print(url_pokemon.json())
    except:
        print("pokemon no encontrado")
        raise

llamada_api("charmander")
llamada_api("pikachu")
llamada_api("jaja")