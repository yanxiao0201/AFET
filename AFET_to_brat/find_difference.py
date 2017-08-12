import os
import glob
import shutil
import errno


# For looking at the difference:
# http://127.0.0.1:8001/diff.xhtml?diff=/exp_left/#/exp_right/0_afet

file_path = '/Users/xiaoyan/Documents/AFET/UMLS_labels_result/AFET_to_brat/'
folders = ['no_type', 'type_type']

def movefiles():
	for folder in folders:
		txt_files = glob.glob(folder + '/*.txt')
		dir = folder + '_difference/'
		if not os.path.exists(os.path.dirname(dir)):
			try:
				os.makedirs(os.path.dirname(dir))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise

		for file in txt_files:
			tokens = file.split('/')
			filename = tokens[-1]
			shutil.copy2(file, dir + '/' + filename)

men_no_types = glob.glob(folders[0] + '/*.ann')
men_type_types = glob.glob(folders[1] + '/*.ann')


def gen_dif_files():
	for idx in range(len(men_no_types)):
		gen_dif_file(idx)


def gen_dif_file(idx):

	men_no_type = men_no_types[idx]
	men_type_type = men_type_types[idx]

	men_no_name = men_no_type.split('/')[-1]
	men_type_name = men_type_type.split('/')[-1]

	with open(men_no_type) as r_no, open(men_type_type) as r_type,\
	open('no_type_difference/' + men_no_name,'w') as w_no, open('type_type_difference/' + men_type_name, 'w') as w_type:
		cont_no = r_no.readlines()
		cont_type = r_type.readlines()

		set_no = set()
		set_type = set()
		for item in cont_no:
			# 'T1\tDisease_disorder 36 77\thistory of paroxysmal atrial fibrillation\n', 

			entries = item.split('\t')
			new_entry = '\t'.join(entries[1:])
			if new_entry not in set_no:
				set_no.add(new_entry)


		for item in cont_type:
			# 'T1\tDisease_disorder 36 77\thistory of paroxysmal atrial fibrillation\n', 

			entries = item.split('\t')
			new_entry = '\t'.join(entries[1:])
			if new_entry not in set_type:
				set_type.add(new_entry)


		diff_no = set_no - set_type
		cnt = 1
		for i in list(diff_no):
			w_no.write('T{}\t'.format(cnt) + i)
			cnt += 1

		diff_type = set_type - set_no
		cnt = 1
		for i in list(diff_type):
			w_type.write('T{}\t'.format(cnt) + i)
			cnt += 1



if __name__ == "__main__":
	movefiles()
	gen_dif_files()
	# gen_dif_file(0)












