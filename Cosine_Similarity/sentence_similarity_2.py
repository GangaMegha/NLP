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


# Function for measuring the cosine similarity given 2 sentences (modelled as sparce dictionaries) a and b from the corpus
''' 
Ex : a = [1:1, 2:1, 3:2]
     b = [2:2, 3:1, 4:2, 5:1]

The keys represent the word index and the values represent the word count in the sentence.
'''
def cosine_similarity(a,b):

	x_key = set(a.keys()) # {1,2,3}
	y_key = set(b.keys()) # {2,3,4,5}

	common = x_key & y_key # {2,3} Intersection of sets => words present in both a and b

	x_val = [a[key] for key in common] # [1,2] Word count corresponding to common words in a
	y_val = [b[key] for key in common] # [2,1] Word count corresponding to common words in b

	''' 
	Cosine Similarity = a.b/( ||a|| * ||b|| )

	Here, a.b = Sum of product of common word occurances in a and b
			  = x_val . y_val
			  = 1*2 + 2*1

		||a|| = Norm of vector a 
			  = Norm (a.values()) since a is a dictionary
			  = sqrt(1*1 + 1*1 + 2*2)

		Similarly for ||b||
	'''
	return(sum([x*y for x,y in zip(x_val,y_val)])/( math.sqrt(sum([x*x for x in a.values()])) * math.sqrt(sum([y*y for y in b.values()])) ))


# Function for building the corpus using sentences present in files whose names are stored in mainFile
def build_corpus(mainFile):
	# Dictionary for holding the unique words as key and their index as value
	diction = dict()
	# Corpus is a list in which each element of the list corresponds to a sentence represented as a dictionary 
	# where keys represent the word indices and values represent the number of occurances of the word in the sentence
	corpus = []

	# Getting list of filenames
	FileNames = getFiles(mainFile)

	# Building the corpus and the dictionary for words
	for filename in FileNames :
		# Dictionary for representing a sentence with keys as word indices and values as word count
		sen_dict = dict()
		# Reading the sentence from the file given by filename
		sentence = getSentence(filename)
		
		for word in sentence :
			if not(diction.has_key(word)):
				# Index of each new unique word assigned as the current length of the dictionary
				diction[word] = len(diction)
			# Count =1 if new word, else increment the count corresponding to the word occurance
			sen_dict[diction[word]] = sen_dict[diction[word]] + 1 if diction[word] in sen_dict else 1
		# Append the current sentence representation into the corpus
		corpus.append(sen_dict)

	return(corpus, diction)

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('--mainFile', action="store", dest="mainFile", default="filenames.txt", type = str)
	parser.add_argument('--outFile', action="store", dest="outFile", default="similarity_2.txt", type = str)
	parser.add_argument('--dictionOut', action="store", dest="dictionOut", default="dictionary.txt", type = str)
	parser.add_argument('--corpusOut', action="store", dest="corpusOut", default="corpus_2.txt", type = str)

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
