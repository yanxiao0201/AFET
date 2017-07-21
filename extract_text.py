import json

infile = "BBN_visualized_result.json"

fileid = "WSJ1829"


data_list= []
with open(infile) as f:
	for entry in f:
		a = json.loads(entry)
		data_list.append(a)

with open("yyy", 'wa') as outfile:
	order_data = [None for i in range(100)]
	for entry in data_list:
		if entry["pid"] == fileid:
			sentence = entry["sent"]
			senid = int(entry["senid"])
			order_data[senid] = sentence

			json.dump(entry, outfile, indent=4, sort_keys=True)
			outfile.write('\n')



# Result = ""
# for i, data in enumerate(order_data):
# 	if data:
# 		print data

