import utils.helpers.nltk_helper as nltk
import utils.helpers.core_helper as core
import json
import utils.utils as utils
import utils.word2vec as w2v

aux_list = list()
word_info = dict()      #lemma, pos, begin, end, text, rep
action_synset_dict = dict()    #supported actions
action_dict = dict()

#CONSTANTS
TREEWEIGHT = 1
EUCLIDEANWEIGHT = 2
COSINEWEIGHT = 3
#

subject_tags = ['nsubj', 'csubj', 'nsubjpass']
object_tags = ['nmod', 'amod', 'dobj', 'iobj']
aux_tags = ['aux', 'auxpass']

def initialize_lists():
    #Auxiliaries List
    # global aux_list
    # aux_file = open('data/aux.json', 'r')
    # aux_list = json.loads(aux_file.read())
    # aux_list = ["do", "have", "be", "may", "must", "shall", "will", "can"]
    #Supported Actions list
    global action_synset_dict
    global action_dict
    action_file = open('data/actions.json')
    action_dict = json.loads(action_file.read())
    for action in action_dict:
        action_synset_dict[action] = nltk.get_verb_synset(action)

#A voting system that chooses the most similar synset to the given verb
def most_similar(verb):
    freq = dict()

    lch_candidate = nltk.most_similar_lch(action_synset_dict, verb)
    freq[lch_candidate] = TREEWEIGHT
    path_candidate = nltk.most_similar_path(action_synset_dict, verb)
    freq[path_candidate] = TREEWEIGHT if path_candidate not in freq.keys() else freq[path_candidate]+TREEWEIGHT
    # wup_candidate = nltk.most_similar_wup(action_synset_dict, verb)
    # freq[wup_candidate] = TREEWEIGHT if wup_candidate not in freq.keys() else freq[wup_candidate]+TREEWEIGHT
    w2v_euclidean_candidate = w2v.most_similar_euclidean(action_dict, verb)
    freq[w2v_euclidean_candidate] = EUCLIDEANWEIGHT if w2v_euclidean_candidate not in freq.keys() else freq[w2v_euclidean_candidate]+EUCLIDEANWEIGHT
    w2v_cosine_candidate = w2v.most_similar_cosine(action_dict, verb)
    freq[w2v_cosine_candidate] = COSINEWEIGHT if w2v_cosine_candidate not in freq.keys() else freq[w2v_cosine_candidate]+COSINEWEIGHT

    winner = list(freq.keys())[0]
    max_score = list(freq.values())[0]
    for candidate, score in freq.items():
        if score > max_score:
            winner = candidate
            max_score = score

    utils.log('The most similar to "%s" is "%s" with score = %d'%(verb, winner, max_score))
    return winner

def get_text(sent, index):
    return word_info[sent][index]['text']

def get_rep(sent, index):
    return word_info[sent][index]['rep']

def get_lemma(sent, index):
    return word_info[sent][index]['lemma']

def get_text(sent, index):
    return word_info[sent][index]['text']

def is_verb(sent, index):
    return word_info[sent][index]['pos'][0] == 'V'

def is_person(sent, index):
    return 'person' in word_info[sent][index] or 'rep' in word_info[sent][index]

#Removes {a, an, the} from the noun
#Substitute pronouns with nouns
def fix_noun(sent, noun_index):
    noun = get_text(sent, noun_index) if 'rep' not in word_info[sent][noun_index] else get_rep(sent, noun_index)
    while 'a ' in noun: noun = noun.replace('a ', '')
    while 'the ' in noun: noun = noun.replace('the ', '')
    while 'an ' in noun: noun = noun.replace('the ', '')
    return noun

def fix_verb(sent, verb_index):
    verb = get_lemma(sent, verb_index)
    verb = most_similar(verb)
    return verb

def dependency_solver(dependencies):
    ret_dict = {'objects':[], 'data': []}
    for sent in dependencies:
        for governor_index in sorted(dependencies[sent]):
            if is_verb(sent, governor_index):
                event = dict()
                governor = get_text(sent, governor_index)
                event['action'] = fix_verb(sent, governor_index)
                for dep in dependencies[sent][governor_index]:
                    if dep['dependancy'] in subject_tags:
                        event['actor'] =  fix_noun(sent, dep['dependent']).capitalize()
                    if dep['dependancy'] in object_tags:
                        if not 'obj' in event:
                            event['obj'] = fix_noun(sent, dep['dependent'])
                        else:
                            event['obj2'] = fix_noun(sent, dep['dependent'])
                        if not is_person(sent, dep['dependent']) and not get_text(sent, dep['dependent']) in ret_dict['objects']:
                            ret_dict['objects'].append(get_text(sent, dep['dependent']))
                if 'actor' in event:
                    ret_dict['data'].append(event)
    return ret_dict

#This may be the main function that returns
#the JSON -List of Events- to be used in Graphics Part.phrase
def nlp(raw_input):
    initialize_lists()
    global word_info
    #Solving Coreferences
    # corefs = core.solve_coref(raw_input)
    #Tokenizing to get lemmas, POS
    word_info = core.get_info(raw_input)
    #Extract Relations
    # relations = core.openie(without_coref)
    #Get Dependencies
    dependencies = core.enhanced_dependencies(raw_input)
    #Put events in the format: {actor, action, obj}
    ret = dependency_solver(dependencies)
    return json.dumps(ret)
    # return json.dumps(format_event(relations))
    #Replacing strange nouns/actions


raw_input = input()

print(nlp(raw_input))