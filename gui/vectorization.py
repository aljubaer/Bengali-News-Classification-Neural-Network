
import numpy as np
import json

index_file = open('word_index_for_seven_topics.txt', encoding='utf-8')
index_json = json.load(index_file)
# print("Total unique words found: ", len(index_json))
def text_to_sequences(text, dimensions=len(index_json) + 100):
  arr = np.zeros(dimensions)
  for word in text:
    if word in index_json:
      arr[index_json[word]] = 1

  return np.array([arr])

