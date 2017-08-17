import json
import collections
import sets

data_file_path = '/Users/xiaoyan/Documents/AFET/UMLS_type/'
files = ['Metamap_abbr.txt', 'metamap_typing_clean.txt']

UMLS_file_path = '/Users/xiaoyan/Documents/AFET/UMLS_type/'
dic_file = 'MRSTY.RRF'


Data = "Acrobat"
"""
type_mapping: return type_map = {UMLS_type: Acrobat_type}
"""



def type_mapping(files,data_file_path):
	abbr_map = {}
	type_map = {}
	with open(data_file_path + files[1]) as f:
		for line in f:
			data = line.split()
			abbr_map[data[0]] = data[1]


	with open(data_file_path + files[0]) as g:
		for line in g:
			entry = line.split('|')

			if entry[0] in abbr_map:
				entity_type = entry[1]
				type_map[entity_type] = abbr_map[entry[0]]

	return type_map

def reverse_map(type_map):
	rev_typeMap = collections.defaultdict(list)
	for entry in type_map:
		rev_typeMap[type_map[entry]].append(entry)

	print "&&&&&&&&&&&&"
	for key in rev_typeMap:
		print key
	print "&&&&&&"
	return rev_typeMap	

def generate_type_correlation(UMLS_file_path, dic_file, type_map):
	#get UMLS datafile

	UMLS_dic = collections.defaultdict(list)
	with open(UMLS_file_path + dic_file) as f:
		for line in f:
			entries = line.split('|')

			mention = entries[0]
			entity_type = entries[1]

			if entity_type in type_map:
				UMLS_dic[type_map[entity_type]].append(mention)


	with open("type_entities.txt","w") as f:
		for entity_type, mentions in UMLS_dic.iteritems():
			f.write(entity_type + "\t" + ";".join(mentions) + '\n')



if __name__ == "__main__":
	type_map = type_mapping(files,data_file_path)
	generate_type_correlation(UMLS_file_path, dic_file, type_map)
	#reverse_map(type_map)

