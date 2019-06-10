import os
import json
import requests
import sys
import time

TRIALS = 10
SLEEPTIME = 1

#properties = {"annotators": -list of comma separated annotators-, "outputFormat": "json"}
def call_core(input, annotators):
    print("Connecting to CoreNLP Server...")

    CORESERVER = 'http://corenlp.run'
    properties = (
        ('properties', '{"annotators":'"'%s'"',"outputFormat":"json"}'%(annotators)),
    )
    trial = 0
    while trial < TRIALS:
        try:
            response = requests.post(CORESERVER, params=properties, data=input)
            break
        except:
            trial += 1
            print('Trial Number', trial, ' -> Connection Error: ', sys.exc_info()[0])
            time.sleep(SLEEPTIME)
    else:
        raise Exception("Couldn't Connect to the CoreNLP Server.")
    
    print('CoreNLP Server Returned.')

    return json.loads(response.text)


def tokenize(text):
    print('Tokenizing...')
    jsonRet = call_core(text, "tokenize,ssplit")['sentences']
    tokens = dict()
    for sent_id in range(len(jsonRet)):
        sentDict = dict()
        idx = 0
        for x in jsonRet[sent_id]['tokens']:
            sentDict[idx] = x['originalText']
            idx += 1
        tokens[sent_id] = sentDict
    print('Tokenization done:', tokens)
    return tokens


def solve_coref(text):
    print("Solving Coreferences...")
    jsonRet = call_core(text, "coref,ssplit")
    tokens = tokenize(text)
    for num in jsonRet['corefs'].keys():
        representative = ""
        nonRepresentatives = []
        for mention in jsonRet['corefs'][num]:
            if mention['isRepresentativeMention']:
                representative = mention['text']
            else:
                nonRepresentatives.append((mention['sentNum'], mention['startIndex']))

        for nr in nonRepresentatives:
            tokens[int(nr[0])-1][int(nr[1])-1] = representative

    ret = []
    for sent_id in tokens:
        for idx in range(len(tokens[sent_id])):
            ret.append(tokens[sent_id][idx])
    ret = ' '.join(ret)
    print("Solving Coreferences done: ", ret)
    return ret


#The Dictionary structure is
#   dict[sentence_number][phrase_number]
def openie(text):
    print('Parsing...')
    jsonRet = call_core(text, 'openie')['sentences']
    ret = dict()

    keys = ['object', 'relation', 'subject']

    for sent in jsonRet:
        ret[sent['index']] = dict()
        index = 0
        for phrase in sorted(sent['openie'], key = lambda ph : ph['subjectSpan']):           #loop on the sorted list
            ret[sent['index']][index] = {key: phrase[key] for key in keys}
            index += 1
    
    print('Parsing done:', ret)
    return ret

def enhancedDependencies(text):
    print('Finding Dependencies...')
    jsonRet = call_core(text, 'parse')
    ret = dict()
    print(jsonRet)

#Returns a dictionary[original_text] that contains:
#lemma => the lemma of the original word
#begin => the beginning index in the original text
#end => the ending index in the original text
#pos => the part of speech
def get_info(text):
    print('Getting Lemmas...')
    jsonRet = call_core(text, 'lemma')['sentences']
    ret_dict = dict()
    for sent in jsonRet:
        for token in sent['tokens']:
            ret_dict[token['originalText']] = dict()
            ret_dict[token['originalText']]['lemma'] = token['lemma']
            ret_dict[token['originalText']]['begin'] = token['characterOffsetBegin']
            ret_dict[token['originalText']]['end'] = token['characterOffsetEnd']
            ret_dict[token['originalText']]['pos'] = token['pos']
    print('Lemmatizing done:', ret_dict)
    return ret_dict