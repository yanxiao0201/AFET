

class Mention(object):
    """
    Wrap a mention. The entity name of the mention is sentence.tokens[start:end].
    Attributes
    ==========
    start : int
        The start index of the mention.
    end : int
        The end index of the mention.(not included)
    labels : list
        The labels.
    """
    def __init__(self, start, end, entity, labels, c_start, c_end):
        self.start = start
        self.end = end
        self.entity = entity
        self.labels = labels
        self.c_start = c_start
        self.c_end = c_end

    def __str__(self):
        result = 'start: %d, end: %d\n' % (self.start, self.end)
        for label in self.labels:
            result += label + ','
        return result

    def get_entity(self):
        return self.entity

    def get_c_start(self):
        return self.c_start

    def get_c_end(self):
        return self.c_end


class Sentence(object):
    """
    Wrap a sentence.
    Attributes
    ==========
    fileid : string
        The file id.
    senid : string
        The sentence id.
    tokens : list
        The token list of this sentence.
    """
    def __init__(self, fileid, senid, tokens, sent):
        self.fileid = fileid
        self.senid = senid
        self.tokens = tokens
        self.mentions = []
        self.pos = []
        self.dep = []
        self.sent = sent

    def __str__(self):
        result = 'fileid: %s, senid: %s\n'%(self.fileid, self.senid)
        for token in self.tokens:
            result += token + ' '
        result += '\n'
        for m in self.mentions:
            result += m.__str__() + '\n'
        return result

    def add_mention(self, mention):
        assert isinstance(mention, Mention)
        self.mentions.append(mention)

    def size(self):
        return min(len(self.tokens),len(self.pos))

    def get_text(self):
        return '\t'.join([str(self.fileid), str(self.senid), self.sent])

    def get_orig_text(self):
        return self.sent

    def get_tokens(self):
        return self.tokens




