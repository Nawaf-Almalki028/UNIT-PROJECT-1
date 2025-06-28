from rapidfuzz import process

def similar_words_handler(word, words):
  process_similar = process.extractOne(word,words)

  if process_similar:
    return True,  process_similar[0], process_similar[1]
  
  else:
    return False, None, process_similar[1]
