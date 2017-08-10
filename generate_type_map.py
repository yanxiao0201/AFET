import json
import collections
import sets

data_file_path = '/Users/xiaoyan/Documents/AFET/Data/Acrobat/'

# extract types from bioinfer training and test files
type_set = set()
for file_type in ['train.json']:
	with open(data_file_path+file_type) as f:
		for entry in f:
			a = json.loads(entry)
			for mention in a["mentions"]:
				for i in mention["labels"]:
					if i.lower() != 'none':
						type_set.add(i)

assert(not 'None' in type_set)

# {"tokens": ["A", "58-year-old", "patient", "with", "a", "3-year", "history", "of", "paroxysmal", "atrial", "fibrillation", "underwent", "circumferential", "pulmonary", "vein", "isolation", "(", "PVI", ")", "in", "2012", "."], "mentions": [{"start": 1, "labels": ["Temporal_Concept"], "end": 2, "entity": "year"}, {"start": 1, "labels": ["Temporal_Concept"], "end": 2, "entity": "old"}, {"start": 2, "labels": ["Clinical_Attribute", "Patient_or_Disabled_Group"], "end": 3, "entity": "patient"}, {"start": 6, "labels": ["Finding"], "end": 11, "entity": "history of atrial fibrillation"}, {"start": 8, "labels": ["Temporal_Concept"], "end": 9, "entity": "paroxysmal"}, {"start": 12, "labels": ["Quantitative_Concept", "Spatial_Concept"], "end": 13, "entity": "circumferential"}, {"start": 13, "labels": ["Body_Part__Organ__or_Organ_Component"], "end": 15, "entity": "pulmonary vein"}, {"start": 15, "labels": ["Functional_Concept", "Therapeutic_or_Preventive_Procedure", "Laboratory_Procedure"], "end": 16, "entity": "isolation"}], "senid": 1, "fileid": "0"}

#get UMLS datafile

UMLS_file_path = '/Users/xiaoyan/Documents/UMLS/2017AA/META/MRSTY.RRF'

UMLS_dic = collections.defaultdict(list)
with open(UMLS_file_path) as f:
	for line in f:
		entries = line.split('|')

		assert(len(entries) == 7)

		mention = entries[0]
		raw_entity_type = entries[3]
		entity_type = raw_entity_type.replace(",", "_").replace(" ", "_")

		if entity_type in type_set:
			UMLS_dic[entity_type].append(mention)

print len(type_set)
print len(UMLS_dic)

diff_set = type_set - set(UMLS_dic.keys())
print diff_set
print len(diff_set)

with open("type_entities.txt","w") as f:
	for entity_type, mentions in UMLS_dic.iteritems():
		f.write(entity_type + "\t" + ";".join(mentions) + '\n')