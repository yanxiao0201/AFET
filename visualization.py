import pandas as pd 

data_set = "BioInfer"
mdic_data = pd.read_csv("Intermediate/{}/mention_text.map".format(data_set), names = ['fmid','mention','start','end','pid','senid','sent'], header = None)

mid_data = pd.read_csv("Intermediate/{}/mention.txt".format(data_set), delimiter = '\t',names = ['fmid','mid'], header = None)

#print mid_data
'''
WSJ1825_2_15_16,corn,15,16,WSJ1825,2,"The harvest arrives in plenty after last year 's drought-ravaged effort : The government estimates corn output at 7.45 billion bushels , up 51 % from last fall ."
'''
t_data = pd.read_csv("Intermediate/{}/type.txt".format(data_set), delimiter = '\t', names = ['type','tid','g'],header = None)

#print t_data

r_data = pd.read_csv("Results/{}/mention_type_pl_warp_bipartite.txt".format(data_set), delimiter = '\t', names = ['mid','tid','g'])

#print r_data

def get_one_row_from_key(df, row_name, key, check=False):
	rows = df.loc[df[row_name] == key]
	if check:
		for _, row in rows.iterrows():
			if row['start'] < 0:
				return None
			return row
	assert(len(rows) == 1)
	for _, row in rows.iterrows():
		return row


result = []
for index, row in r_data.iterrows():
	m = {}
	mid = row['mid']
	tid = row['tid']
	fmid = get_one_row_from_key(mid_data, 'mid', mid)['fmid']
	# print get_one_row_from_key(mid_data, 'mid', mid)
	#print fmid
	#print mdic_data
	mdic_row = get_one_row_from_key(mdic_data, 'fmid', fmid, check=True)
	if mdic_row is None:
		continue
	m['mention'] = mdic_row['mention']
	m['start'] = mdic_row['start']
	m['end'] = mdic_row['end']
	m['pid'] = mdic_row['pid']
	m['senid'] = mdic_row['senid']
	m['sent'] = mdic_row['sent']

	m['type'] = get_one_row_from_key(t_data, 'tid', tid)['type']


	result.append(m)

	
import json
with open('{}_visualized_result.txt'.format(data_set), 'w') as outfile:
    json.dump(result, outfile, indent=4, sort_keys=True)



