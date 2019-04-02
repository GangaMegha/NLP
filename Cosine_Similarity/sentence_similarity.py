# Accepting filenames as arguments
import argparse 

# For computing square root.
import math

# Function for reading the filenames in the mainFile
'''
Ex : file1.txt
	 file2.txt
'''
def getFiles(mainFile):
	with open(mainFile) as f:
		filenames = [filename.split('\n')[0] for filename in f]
	return(filenames)


# Function for reading the sentences given a filename.
''' 
Ex : I have no clue
'''
def getSentence(filename):
	with open(filename) as f:
		sentence = [word for line in f for word in line.lower().split()]
	return(sentence)


# Function for measuring the cosine similarity given 2 sentences (modelled as sparce vectors) a and b from the corpus
''' 
Ex : a = [1, 2, 3]
     b = [2, 3, 4, 5]

The list elements represent the indices of the words present in the sentence.
Here we assume the number of occurance of each word in a sentence is not accounted for in the corpus
'''
def cosine_similarity(a,b):

	a = set(a) # {1,2,3}
	b = set(b) # {2,3,4,5}

	common = a & b # {2,3} Intersection of sets => words present in both a and b
	''' 
	Cosine Similarity = a.b/( ||a|| * ||b|| )

	Here, a.b = Sum of product of common word occurances in a and b
			  = len(common) since occurance of a word in a sentence corresponds to 1 and absence corresponds to 0 in the corpus
			  = 2

		||a|| = Norm of vector a 
			  = sqrt of the number of non-repeating elements in 'a' since since occurance of a word in a sentence corresponds to 1 and absence corresponds to 0 in the corpus
			  = sqrt(len(number of non-repeating elements in 'a'))
			  = sqrt(a&a)

		Similarly for ||b||
	'''
	return(len(common)/(math.sqrt(len(a&a))*math.sqrt(len(b&b))))


# Function for building the corpus using sentences present in files whose names are stored in mainFile
def build_corpus(mainFile):
	# Dictionary for holding the unique words as key and their index as value
	diction = dict()
	# Corpus is a list in which each element of the list corresponds to a sentence represented as a list of word indices (words present in the sentence) 
	corpus = []

	# Getting list of filenames
	FileNames = getFiles(mainFile)

	# Building the corpus and the dictionary for words
	for filename in FileNames :
		# List for representing a sentence with indices of words in the sentence
		sen = []
		# Reading the sentence from the file given by filename
		sentence = getSentence(filename)
		
		for word in sentence :
			if not(diction.has_key(word)):
				# Index of each new unique word assigned as the current length of the dictionary
				diction[word] = len(diction)
			# append the word index to the sen vector
			sen.append(diction[word])
		# Append the current sentence representation into the corpus
		corpus.append(sen)

	return(corpus, diction)

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('--mainFile', action="store", dest="mainFile", default="filenames.txt", type = str)
	parser.add_argument('--outFile', action="store", dest="outFile", default="similarity.txt", type = str)
	parser.add_argument('--dictionOut', action="store", dest="dictionOut", default="dictionary.txt", type = str)
	parser.add_argument('--corpusOut', action="store", dest="corpusOut", default="corpus.txt", type = str)

	arg_val = parser.parse_args()
	arg_val = vars(arg_val)

  	return(arg_val)



def main():
	config = parse()
	
	# Building the corpus for the sentences and the dictionary for the unique words
	corpus,diction = build_corpus(config['mainFile'])

	# Write the corpus to file
	with open(config['corpusOut'], 'w') as f:
		for ele in corpus:
			f.write(str(ele))
			f.write('\n')

	# Write the dictionary (unique words and indices) to file
	with open(config['dictionOut'], 'w') as f:
		f.write(str(diction))

	# Calculate the similarity between each sentence and write the obtained upper triangular matrix to file
	with open(config['outFile'], 'w') as f:
		for i in range(len(corpus)) :
			sim_arr = []

			# For each sentence i, calculate it's similarity for all sentences after it (sentence i included)
			for j in range(i,len(corpus)) :
				# The calculated similarity rounded off to 3 decimal places
				sim_arr.append(round(cosine_similarity(corpus[i],corpus[j]),3))
			f.write(str(sim_arr))
			f.write('\n')

if __name__== "__main__":
	main()
