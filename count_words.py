import collections
import itertools
import glob
import string
import operator

def count_words(item):
   word, occurance = item
   return (word, sum(occurance))

def file_to_words(fl):
    STOP_WORDS = set([
        'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in', 
        'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the', 'to', 'with',
        ])
    
    TR = ''.maketrans(string.punctuation, ' ' * len(string.punctuation))
    words = []
    with open(fl, 'r') as f:
        for line in f:
            if not line:
                continue

            line = line.translate(TR)
            for w in line.split():
                w = w.lower()
                if w not in STOP_WORDS and w.isalpha():
                    words.append((w, 1))

    return words

if __name__ == '__main__':
    files = glob.glob('*.txt')
    a = map(file_to_words, files)
    word_dict = collections.defaultdict(list)
    for k, v in itertools.chain(*a):
        word_dict[k].append(v)

    b = map(count_words, word_dict.items())
    word_list = []
    for k, v in word_dict.items():
        word_list.append((k, sum(v)))
    
    word_list.sort(key=operator.itemgetter(1))
    word_list.reverse()
    print(word_list)
