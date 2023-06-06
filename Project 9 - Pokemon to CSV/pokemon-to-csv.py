import requests
import json
import csv


pad = '0'
n = 3


response = requests.get('https://pokeapi.co/api/v2/generation/')
print(response.status_code)
generations = response.json().get('results')

for gen in generations:
    response = requests.get(generations[0]['url'])
    pokemons = response.json().get('pokemon_species')

    for pokemon in pokemons:
        numbers = [int(s) for s in pokemon['url'].split("/") if s.isdigit()]
        pokemon['number'] = str(numbers[-1]).rjust(n, pad)
        del pokemon['url']
        pokemon['name'] = pokemon['name'].capitalize()
        pokemon['sprite'] = f'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/{pokemon["number"]}.png'

    keys = pokemons[0].keys()
    with open(f'{gen["name"]}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(pokemons)
