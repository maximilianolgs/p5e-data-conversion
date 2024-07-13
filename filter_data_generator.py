from pathlib import Path
import json
import os

input_location = Path(__file__).parent.parent / "data" / "pokemon"
data_location = Path(__file__).parent.parent / "data"

filter_data = {}
pokemon_index_cap = 809

with open(os.path.join(data_location, "index_order.json"), 'r', encoding='utf-8') as f:
    poke_list = json.load(f)


# go thru the files
for index in range(pokemon_index_cap):
    index += 1
    
    species_list = poke_list[str(index)]
    for raw_poke_name in species_list:
        poke_name = raw_poke_name.replace(' ♀', '-f').replace(' ♂', '-m').replace('é', 'e').replace('\n', ' ').replace(':', '')
        with open(os.path.join(input_location, poke_name + '.json'), 'r', encoding='utf-8') as f:
            poke = json.load(f)
        
        if not 'variant_data' in poke:
            filter_data[raw_poke_name] = {
                                            'index': poke['index'],
                                            'Type': poke['Type'],
                                            'SR': poke['SR'],
                                            'MIN LVL FD': poke['MIN LVL FD']
                                        }
        else:
            for key in poke['variant_data']['variants']:
                variant = poke['variant_data']['variants'][key]
                orig_s = variant['original_species']
                filter_data[orig_s] = {
                                        'index': poke['index'],
                                        'Type': poke['Type'],
                                        'SR': poke['SR'],
                                        'MIN LVL FD': poke['MIN LVL FD']
                                    }
                if 'diff' in variant:
                    filter_data[orig_s]['variant'] = 'true'
                    if 'Type' in variant['diff']:
                        filter_data[orig_s]['Type'] = variant['diff']['Type']
                    if 'SR' in variant['diff']:
                        filter_data[orig_s]['SR'] = variant['diff']['SR']
                    if 'MIN LVL FD' in variant['diff']:
                        filter_data[orig_s]['MIN LVL FD'] = variant['diff']['MIN LVL FD']

with open(os.path.join(data_location, "filter_data.json"), 'w', encoding='utf-8') as f:
    json.dump(filter_data, f, indent=2, ensure_ascii=False)