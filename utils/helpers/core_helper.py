import os
import json
import requests
import sys
import time

TRIALS = 10
SLEEPTIME = 1

def log(message):
    sys.stderr.write(message + '\n')
    sys.stderr.flush()

#properties = {"annotators": -list of comma separated annotators-, "outputFormat": "json"}
def call_core(input, annotators):
    log("Connecting to CoreNLP Server...")

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
            log('Trial Number '+  str(trial)+ ' -> Connection Error: '+ sys.exc_info()[0])
            time.sleep(SLEEPTIME)
    else:
        raise Exception("Couldn't Connect to the CoreNLP Server.")
    
    log('CoreNLP Server Returned.')

    return json.loads(response.text)


def tokenize(text):
    log('Tokenizing...')
    jsonRet = call_core(text, "tokenize,ssplit")['sentences']
    tokens = dict()
    for sent_id in range(len(jsonRet)):
        sentDict = dict()
        idx = 0
        for x in jsonRet[sent_id]['tokens']:
            sentDict[idx] = x['originalText']
            idx += 1
        tokens[sent_id] = sentDict
    log('Tokenization done: '+ str(tokens))
    return tokens

#returns a dict[word_idx] = representative
def solve_coref(text):
    log("Solving Coreferences...")
    jsonRet = call_core(text, "coref")
    tokens = tokenize(text)
    ret = dict()
    for num in jsonRet['corefs'].keys():
        representative = ""
        nonRepresentatives = []
        for mention in jsonRet['corefs'][num]:
            if mention['isRepresentativeMention']:
                representative = mention['text']
            else:
                nonRepresentatives.append(mention['startIndex'])

        for nr in nonRepresentatives:
            ret[nr] = representative
    return ret


#The Dictionary structure is
#   dict[sentence_number][phrase_number]
def openie(text):
    log('Parsing...')
    jsonRet = call_core(text, 'openie')['sentences']
    ret = dict()

    keys = ['object', 'relation', 'subject']

    for sent in jsonRet:
        ret[sent['index']] = dict()
        index = 0
        for phrase in sorted(sent['openie'], key = lambda ph : ph['subjectSpan']):           #loop on the sorted list
            ret[sent['index']][index] = {key: phrase[key] for key in keys}
            index += 1
    
    log('Parsing done: '+ str(ret))
    sys.stderr.flush()
    return ret

def enhanced_dependencies(text):
    log('Finding Dependencies...')
    jsonRet = call_core(text, 'parse')['sentences']
    dep_dict = dict()
    for sent in jsonRet:
        dep_dict[sent['index']] = dict()
        for dependency in sent['basicDependencies']:
            if dependency['governorGloss'] == 'ROOT':
                continue
            if dependency['governor'] not in dep_dict[sent['index']]:
                dep_dict[sent['index']][dependency['governor']] = list()
            dep_dict[sent['index']][dependency['governor']].append({
                                                                        'dependancy': dependency['dep'],
                                                                        'dependent': dependency['dependent']
                                                                        })
    log('Finding Dependencies done: ' + str(dep_dict))
    return dep_dict

#Returns a dictionary[sentence_index][token_index] that contains:
#lemma => the lemma of the original word
#begin => the beginning index in the original text
#end => the ending index in the original text
#pos => the part of speech
#text => original text
#rep ?=> the representative (if it has)
#is_person ?=> if this is a person entity
def get_info(text):
    log('Getting Lemmas...')
    jsonRet = call_core(text, 'lemma, ner')['sentences']
    ret_dict = dict()
    corefs = solve_coref(text)

    persons = [];
    for sent in jsonRet:
        for entity in sent['entitymentions']:
            if entity['ner'] == 'PERSON':
                persons.append(entity['text'])
        ret_dict[sent['index']] = dict()
        for token in sent['tokens']:
            ret_dict[sent['index']][token['index']] = dict()
            ret_dict[sent['index']][token['index']]['lemma'] = token['lemma']
            ret_dict[sent['index']][token['index']]['begin'] = token['characterOffsetBegin']
            ret_dict[sent['index']][token['index']]['end'] = token['characterOffsetEnd']
            ret_dict[sent['index']][token['index']]['pos'] = token['pos']
            ret_dict[sent['index']][token['index']]['text'] = token['originalText']
            if token['index'] in corefs:
                ret_dict[sent['index']][token['index']]['rep'] = corefs[token['index']]
            if token['originalText'] in persons:
                ret_dict[sent['index']][token['index']]['is_person'] = True
    log('Lemmatizing done: '+ str(ret_dict))
    return ret_dict