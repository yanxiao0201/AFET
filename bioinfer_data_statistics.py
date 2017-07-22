import json

import collections

infile = "BioInfer_visualized_result.json"

type_dic = collections.defaultdict(list)
with open(infile) as f:
	for entry in f:
		a = json.loads(entry)

		type_dic[a["type"]].append(a)



for key in type_dic:
	print key, ":", len(type_dic[key])
	




