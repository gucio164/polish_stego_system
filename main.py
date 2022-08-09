# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import nltk
import spacy
import queue
from bitarray import bitarray
import random
from pyinflect import getAllInflections, getInflection
from stempel import StempelStemmer
import wn
import morfeusz2
pl = wn.Wordnet('omw-pl:1.4')

#import plwordnet
#wn = plwordnet.load('plwordnet.xml')

morf = morfeusz2.Morfeusz()


sp = spacy.load('pl_core_news_lg')
stemmer = StempelStemmer.polimorf()


random.seed(9001)

'freq of polish alphabet letters '
alphabet = [(0.1, ' '), (0.088, 'i'), (0.086, 'e'), (0.083, 'a'), (0.075, 'o'), (0.057, 'n'), (0.053, 'z'), (0.0415, 'r'),
            (0.0413, 's'), (0.0411, 'w'),
            (0.0403, 'y'), (0.039, 'c'), (0.0385, 't'), (0.0335, 'd'), (0.03, 'k'), (0.0287, 'p'), (0.0281, 'm'),
            (0.0238, 'ł'), (0.0228, 'j'),
            (0.0224, 'l'), (0.0206, 'u'), (0.0193, 'b'), (0.0146, 'g'), (0.0125, 'h'), (0.0113, 'ę'), (0.0093, 'ż'),
            (0.0079, 'ą'), (0.0078, 'ó'), (0.0072, 'ś'), (0.006, 'ć'), (0.0026, 'f'), (0.0016, 'ń'),
            (0.0008, 'ź')]


'Code responsible for creating Huffman tree'

def read_f(in_file):
    with codecs.open(in_file, 'r', 'utf-8') as f:
        return f.read()


def write_f(in_file, txt):
    with codecs.open(in_file, 'w', 'utf-8') as f:
        f.write(txt)

class HuffmanNode(object):
    def __init__(self, left=None, right=None, root=None):
        self.left = left
        self.right = right
        self.root = root

    def children(self):
        return ((self.left, self.right))


def create_tree(frequencies):
    p = queue.PriorityQueue()
    for value in frequencies:
        p.put(value)
    while p.qsize() > 1:
        try:
            l, r = p.get(), p.get()
            node = HuffmanNode(l, r)
            p.put((l[0] + r[0], node))
        except:
            TypeError
    return p.get()


def walk_tree(node, prefix="", code={}):
    if isinstance(node[1].left[1], HuffmanNode):
        walk_tree(node[1].left, prefix + "0", code)
    else:
        code[node[1].left[1]] = prefix + "0"
    if isinstance(node[1].right[1], HuffmanNode):
        walk_tree(node[1].right, prefix + "1", code)
    else:
        code[node[1].right[1]] = prefix + "1"
    return (code)


def generate_codes_decode(freq):
    node = create_tree(freq)
    code = walk_tree(node)
    dic = {}
    for i in sorted(freq, reverse=True):
        try:
            dic[i[1]] = bitarray(code[i[1]])
        except:
            KeyError
    return dic


def generate_codes(freq):
    node = create_tree(freq)
    code = walk_tree(node)
    dic = {}
    for i in sorted(freq, reverse=True):
        try:
            dic[i[1]] = code[i[1]]
        except:
            KeyError
    return dic


'End of Huffman tree section'


def hd_msg(message, alph):
    res = []
    for a in message:
        a = alph[a]
        res.append(a)
    return res


'Deleting suffix for words in given text'


def remove_suffix(text):
    res = []
    for word in text:
        a = stemmer.stem(word)
        res.append(a)
    return res


'Part of speech tagging'


def pos_tag(text):
    res = []
    sen = sp(text)
    for word in sen:
        a = word.pos_
        res.append(a)
    return res


'Decoding stego messaga bits to text'


def decode(message):
    alp_decode = generate_codes_decode(alphabet)
    temp = ''.join(message)
    msg_decode = bitarray(temp).decode(alp_decode)
    print(''.join(msg_decode))


'Generating list of synonyms for given word and POS'


def list_synonyms(word, pos):
    synonyms = []
    anal = morf.analyse(word.lower())
    word_pos = anal[0][2][2]
    for syn in pl.synsets(word):
        for i in syn.lemmas():
            if word.lower() in i.lower():
                continue
            anal = morf.analyse(i.lower())
            temp = anal[0][2][1]
            if anal[0][2][2] == word_pos: #wersja mocno nastawiona na poprawne substytucje
                synonyms.append(temp)
    print(synonyms)
    print(word)
    return synonyms




'Generating similarity score for given word an its synonyms'


def check_similarity(word, synon):
    dic = {}
    for syn in synon:
        doc_1 = sp(word)
        doc_2 = sp(syn)
        similarity = doc_1.similarity(doc_2)
        dic.update({syn: similarity})
    return dic

'Finding all differeces between two tokenized texts'
def lists_diff(l1, l2):
    dic = []
    for i, j in zip(l1, l2):
        if i == j:
            continue
        else:
            dic.append((i, j))
    return dic


