#This script is used to generate type_entities.txt for the AFET input. Two files need to be in the current directory: MRSTY.RRF, Metamap_abbr.txt. 
#This script is used if the AFET input types is based on UMLS types. To use Acrobat types as the AFET input, run generate_type_map_acrobat.py instead
#To use the script: $ python generate_type_map_UMLS.py

import json
import collections
import sets

dataset = "Acrobat/"
data_file_path = '/Users/xiaoyan/Documents/AFET/Data/' + dataset
files = ["train.json"]

def gen_input_types(data_file_path, files):
	# extract types from training and test files
	type_set = set()
	for file_type in files:
		with open(data_file_path+file_type) as f:
			for entry in f:
				a = json.loads(entry)
				for mention in a["mentions"]:
					for i in mention["labels"]:
						if i.lower() != 'none':
							type_set.add(i)

	assert(not 'None' in type_set)

	return type_set

# {"tokens": ["The", "patient", "was", "discharged", "with", "medical", "treatment", "and", "nocturnal", "BiPAP", "treatment", "."], "mentions": [{"start": 1, "labels": ["Clinical_Attribute", "Patient_or_Disabled_Group"], "end": 2, "entity": "patient"}, {"start": 3, "labels": ["Health_Care_Activity"], "end": 4, "entity": "discharged"}, {"start": 5, "labels": ["Therapeutic_or_Preventive_Procedure"], "end": 7, "entity": "medical treatment"}, {"start": 8, "labels": ["Temporal_Concept"], "end": 9, "entity": "nocturnal"}, {"start": 10, "labels": ["Functional_Concept", "Research_Activity", "Therapeutic_or_Preventive_Procedure", "Conceptual_Entity", "Health_Care_Activity"], "end": 11, "entity": "treatment"}], "senid": 3, "fileid": "1"}

dic_file = "MRSTY.RRF"
abbr_file = "Metamap_abbr.txt"
UMLS_file_path = '/Users/xiaoyan/Documents/AFET/UMLS_type/'


# TypeId -> TypeName. Exp: {T116:Amino_Acid__Peptide__or_Protein}
def gen_type_maps(UMLS_file_path, abbr_file):
	type_map = {}
	with open(UMLS_file_path + abbr_file) as f:
		for line in f:
			entries = line.split('|')
			type_code = entries[1]
			type_name = entries[2].replace(",", "_").replace(" ", "_").strip("\n")

			type_map[type_code] = type_name


	return type_map

#TypeName -> entity ID. Exp: {Amino_Acid__Peptide__or_Protein: C0000005}
def gen_type_entities(UMLS_file_path, type_map, dic_file):
	UMLS_dic = collections.defaultdict(list)
	with open(UMLS_file_path + dic_file) as f:
		for line in f:
			entries = line.split('|')

			mention = entries[0]
			entity_type = entries[1]

			if entity_type in type_map:
				UMLS_dic[type_map[entity_type]].append(mention)

	return UMLS_dic


def write_type_entities(data_file_path, UMLS_dic):

	with open(data_file_path + "type_entities.txt","w") as f:
		for entity_type, mentions in UMLS_dic.iteritems():
			f.write(entity_type + "\t" + ";".join(mentions) + '\n')

	print "Writing successful"


if __name__ == "__main__":
	type_map = gen_type_maps(UMLS_file_path, abbr_file)
	UMLS_dic = gen_type_entities(UMLS_file_path, type_map, dic_file)
	write_type_entities(data_file_path, UMLS_dic)


