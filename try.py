import nltk
from nltk.tokenize.moses import MosesDetokenizer, MosesTokenizer

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

    print untokenize(tokens)


    offset = 0
    for token in tokens:
        offset = sent.find(token, offset)
        yield token, offset, offset+len(token)
        offset += len(token)


import re
def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
         "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()


print tokenize_with_indices('I read (67%) and  ( 20% ) and, .R$^HD &*!U ZJK, JKNA X6bxhj token.')
