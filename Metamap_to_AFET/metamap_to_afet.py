#!/usr/bin/env python

import json
import nltk
import bisect
import glob

'''
Convert MetaMap json output to AFET json input.
Assume the current working directory has `<fileid>.txt.json`s
 that are properly formatted (i.e. can be loaded directly by `json.load`),
 and `Metamap_abbr.txt` exists.
Usage: `./metamap_to_afet.py > x`
Result is saved as "<id_or_range_of_ids>_AFET_input.json".
Errors of MataMap are saved to `x`.
'''

def proc_files():
    # Find all <fileid>.txt.json in the current working directory..
    ids = sorted(int(file.split('.')[0]) for file in glob.glob('*.txt.json'))
    write_file('%s-%s' % (ids[0], ids[-1]), [item for sublist in \
        [proc_file(id, False) for id in ids] for item in sublist])

def proc_file(fileid, write=True):
    # Process a file. Either write to a file or return the result.
    print '-'*50, 'file', fileid, 'processing'
    result = proc_file_helper(fileid)
    remove_label_duplicates(result)
    print '-'*50, 'file', fileid, 'has', len(result), 'sentences'
    if write:
        write_file(fileid, result)
    else:
        return result

def proc_file_helper(fileid):
    # Traverse the output of MetaMap.
    result = []
    weird_matamap_count = 0
    total_char_count = 0
    senid = 0
    abbrs = load_abbrs()
    for u in read_file(fileid):
        sent = u['UttText']

        tokens, indices = tokenize_with_indices(sent)
        senid_cand = int(u['UttNum'])
        assert(senid_cand == senid + 1)
        senid = senid_cand
        mentions = get_mentions_from_utterance(u, total_char_count, tokens, \
            indices, weird_matamap_count, abbrs)
        result.append({"tokens": tokens, "mentions": mentions, \
            "senid": senid, "fileid": str(fileid)})
        total_char_count += len(sent)
    return result

def read_file(fileid):
    with open('%s.txt.json' % fileid) as f:
        data = json.load(f)
    return data['AllDocuments'][0]['Document']['Utterances']

def write_file(fileid, result):
    with open('{}_AFET_input.json'.format(fileid), 'w') as outfile, \
    open('{}_AFET_input_pretty.json'.format(fileid), 'w') as outfile_p:
        for d in result:
            json.dump(d, outfile)
            outfile.write('\n')
            json.dump(d, outfile_p, indent=4, sort_keys=True)
            outfile_p.write('\n')

def get_mentions_from_utterance(u, total_char_count, tokens, indices, \
    weird_matamap_count, abbrs):
    mentions = []
    for p in u['Phrases']:
        phrase = p['PhraseText']
        phrase_end_pos = int(p['PhraseStartPos']) + int(p['PhraseLength']) 
        for m in p['Mappings']:
            for mc in m['MappingCandidates']:
                entity_list = mc['MatchedWords']
                assert(entity_list)
                types = [abbrs[type] for type in mc['SemTypes']]
                mccp = mc['ConceptPIs']
                char_start_pos = int(mccp[0]['StartPos']) - total_char_count
                char_end_pos = int(mccp[-1]['StartPos']) - total_char_count \
                + int(mccp[-1]['Length'])
                #print '@@@', u["UttText"][char_start_pos:char_end_pos]

                assert(char_start_pos >= 0 and char_end_pos >= 0)
                start = get_token_index(char_start_pos, indices)
                end = get_token_index(char_end_pos, indices) + 1
                #print '##', tokens[start:end]
                if tokens[end-1] == ',' or tokens[end-1] == '.' or tokens[end-1] == ')': end -= 1
                #if phrase_end_pos-total_char_count-char_end_pos == 2: end -= 1
                weird_matamap_count = check(weird_matamap_count, entity_list, \
                    tokens, start)
                add_mention(mentions, entity_list, types, start, end)
    return mentions

def load_abbrs():
    abbrs = {}
    with open('Metamap_abbr.txt') as f:
        for line in f:
            line = line.rstrip().split('|')
            abbrs[line[0]] = line[-1].replace(' ', '_').replace(',', '_')
    return abbrs

'''
The reason for the following helper functions:
MetaMap tells the position of the first character of each entity,
but AFET needs the positions of the first and last words of each entity.
Moreover, sometimes MetaMap finds entities
 NOT as they are in the original sentences.
For example,
The original sentence is
 "This is a ten-electrode steerable lasso-shaped cathe-ter that allows 
 irrigated unipolar and bi-polar radiofrequency (RF) ablation (cool 
 flow of 60 ml/min)."
MetaMap finds "radiofrequency ablation"
The correct output is the positions of "radiofrequency" and "ablation".
The potential problem therefore is that AFET assumes continuous word sequences
as entities, e.g. "radiofrequency (RF) ablation", NOT "radiofrequency ablation".
Some weird problems are logged as 'Attention!...'.
'''

def tokenize_with_indices(sent):
    tokens = []
    indices = []
    for token in spans(sent):
        tokens.append(token[0])
        assert(token[1] != -1)
        indices.append(token[1])
    return tokens, indices

def get_token_index(char_index, token_start_indices):
    # e.g. 
    # If char_index == 7, token_start_indices == [0, 1, 5, 10],
    # should return 2.
    # If char_index == 5, token_start_indices == [0, 1, 5, 10],
    # should return 2.
    i = bisect.bisect_right(token_start_indices, char_index)
    return i - 1

def spans(sent):
    # Ref: 
    # https://stackoverflow.com/questions/31668493/get-indices-of-original-text-from-nltk-word-tokenize.
    tokens = nltk.word_tokenize(sent)
    offset = 0
    for token in tokens:
        offset = sent.find(token, offset)
        yield token, offset, offset+len(token)
        offset += len(token)

def add_mention(mentions, entity_list, types, start, end):
    entity = ' '.join(entity_list)
    for m in mentions:
        if m['entity'] == entity:
            m['labels'] += types
            return
    mentions.append({'start': start, 'end': end, \
        'entity': entity, 'labels': types})

def remove_label_duplicates(result):
    for r in result:
        for m in r['mentions']:
            m['labels'] = list(set(m['labels']))

def check(weird_matamap_count, entity_list, tokens, start):
    i = start
    j = 0
    while i < len(tokens) and j < len(entity_list):
        if entity_list[j].lower() in tokens[i].lower():
            j += 1
        else:
            i += 1
    if j < len(entity_list):
        weird_matamap_count += 1
        print 'Attention!'
        print 'j: %s\nentity_list: %s\ntokens: %s\nstart:%s\n' % \
        (j, entity_list, tokens, start)
        if weird_matamap_count == 1000: # tolerate for 1000 times
            exit(1)
    return weird_matamap_count

if __name__ == "__main__":
    # proc_file(0)
    proc_files()
