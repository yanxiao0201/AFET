#Need 3 files in the current directory: 'Metamap_abbr.txt', 'metamap_typing_clean.txt', 'Acrobat_visualized_result.json'

import json
import collections
import sets

data_file_path = '/Users/xiaoyan/Documents/AFET/AFET_to_brat/'

files = ['Metamap_abbr.txt', 'metamap_typing_clean.txt']

abbr_map = {}
type_map = {}
# result_types = ['_no_type', '_type_type'] This is for comparing with or without type_entities.txt
result_types = ['']

def type_mapping(data_file_path,files, result_types):
	with open(data_file_path + files[1]) as f:
		for line in f:
			data = line.split()
			abbr_map[data[0]] = data[1]


	with open(data_file_path + files[0]) as g:
		for line in g:
			entry = line.split('|')

			if entry[0] in abbr_map:
				entity_type = entry[-1].replace(",", "_").replace(" ", "_").strip('\n')
				type_map[entity_type] = abbr_map[entry[0]]


	for result_type in result_types:
		with open(data_file_path + 'Acrobat_visualized_result' + result_type + '.json') as f, open(data_file_path + 'Acrobat_mapped_result' + result_type + '.json', 'w') as g:
			for entry in f:
				a = json.loads(entry)
				if a["type"] in type_map:
					a['type'] = type_map[a['type']]
				json.dump(a, g)
				g.write('\n')

	return set(type_map.values())


if __name__ == "__main__":
	type_mapping(data_file_path,files, result_types)	