if __name__ == "__main__":

    'coding alphabet and secret message letters'
    alp_code = generate_codes(alphabet)
    secret = "it is a secret message"
    secret_list = list(secret)
    msg = hd_msg(secret_list, alp_code)
    msg = ''.join(msg)
    print(msg)

    'suffix removal and pos tagging'
    tokens = nltk.word_tokenize(secret) #                        tokenizacja
    suff_less_secret = remove_suffix(tokens)
    'opening file, read and tokenize its content'
    orig_text = read_f('overt.txt')
    words = nltk.word_tokenize(orig_text) #                        tokenizacja
    i = 0 #iterator for skipping words
    'enumerate through given words'
    for id, word in enumerate(words):
        word_sp = sp(word) #                        tu nie wiem co
        word_tag = "".join([t.tag_ for t in word_sp])
        anal = morf.analyse(word_sp.text)
        suff_less_word = anal[0][2][1] #stemmer.stem(word)
        word_flection = anal[0][2][2]
        word_pos = pos_tag(word)
        if len(msg) > 0:
            if word_pos[0] == 'NOUN':
                if i == 0 and len(word) > 3:
                    similarity = check_similarity(suff_less_word, list_synonyms(suff_less_word, 'NOUN'))
                    similarity = dict(sorted(similarity.items(), key=lambda x: x[1], reverse=True))
                    similarity = {y: x for x, y in similarity.items()}
                    if len(similarity) < 2:
                        continue
                    else:
                        similarity_code = generate_codes(list(similarity.items())[:3])
                        similarity_code = {y: x for x, y in similarity_code.items()}
                        print(similarity_code)
                        for c in similarity_code:
                            if msg.startswith(c):
                                msg = msg[len(c):]
                                print("Found a word:")
                                print(msg)
                                print(similarity_code.get(c) + '---' + words[id])
                                temp = morf.generate(similarity_code.get(c))
                                for iterator in temp:
                                    if word_flection == iterator[2]:
                                        inf = iterator[0]
                                #inf = getInflection(similarity_code.get(c), tag=word_tag) #                        sposob znajdowania koncowek
                                print('----------------')
                                print(inf)
                                print('----------------')
                                if inf:
                                    words[id] = inf
                                else:
                                    words[id] = similarity_code.get(c)
                                break
                            else:
                                continue

            elif word_pos[0] == 'VERB' and len(word) > 3:
                if i == 0:
                    similarity = check_similarity(suff_less_word, list_synonyms(suff_less_word, 'VERB'))
                    similarity = dict(sorted(similarity.items(), key=lambda x: x[1], reverse=True))
                    similarity = {y: x for x, y in similarity.items()}
                    if len(similarity) < 2:
                        continue
                    else:
                        similarity_code = generate_codes(list(similarity.items())[:3])
                        similarity = sorted(similarity)
                        similarity_code = {y: x for x, y in similarity_code.items()}
                        print(similarity_code)
                        for c in similarity_code:
                            if msg.startswith(c):
                                msg = msg[len(c):]
                                print("Found a word:")
                                print(msg)
                                print(similarity_code.get(c) + '---' + words[id])
                                temp = morf.generate(similarity_code.get(c))
                                for iterator in temp:
                                    if word_flection == iterator[2]:
                                        inf = iterator[0]
                                # inf = getInflection(similarity_code.get(c), tag=word_tag) #                        sposob znajdowania koncowek
                                print('----------------')
                                print(inf)
                                print('----------------')
                                if inf:
                                    words[id] = inf
                                else:
                                    words[id] = similarity_code.get(c)
                                break
                            else:
                                continue
            else:
                continue
        else:
            print("Encoding done..")
            stego = ' '.join(words)
            write_f('result.txt', stego)
            break
        i = (i + 1) % 2


    'Decoding:'
    orig_text = read_f('overt.txt')
    stego_text = read_f('result.txt')
    print("Decoding starting..")
    words = nltk.word_tokenize(orig_text)
    stego_words = nltk.word_tokenize(stego_text)
    #print(words)
    #print(stego_words)
    diff = lists_diff(words, stego_words)
    print(diff)
    res_bin_code = ''
    for word in diff:
        anal = morf.analyse(word[0])
        temp = anal[0][2][1]  # stemmer.stem(word)
        anal = morf.analyse(word[1])
        temp2 = anal[0][2][1]
        word_pos = pos_tag(word[0])
        if word_pos[0] == 'NOUN':
            similarity = check_similarity(temp, list_synonyms(temp, 'NOUN'))
        elif word_pos[0] == 'VERB':
            similarity = check_similarity(temp, list_synonyms(temp, 'VERB'))
        similarity = dict(sorted(similarity.items(), key=lambda x: x[1], reverse=True))
        similarity = {y: x for x, y in similarity.items()}
        similarity_code = generate_codes(list(similarity.items())[:3])
        res_bin_code += similarity_code[temp2]
    print(res_bin_code)
    decode(res_bin_code)
    print("Decoding done..")
