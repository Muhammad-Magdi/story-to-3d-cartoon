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

#Determines the word that's most similar to the given word
def similarity(list,word):
    best=-1
    ind=-1
    word = wn.synsets(word, pos = wn.VERB)[0]
    for i in range(len(list)):
        if wn.wup_similarity(list[i], word) > best:
            best=word.wup_similarity(list[i])
            ind=i
    return list[ind].name().split('.')[0]

def replace_actions(raw_input):
    print(raw_input)
    pos_string = sentence_to_tags(raw_input)
    our_actions = []
    file = open('data/actions.txt', 'rt')
    for line in file:
        line = line[0:-1]
        our_actions.append(wn.synsets(line, pos = wn.VERB)[0])

    idx = 0
    for word_tag in pos_string:
        if word_tag[1][0] == 'V':
            raw_input = raw_input.replace(word_tag[0], similarity(our_actions, word_tag[0]))
    return raw_input

#Takes an event and returns a map of its content
def event_divider(event):
    event_words = remove_stopwords(event)
    pos = sentence_to_tags(event)

    ret = dict()
    ret['subject'] = pos[0][0]
    ret['action'] = pos[1][0]
    if len(pos) >= 3 : ret['object'] = pos[2][0]
    return ret
