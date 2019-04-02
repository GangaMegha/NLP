# Cosine Similarity between sentences 
The sentences are represented as sparce matrices(words).

So you'll find 2 python files :

  sentence_similarity.py : Ignores the number of word occurrences while building the corpus. 
  sentence_similarity_2.py : Similarity computed by taking into account the number of word occurrences in the sentence.

The generated word dictionaries in both scenarios are the same. Only the corpus representation changes. 
You can see this in corpus.txt and corpus_2.txt. 
The resultant similarity upper triangular matrix (including the diagonal) for the sentences in both cases can be found in similarity.txt and similarity_2.txt. 
The first scenario is faster, but the difference in results can be observed in the last 2 sentences : 
      he knows a clue clue clue clue
      he knows a clue
For which we get a similarity of 1.0 and 0.803 respectively using codes (1) and (2).

The command line options are :
    --mainFile : default="filenames.txt"
    --outFile : default="similarity.txt" or default="similarity_2.txt"
    --dictionOut : default="dictionary.txt"
    --corpusOut : default="corpus.txt" or default="corpus_2.txt"
    
The sentence files are inside the folder 'files'.
