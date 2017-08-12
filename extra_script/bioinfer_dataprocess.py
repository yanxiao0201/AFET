import json
import nltk
import collections

class Doc:
	def __init__(self):
		self.labels = []
		self.text = ''

	def add_label(self, label):
		self.labels.extend(label)

	def add_text(self, text):
		self.text = text


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

		tmp_dict = collections.defaultdict(Doc)


		for mention in data["entityMentions"]:


			old_text = mention["text"]
			text = nltk.word_tokenize(old_text.replace("*", " "))

			text_idx_list = get_start_idx_list(new_data["tokens"], text)
			
			if len(text_idx_list) == 0:
				print text_idx_list
				print new_data
				print text
				exit(1)
			else:
				for (start, end) in text_idx_list:
					label = mention["label"]
					if label != "None" or label != "none":
						tmp_dict[(start,end,old_text)].add_label(label.split(','))
						tmp_dict[(start,end,old_text)].add_text(old_text)

		for start,end,old_text in tmp_dict:
			doc = tmp_dict[(start,end,old_text)]
			new_mention = {"start":start, "labels":doc.labels,"end": end}
			if pretty:
				new_mention["text"] = doc.text

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

def get_start_idx_list(x, y):
	rtn = []
	l1 = len(x)
	l2 = len(y)
	i = 0
	while i < l1:
		j = 0
		i_save = None
		first = True
		while i < l1 and j < l2:
			if y[j] in x[i]:
				if first:
					i_save = i
					first = False
				j += 1
			else:
				i += 1
		if j == l2:
			rtn.append((i_save, i+1))
			i += 1
	return rtn


if __name__ == '__main__':
	for mode in ['train', 'test']:
		for pretty in ['','_pretty']:
			print mode, pretty
			main(mode,pretty)


