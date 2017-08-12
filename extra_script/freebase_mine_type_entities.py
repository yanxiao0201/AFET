import json
import collections
import sets

data_file_path = '/home/yba/Documents/CoType/data/source/BioInfer/'

# extract types from bioinfer training and test files
type_set = set()
for file_type in ['train.json', 'test.json']:
	with open(data_file_path+file_type) as f:
		for entry in f:
			a = json.loads(entry)
			for mention in a["entityMentions"]:
				for i in mention["label"].split(','):
					if i.lower() != 'none':
						type_set.add(i) 
assert(not 'None' in type_set)

#get freebase_dic
freebase_file_path = '/media/yba/My Passport/freebase/freebase-mid-type.map'

freebase_dic = collections.defaultdict(list)
with open(freebase_file_path) as f:
	for line in f:

		# <http://rdf.freebase.com/ns/m.01852x2>  <http://rdf.freebase.com/ns/base.type_ontology.abstract>
		entries = line.split()
		assert(len(entries) == 2)

		mention = entries[0]
		entity_type = entries[1].split("/")[-1][:-1]
		if entity_type in type_set:
			freebase_dic[entity_type].append(mention)

print len(type_set)
print len(freebase_dic)

diff_set = type_set - set(freebase_dic.keys())
print diff_set
print len(diff_set)

with open("type_entities.txt","w") as f:
	for entity_type, mentions in freebase_dic.iteritems():
		f.write(entity_type + "\t" + ";".join(mentions) + '\n')







