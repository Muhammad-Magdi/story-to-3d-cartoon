from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag

#Removes stopwords specified in the stopwords.txt file
def remove_stopwords(text):
    print('Removing stopwords...')
    word_arr = word_tokenize(text)
    f = open('data/stopwords.txt')
    stopwords = f.read()
    word_arr = [word for word in word_arr if word not in stopwords]
    print('Stopwords removed.')
    return word_arr

# def handle_negation(text):
#     f = open('data/stopwords_negation.txt')
#     stopwords_negation = f.read()
#     word_arr = [word if word not in stopwords_negation else 'not' for word in word_arr]

#Removes the stop words
def clean_data(text):
    print('Cleaning text...')
    text = text.lower()
    word_arr = remove_stopwords(text)
    # handle_negation(word_arr)
    print('Cleaning done.')
    return ' '.join(word_arr)

#Tokenizes and returns the POS of a sentence
def sentence_to_tags(words):
    words = word_tokenize(words)
    POS = pos_tag(words)
    return POS

def most_similar_wup(synsets_dict, verb):
    best_similarity = -1
    most_similar = str()
    verb_synset = wn.synsets(verb, pos = wn.VERB)[0]

    for verb, synset in synsets_dict.items():
        if wn.wup_similarity(synset, verb_synset) > best_similarity:
            best_similarity = wn.wup_similarity(synset, verb_synset)
            most_similar = verb
    
    return most_similar

def most_similar_lch(synsets_dict, verb):
    best_similarity = -1
    most_similar = str()
    verb_synset = wn.synsets(verb, pos = wn.VERB)[0]

    for verb, synset in synsets_dict.items():
        if wn.lch_similarity(synset, verb_synset) > best_similarity:
            best_similarity = wn.lch_similarity(synset, verb_synset)
            most_similar = verb
    
    return most_similar

def most_similar_path(synsets_dict, verb):
    best_similarity = -1
    most_similar = str()
    verb_synset = wn.synsets(verb, pos = wn.VERB)[0]

    for verb, synset in synsets_dict.items():
        if wn.path_similarity(synset, verb_synset) > best_similarity:
            best_similarity = wn.path_similarity(synset, verb_synset)
            most_similar = verb
    
    return most_similar

#A voting system that chooses the most similar synset to the given verb
def most_similar(synsets_dict, verb):
    freq = dict()

    lch_candidate = most_similar_lch(synsets_dict, verb)
    freq[lch_candidate] = 1
    path_candidate = most_similar_path(synsets_dict, verb)
    freq[path_candidate] = 1 if path_candidate not in freq.keys() else freq[path_candidate]+1
    wup_candidate = most_similar_wup(synsets_dict, verb)
    freq[wup_candidate] = 1 if wup_candidate not in freq.keys() else freq[wup_candidate]+1

    winner = list(freq.keys())[0]
    max_score = list(freq.values())[0]
    for candidate, score in freq.items():
        if score > max_score:
            winner = candidate

    print('The most similar to "%s" is "%s" with score = %d'%(verb, winner, max_score))
    return winner

def get_verb_synset(verb):
    return wn.synsets(verb, pos = wn.VERB)[0]

def replace_actions(synsets_dict, verbs):
    for idx, verb in enumerate(verbs):
        verbs[idx] = most_similar(synsets_dict, verb)
    return verbs
