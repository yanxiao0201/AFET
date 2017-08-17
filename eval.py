#!/usr/bin/env python2.7

from __future__ import division
import sys, os, glob, nltk, bisect


'''
Evaluate `EVAL` annotation files against `TRUTH` annotation files.
'''

path = "/Users/xiaoyan/Documents/brat/data/"



TRUTH = path + "ground_truth/*.ann"
EVAL = path + 'AFET_result/*.ann'



DEBUG = True


def main():
    truth_files = glob.glob(TRUTH)
    eval_files = glob.glob(EVAL)
    for truth_file in truth_files:
        for eval_file in eval_files:
            if truth_file.split('/')[-1] == eval_file.split('/')[-1]:
                truth_txt, eval_txt = check_text(truth_file, eval_file)
                eval(truth_file, eval_file, truth_txt, eval_txt)

def check_text(truth_file, eval_file):
    t = truth_file[:-3] + 'txt'
    e = eval_file[:-3] + 'txt'
    s1 = open(t).read()
    s2 = open(e).read()
    s1 = s1.replace('\xe2\x80\x93', '-')
    if not len(s1) == len(s2):
        print 'Attention!'
        print '%s and %s are different' % (t, e)
        print 'len(s1)', len(s1)
        print 'len(s2)', len(s2)
    return s1, s2

def eval(truth_file, eval_file, truth_txt, eval_txt):
    truth_anns = get_annotations(truth_file, truth_txt)
    eval_anns = get_annotations(eval_file, eval_txt)
    correct_anns = list(set(truth_anns) & set(eval_anns))
    print '-'*10, eval_file, 'against', truth_file
    print 'len(truth_anns)', len(truth_anns)
    print 'len(eval_anns)', len(eval_anns)
    print 'len(correct_anns)', len(correct_anns)
    precision = len(correct_anns) / len(eval_anns)
    recall = len(correct_anns) / len(truth_anns)
    if precision == 0 and recall == 0:
        f1 = None
    else:
        f1 = 2 * precision * recall / (precision + recall)
    print 'precision', precision
    print 'recall', recall
    print 'f1', f1
    if DEBUG:
        print correct_anns

def get_annotations(file, text):
    anns = []
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            # print line
            ls = line.split()
            c = ls[0][0]
            if c == 'T':
                # Entity or event.
                handle_entity_event(ls, anns, \
                    tokenize_with_indices(text))
            elif c == 'E':
                # Event.
                handle_event(ls, anns)
            elif c == 'R':
                # Relation.
                handle_relation(ls, anns)
            elif c == '*':
                # Symmetric relation. In ACROBAT, it is "overlap".\
                handle_symmetric_relation(ls, anns)
            elif c == 'A':
                # Attribute.
                handle_attribute(ls, anns)
            elif c == '#':
                # Comment.
                continue
            else:
                raise RuntimeError('Unrecognized line: %s' % line)
    return anns

def handle_entity_event(ls, anns, tup):
    assert(len(ls) >= 5)
    offsets = tup[1]
    l = len(nltk.word_tokenize(' '.join(ls[4:])))
    ls[2] = str(get_token_index(int(ls[2]), offsets))
    ls[3] = str(int(ls[2]) + l)
    assert(int(ls[2]) <= int(ls[3]))
    # if ls[4] == 'bradycardia':
    #     print '@@@', ls
    #     print 'fuck', tup[2]
    #     print 's', s
    #     print 'e', e
    #     exit(1)
    anns.append(' '.join(ls[1:]))

def handle_event(ls, anns):
    assert(len(ls) == 2)
    pass

def handle_relation(ls, anns):
    assert(len(ls) == 4)
    pass

def handle_symmetric_relation(ls, anns):
    assert(len(ls) >= 3)
    assert(ls[1] == 'OVERLAP')
    pass

def handle_attribute(ls, anns):
    assert(len(ls) == 4)
    pass

def get_token_index(char_index, token_start_indices):
    # e.g. 
    # If char_index == 7, token_start_indices == [0, 1, 5, 10],
    # should return 2.
    # If char_index == 5, token_start_indices == [0, 1, 5, 10],
    # should return 2.
    i = bisect.bisect_right(token_start_indices, char_index)
    return i - 1

def tokenize_with_indices(sent):
    tokens = []
    indices = []
    rtn = []
    for token in spans(sent):
        tokens.append(token[0])
        assert(token[1] != -1)
        indices.append(token[1])
        rtn.append((token[0], token[1]))
    return tokens, indices, rtn

def spans(sent):
    # Ref: 
    # https://stackoverflow.com/questions/31668493/get-indices-of-original-text-from-nltk-word-tokenize.
    tokens = nltk.word_tokenize(sent)
    offset = 0
    for token in tokens:
        offset = sent.find(token, offset)
        yield token, offset, offset+len(token)
        offset += len(token)


if __name__ == '__main__':
    sys.exit(main())
