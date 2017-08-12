import json

infile = "Data/BBN/test.json"

fileid = "WSJ1829"


data_list= []
with open(infile) as f:
	for entry in f:
		a = json.loads(entry)
		data_list.append(a)

with open("zzz", 'wa') as outfile:

	for entry in data_list:
		if entry["fileid"] == fileid:
			tokens = entry["tokens"]
			senid = int(entry["senid"])

			mentions = entry["mentions"]

			for mention in mentions:
				start = int(mention["start"])
				end = int(mention["end"])
				words = tokens[start:end]

				mention["text"] = " ".join(words)

			del entry["tokens"]
			
			json.dump(entry, outfile, indent=4, sort_keys=True)
			outfile.write('\n')