from rapidfuzz import process

word1 = "prodct"
words1 = ["products","hellothere"]

def similar_words_handler(word, words):
  process_similar = process.extractOne(word,words)

  if process_similar:
    return process_similar[0]
  else:
    return None
