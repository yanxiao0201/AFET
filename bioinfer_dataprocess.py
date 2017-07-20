import json
import nltk
import collections



def main(mode, pretty):
	infile = "Data/BioInfer_old/%s.json" % mode


	data_list= []
	with open(infile) as f:
		for entry in f:
			a = json.loads(entry)
			data_list.append(a)


	data_new_list = []
	i = 0
	for data in data_list:
		new_data = {}
		new_data["fileid"] = data["articleId"]
		new_data["tokens"] = nltk.word_tokenize(data["sentText"].replace("*", " "))
		new_data["senid"] = int(data["sentId"])
		new_data["mentions"] = []

		tmp_dict = collections.defaultdict(list)


		for mention in data["entityMentions"]:


			text = mention["text"]
			text = nltk.word_tokenize(text.replace("*", " "))

			text_idx_list = getsubidx(new_data["tokens"], text)
			
			if len(text_idx_list) == 0:
				print text_idx_list
				print new_data
				print text
				exit(1)
			else:
				for start in text_idx_list:
					end = start + len(text)
					label = mention["label"]
					if label != "None" or label != "none":
						tmp_dict[(start,end)].extend(label.split(','))

		for start,end in tmp_dict:
			new_mention = {"start":start, "labels":tmp_dict[(start,end)],"end": end}

			new_data["mentions"].append(new_mention)

		data_new_list.append(new_data)

	print len(data_new_list)

	with open("Data/BioInfer/%s%s.json" % (mode, pretty), 'wa') as outfile:
		for d in data_new_list:
			if pretty:
				json.dump(d, outfile, indent=4, sort_keys=True)
			else:
				json.dump(d, outfile)
			outfile.write('\n')

def getsubidx(x, y):
	res = []
	l1, l2 = len(x), len(y)


	i = 0
	j = 0

	while i < l1 and j < l2:
		if y[j] in x[i]:
			j += 1
		else:
			i += 1

		if j == l2:
				

	if 	
	
	# for i in range(l1):
	# 	is_sub = True
	# 	for j in range(l2):
	# 		if i+j < l2:
	# 			if y[j] in x[i+j]:
	# 				continue
	# 			elif i+j > 0:
	# 				if y[j] in x[i+j-1]:
	# 					continue
	# 				else:
	# 		else:
	# 			is_sub = False
	# 			break
	# 	if is_sub:
	# 		res.append(i)
	return res


if __name__ == '__main__':
	for mode in ['train', 'test']:
		for pretty in ['','_pretty']:
			print mode, pretty
			main(mode,pretty)


