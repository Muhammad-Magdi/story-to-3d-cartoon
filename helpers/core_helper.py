import os
import json
import requests

#properties = {"annotators": -list of comma separated annotators-, "outputFormat": "json"}

def call_core(input, annotators):
    properties = (
        ('properties', '{"annotators":'"'%s'"',"outputFormat":"json"}'%(annotators)),
    )
    response = requests.post('http://corenlp.run', params=properties, data=input)
    return json.loads(response.text)

def tokenize(text):
    jsonRet = call_core(text, "tokenize,ssplit")
    tokens = dict()
    for sentIdx in range(len(jsonRet['sentences'])):
        sentDict = dict()
        idx = 0
        for x in jsonRet['sentences'][sentIdx]['tokens']:
            sentDict[idx] = x['originalText']
            idx += 1
        tokens[sentIdx] = sentDict
    return tokens


def solve_coref(text):
    jsonRet = call_core(text, "coref,ssplit")
    tokens = tokenize(text)
    for num in jsonRet['corefs'].keys():
        representative = "";
        nonRepresentatives = [];
        for mention in jsonRet['corefs'][num]:
            if mention['isRepresentativeMention']:
                representative = mention['text']
            else:
                nonRepresentatives.append((mention['sentNum'], mention['startIndex']))

        for nr in nonRepresentatives:
            tokens[int(nr[0])-1][int(nr[1])-1] = representative

    ret = []
    for sentIdx in tokens:
        for idx in range(len(tokens[sentIdx])):
            ret.append(tokens[sentIdx][idx])
    return ' '.join(ret)
