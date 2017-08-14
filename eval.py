#!/usr/bin/env python2.7

from __future__ import division
import sys, os, re, bisect, glob, inspect


'''
Evaluate `EVAL` annotation files against `TRUTH` annotation files.
'''
if len(sys.argv) < 2:
    print "Usage: python eval.py [n|y]"
    print "use \"n\" to run without type correlation and \"y\" to run with type correlation"
    sys.exit(1)
else:
    flag = sys.argv[1]

path = "/Users/xiaoyan/Documents/brat/data/"

TRUTH = path + "ground_truth/1_afet.ann"

if flag == 'n':
    EVAL= path + "mapped_type_no_correlation/1_afet.ann" 

elif flag == 'y':
    EVAL = path + "mapped_type/1_afet.ann"


print EVAL
print TRUTH

DEBUG = False


def main():
    truth_files = glob.glob(TRUTH)
    eval_files = glob.glob(EVAL)
    for truth_file in truth_files:
        for eval_file in eval_files:
            if truth_file.split('/')[-1] == eval_file.split('/')[-1]:
                eval(truth_file, eval_file)

def eval(truth_file, eval_file):
    truth_anns = get_annotations(truth_file)
    eval_anns = get_annotations(eval_file)
    correct_anns = list(set(truth_anns) & set(eval_anns))
    print '-'*10, eval_file, 'against', truth_file
    print 'len(truth_anns)', len(truth_anns)
    print 'len(eval_anns)', len(eval_anns)
    print 'len(correct_anns)', len(correct_anns)
    precision = len(correct_anns) / len(eval_anns)
    recall = len(correct_anns) / len(truth_anns)
    f1 = 2 * precision * recall / (precision + recall)
    print 'precision', precision
    print 'recall', recall
    print 'f1', f1
    if DEBUG:
        print correct_anns

def get_annotations(file):
    anns = []
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            # print line
            ls = line.split()
            c = ls[0][0]
            if c == 'T':
                # Entity or event.
                handle_entity_event(ls, anns)
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

def handle_entity_event(ls, anns):
    assert(len(ls) >= 5)
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


if __name__ == '__main__':
    sys.exit(main())
