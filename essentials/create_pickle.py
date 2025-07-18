import pickle

with open('.wordlist/german_nouns_5.txt', 'r', encoding='latin-1') as wordlist:
    content = [line.strip() for line in wordlist]

with open('pickled_wordlist.pkl', 'wb') as pickled:
    pickle.dump(content, pickled)