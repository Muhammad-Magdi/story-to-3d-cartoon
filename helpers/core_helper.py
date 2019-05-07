import os
import json

def call_core(input, annotators, output_file):
    output_file = "gen/%s"%(output_file)
    line = """wget --post-data '%s' 'http://corenlp.run/?properties={"annotators": "%s", "outputFormat": "json"}' -O %s"""
    os.system(line %(input,annotators,output_file))

def tokenize(text):
    call_core(text, "tokenize,ssplit", "tokens.txt")
    jsonRet = json.loads(open('gen/tokens.txt', 'r').read())
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
    call_core(text, "coref,ssplit", "coref.txt")
    jsonRet = json.loads(open('gen/coref.txt', 'r').read())

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
