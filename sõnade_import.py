import nltk
from nltk.corpus import words
from nltk.corpus import PlaintextCorpusReader

import random

english_words = words.words('en-basic')

random_index = random.randint(0, len(english_words) - 1)

random_english_word = english_words[random_index]
print(random_english_word)