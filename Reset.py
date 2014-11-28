import pickle

dictionary = {}
pickle.dump(dictionary,open('userData/database.p','wb'))

avg_scores = {'users':0, 'total_correct': 0, 'total_attempt':0, 'total_digits':0}
pickle.dump(avg_scores,open('userData/avgscores.p','wb'))