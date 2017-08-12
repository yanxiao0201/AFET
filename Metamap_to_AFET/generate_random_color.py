import random

'''
Load `Metamap_abbr.txt` and assign a color to each type.
For brat visualization.
'''

def main():
    types = load_abbrs().values()
    r = lambda: random.randint(100,255)
    for type in types:
        print '%s   bgColor:%s' % (type, '#%02X%02X%02X' % (r(),r(),r()))

def load_abbrs():
    abbrs = {}
    with open('Metamap_abbr.txt') as f:
        for line in f:
            line = line.rstrip().split('|')
            abbrs[line[0]] = line[-1].replace(' ', '_').replace(',', '_')
    return abbrs

if __name__ == '__main__':
    main()
