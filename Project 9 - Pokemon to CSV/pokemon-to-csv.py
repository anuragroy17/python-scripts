import requests
import json
import csv


pad = '0'
n = 3

response = requests.get('https://pokeapi.co/api/v2/generation/')
print(response.status_code)
generations = response.json().get('results')

for gen in generations:
    response = requests.get(gen['url'])
    pokemons = response.json().get('pokemon_species')

    for pokemon in pokemons:
        pokemon['Name'] = pokemon['name'].capitalize()
        del pokemon['name']

        response = requests.get(pokemon['url'])
        evolution = response.json().get('evolves_from_species')
        if evolution != None:
            pokemon['Evolves From'] = evolution['name'].capitalize()
        else:
            pokemon['Evolves From'] = ''

        numbers = [int(s) for s in pokemon['url'].split("/") if s.isdigit()]
        pokemon['Number'] = str(numbers[-1]).rjust(n, pad)
        pokemon['Sprite'] = f'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/{pokemon["Number"]}.png'
        del pokemon['url']

    sortedPokemons = sorted(pokemons, key=lambda d: d['Number'])

    keys = sortedPokemons[0].keys()
    with open(f'{gen["name"]}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(sortedPokemons)
