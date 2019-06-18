import utils.helpers.nltk_helper as nltk
import utils.helpers.core_helper as core
import json
import utils.utils as utils

aux_list = list()
word_info = dict()      #lemma, pos, begin, end
action_synset_dict = dict()    #supported actions

subject_tags = ['nsubj', 'csubj', 'nsubjpass']
object_tags = ['nmod', 'amod', 'dobj', 'iobj']
aux_tags = ['aux', 'auxpass']

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
        for sent in word_info:
            if word_info[verb]['lemma'] not in aux_list:
                ret.append(verb)
    return ret

def lemmatize_verb(sent, verb):
    return word_info[sent][verb]['lemma']

def fix_verb(sent, verb):
    verb = lemmatize_verb(sent, verb)
    verb = nltk.most_similar(action_synset_dict, verb)
    return verb

def format_event(relations):
    utils.log('Dividing Events...')
    ret_list = list()
    for sent_id in relations:
        for phrase_id in relations[sent_id]:
            phrase = relations[sent_id][phrase_id]
            event = dict()
            event['action'] = fix_verb(phrase['relation'])
            event['subject'] = phrase['subject']        #to be edited
            event['object'] = phrase['object']          #to be edited
            ret_list.append(event)
    utils.log('Dividing Events done.')
    return ret_list

def dependency_solver(dependencies):
    events = list()
    for sent in dependencies:
        for governor in dependencies[sent]:
            if word_info[sent][governor]['pos'][0] == 'V':
                event = dict()
                event['action'] = fix_verb(sent, governor)
                for dep in dependencies[sent][governor]:
                    if dep['dependancy'] in subject_tags:
                        event['subject'] = dep['dependent']
                    if dep['dependancy'] in object_tags:
                        event['object'] = dep['dependent']
                if 'subject' in event:
                    events.append(event)
    return events

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
    # relations = core.openie(without_coref)
    #Get Dependencies
    dependencies = core.enhanced_dependencies(without_coref)
    #Put events in the format: {subject, action, object}
    return json.dumps(dependency_solver(dependencies))
    # return json.dumps(format_event(relations))
    #Replacing strange nouns/actions


raw_input = input()

print(nlp(raw_input))