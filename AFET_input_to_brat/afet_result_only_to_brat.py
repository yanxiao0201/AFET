#!/usr/bin/env python

import json
import nltk
import os
import errno
from type_map_acrobat import *

'''
Convert AFET visualized json output to brat format.
Assume the current working directory has `Acrobat_mapped_result_.json`

Results are saved to "AFET_to_brat/".
'''
result_files = ['Acrobat_mapped_result.json']

# def proc_file():
#     print '-'*50, 'file', fileid, 'processing'
#     result = proc_file_helper(fileid)
#     remove_label_duplicates(result)
#     print '-'*50, 'file', fileid, 'has', len(result), 'sentences'
#     write_file(fileid, result)

class Mention:
    def __init__(self, start, end, txt, type):
        # Character-and-document level starting and ending positions.
        self.start = start
        self.end = end
        self.txt = txt
        self.type = type

class Doc:
    MAX = 200 # assume max 1000 sentences
    def __init__(self, docid):
        self.docid = docid
        self.sents = [None for i in range(self.MAX)] # one entry for each sent
        self.mentions = []

    def add_sent(self, sent, senid):
        senid = self.real_senid(senid)
        assert(senid >= 0 and senid < self.MAX)
        self.sents[senid] = sent

    def merge_sents(self):
        self.txt = ''.join(filter(None, self.sents))
        # Find the total number of characters at the starting of each sentence.
        self.char_total = [None for i in range(self.MAX)]
        self.char_total[0] = 0
        for i, sent in enumerate(self.sents):
            if sent:
                self.char_total[i+1] = self.char_total[i] + len(sent) + 1

    def add_menton(self, m_txt, type, c_start, c_end, senid, is_train):
        # Convert word-and-sentence starting and ending positions to
        # character-and-document level ones.
        senid = self.real_senid(senid)
        cand = self.sents[senid][c_start:c_end]
        if is_train:
            m_txt = cand
        else:
            print 'm_txt', m_txt
            print 'self.sents[senid]', self.sents[senid]
            print 'c_start', c_start
            print 'cand', cand
            assert(m_txt == cand)
        s_s = c_start
        s_e = c_end
        d_s = s_s + self.char_total[senid]
        d_e = d_s + len(m_txt)
        self.mentions.append(Mention(d_s, d_e, m_txt, type))

    def write_to_brat_format(self, label):
        dir = "AFET_to_brat/"
        if not os.path.exists(os.path.dirname(dir)):
            try:
                os.makedirs(os.path.dirname(dir))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        dir2 = dir + label + '/'
        if not os.path.exists(os.path.dirname(dir2)):
            try:
                os.makedirs(os.path.dirname(dir2))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open('%s/%s_afet.txt' % (dir2, self.docid), 'w') as f_txt, \
        open('%s/%s_afet.ann' % (dir2, self.docid), 'w') as f_ann:
            f_txt.write(self.txt)
            for i, m in enumerate(sorted(self.mentions, key=lambda x: x.start)):
                f_ann.write('\t'.join(['T%s' % (i+1), m.type + ' ' + \
                    str(m.start) + ' ' + str(m.end), m.txt]))
                f_ann.write('\n')

    def real_senid(self, senid):
        return senid - 1 # bc AFET uses 1-based index

def proc_file(files):
    # proc_file_helper(clean_up_mentions(train_format_to_output_format()), \
    #     'before_afet', True)

    # files = ['Acrobat_mapped_result_no_type.json', 'Acrobat_mapped_result_type_type.json']   

    labels = []
    for file in files:
        tokens = file.split('_')
        label = tokens[-2] + '_' + 'type'
        labels.append(label)


    for idx, file in enumerate(files): 
        proc_file_helper(clean_up_mentions(\
            read_file(file)), labels[idx], False)

def proc_file_helper(mentions, label, is_train):
    # If it is the training json, text might not match, because of MetaMap,
    # e.g. "99-year-old" might become "year".
    # If it is the visualized AFET output, text must match the sentence.[0]

    # {u'end': 4, u'start': 3.0, u'pid': 0, u'mention': u'ten-electrode', u'senid': 5, u'type': u'Quantitative', u'sent': u'This is a ten-electrode steerable lasso-shaped cathe-ter that allows irrigated unipolar and bi-polar radiofrequency -LRB- RF -RRB- ablation -LRB- cool flow of 60 ml/min -RRB- .'}


    docs = {}
    for m in mentions:
        docid = int(m['pid'])
        if docid in docs:
            doc = docs[docid]
        else:
            doc = Doc(docid)
            docs[docid] = doc
        senid = int(m['senid'])
        if senid > Doc.MAX:
            print 'senid is %s but max allocated is %s' % (senid, Doc.MAX)
            exit(1)
        doc.add_sent(change_to_bracket(m['sent']), senid)
    for _, doc in docs.iteritems():
        doc.merge_sents()
    for m in mentions:
        if m['type'] in mapped_type: #if it is a valid type:
            doc = docs[int(m['pid'])]
            doc.add_menton(change_to_bracket(m['mention']), m['type'], \
                int(m['c_start']), int(m['c_end']), int(m['senid']), is_train)
    for _, doc in docs.iteritems():
        doc.write_to_brat_format(label)

def change_to_bracket(sentence):
    return sentence.replace("-LRB-", "(").replace("-RRB-", ")")

def train_format_to_output_format():
    mentions = []
    for t in read_file('Data/Acrobat/train.json'):
        for m in t['mentions']:
            for l in m['labels']:
                mentions.append({'mention': m['entity'], 'type': l, \
                    'start': m['start'], 'end': m['end'], \
                    'sent': ' '.join(t['tokens']), 'senid': t['senid'], \
                    'pid': int(t['fileid'])})
    return mentions

def read_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def write_file(fileid, result):
    with open('{}_AFET_input.json'.format(fileid), 'w') as outfile, \
    open('{}_AFET_input_pretty.json'.format(fileid), 'w') as outfile_p:
        for d in result:
            json.dump(d, outfile)
            outfile.write('\n')
            json.dump(d, outfile_p, indent=4, sort_keys=True)
            outfile_p.write('\n')

def clean_up_mentions(mentions):
    rtn = []
    for m in mentions:
        try:
            start = int(m['start'])
        except:
            print 'Attention!'
            print m
            continue
        rtn.append(m)
    return rtn

def tokenize_with_indices(sent, extra_space=False):
    tokens = []
    indices = []
    for token in spans(sent):
        tokens.append(token[0])
        assert(token[1] != -1)
        indices.append(token[1])
        end = token[2]
    if extra_space:
        return tokens + [' '], indices + [end]
    return tokens, indices

def spans(sent):
    # Ref: 
    # https://stackoverflow.com/questions/31668493/get-indices-of-original-text-from-nltk-word-tokenize.
    tokens = nltk.word_tokenize(sent)
    offset = 0
    for token in tokens:
        offset = sent.find(token, offset)
        yield token, offset, offset+len(token)
        offset += len(token)

if __name__ == "__main__":  
    mapped_type = type_mapping(data_file_path,files, result_types)
    proc_file(result_files)
