import helpers.nltk_helper as nltk
import helpers.core_helper as core
import json

aux_list = list()
word_info = dict()      #lemma, pos, begin, end
action_synset_dict = dict()    #supported actions

def initialize_lists():
    #Auxiliaries List
    global aux_list
    aux_file = open('data/aux.json', 'r')
    aux_list = json.loads(aux_file.read())

    #Supported Actions list
    global action_synset_dict
    action_file = open('data/actions.json')
    for action in json.loads(action_file.read()):
        action_synset_dict[action] = nltk.get_verb_synset(action)


def remove_auxiliaries(verb_phrase):
    ret = list()
    for verb in verb_phrase:
        if word_info[verb]['lemma'] not in aux_list:
            ret.append(verb)
    return ret

def lemmatize_verbs(verb_list):
    for index in range(len(verb_list)):
        verb_list[index] = word_info[verb_list[index]]['lemma']
    return verb_list

def fix_verb(verb_phrase):
    verb_list = verb_phrase.split(' ')
    verb_list = remove_auxiliaries(verb_list)
    for idx, verb in enumerate(verb_list):
        if word_info[verb]['pos'][0] == 'V':
            verb_list = lemmatize_verbs(verb_list)
            verb_list[idx] = nltk.most_similar(action_synset_dict, verb)
    return ' '.join(verb_list)

def format_event(relations):
    print('Dividing Events...')
    ret_list = list()
    for sent_id in relations:
        for phrase_id in relations[sent_id]:
            phrase = relations[sent_id][phrase_id]
            event = dict()
            event['action'] = fix_verb(phrase['relation'])
            event['subject'] = phrase['subject']        #to be edited
            event['object'] = phrase['object']          #to be edited
            ret_list.append(event)
    print('Dividing Events done.')
    return ret_list

#This may be the main function that returns
#the JSON -List of Events- to be used in Graphics Part.phrase
def nlp(raw_input):
    initialize_lists()
    global word_info

    #Solving Coreferences
    without_coref = core.solve_coref(raw_input)
    #Tokenizing to get lemmas, POS
    word_info = core.get_info(without_coref)
    #Extract Relations
    relations = core.openie(without_coref)
    #Put events in the format: {subject, action, object}
    return json.dumps(format_event(relations))
    #Replacing strange nouns/actions



raw_input = input()
print(nlp(raw_input))