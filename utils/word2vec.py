import gensim
from numpy.linalg import norm
from numpy import dot
import sys
from nltk.data import find

word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=False)

def log(message):
    sys.stderr.write(message + '\n')
    sys.stderr.flush()

def euclidean_distance(vec1, vec2):
    return norm(vec2-vec1)

def cosine_distance(vec1, vec2):
    return 1 - (dot(vec1, vec2)/(norm(vec1)*norm(vec2)))

def most_similar_cosine(list, word1):
    log("Measuring Cosine distance for " + word1)
    min_dist = float('inf')
    min_word = ''
    word1vec = model[word1]
    for word2 in list:
        word2vec = model[word2]
        dist = cosine_distance(word1vec, word2vec)
        log(str(word2) + " " + str(dist))
        if dist < min_dist:
            min_word = word2
            min_dist = dist
    return min_word

def most_similar_euclidean(list, word1):
    log("Measuring Euclidean distance for " + word1)
    min_dist = float('inf')
    min_word = ''
    word1vec = model[word1]
    for word2 in list:
        word2vec = model[word2]
        dist = euclidean_distance(word1vec, word2vec)
        log(str(word2) + " " + str(dist))
        if dist < min_dist:
            min_word = word2
            min_dist = dist
    return min_word