from pathlib import Path
import json
import os

input_location = Path(__file__).parent.parent / "data" / "pokemon"
output_location = Path(__file__).parent.parent / "data"

variant_map = {}

# go thru the files
for file in os.listdir(input_location):
    if file.endswith('.json'):
        poke_name = os.path.splitext(file)[0]
        with open(os.path.join(input_location, file), 'r', encoding='utf-8') as mf:
            poke = json.load(mf)
            
        if 'variant_data' in poke:
            variant_map[poke_name] = []
            for key in poke['variant_data']['variants']:
                if poke_name != poke['variant_data']['variants'][key]['original_species']:
                    variant_map[poke_name].append(poke['variant_data']['variants'][key]['original_species'])

with open(output_location / "variant_map.json", 'w', encoding='utf-8') as f:
    json.dump(variant_map, f, indent=2, ensure_ascii=False)