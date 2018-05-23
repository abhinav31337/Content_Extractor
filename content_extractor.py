
############################################## Abhinav Pachauri #########################################################################
##############  In order to run on the content extractor on command line just type: python content_extractor.py -i <inputfile_name> #####
############# A folder named "output" will be created at the path where this file "content_extractor.py" is saved and ###################
############# then n files will be further created within this output folder numbered from 1 to n #######################################
############# where n is the number of URLs provided in the inputfile to extract the important content.  ################################
#########################################################################################################################################

from __future__ import print_function
import codecs
import os
import sys, getopt
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

nltk.download('stopwords')
reload(sys)  
sys.setdefaultencoding('utf8')

n_features = 1000
n_components = 10
n_top_words = 20
matching_threshold=0.9

def undesired_tags(element):
	if element.parent.name in ['style', 'script', 'head','title' 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True

def topics(model, feature_names, n_top_words):
    top_words=[]
    for topic_idx, topic in enumerate(model.components_):
        top_words += [feature_names[i].encode('utf-8') for i in topic.argsort()[:-n_top_words - 1:-1]]
    return top_words       

def extractor(input_file,out_directory="output"):
	if not os.path.exists(out_directory):
		os.makedirs(out_directory)

	### Reading urls from file
	urls = codecs.open(input_file, "r",encoding='utf-8', errors='ignore').readlines()
	for i,url in enumerate(urls):
		print("Processing "+str(i)+". "+urls[i]+" link..")
		output_file = os.path.join(out_directory,'output'+str(i+1)+'.txt')
		fw = open(output_file,'w')
		print("opening link..")
		try:
	 		html = requests.get(url.split('\n')[0]).text
	 		soup = BeautifulSoup(html)
	 		all_text = soup.find_all(text=True)
		 	stop = stopwords.words('english') + list(string.punctuation)

		 	theme_wordcount=0
		 	titleline= soup.find('h1').get_text()
		 	title_words = [i for i in word_tokenize(titleline.lower()) if i not in stop]

		 	print("Extracting first all the text from webpage..")
		 	lines = [patch.split('.') for patch in filter(undesired_tags, all_text)]
			all_text_lines=[]
			for line_list in lines:
				for line in line_list:
					all_text_lines.append(line.strip())

			tf_vectorizer = CountVectorizer(max_features=n_features,stop_words=stop)
			tf = tf_vectorizer.fit_transform(all_text_lines)
			tf_feature_names = tf_vectorizer.get_feature_names()
			lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,learning_method='online',learning_offset=50.,random_state=0)
			lda.fit(tf)
			topic_top_words = topics(lda, tf_feature_names, n_top_words)
			print("Picking up main theme of the page..")
			desired_text_lines=[]
			for ind,textline in enumerate(all_text_lines):
				textline_tokens = [i for i in word_tokenize(textline.lower()) if i not in stop]
				theme_match=0
				if len(textline_tokens)>0:
					for token in textline_tokens:
						if(token in topic_top_words):
							theme_match+=1
					if(((float(theme_match))/len(textline_tokens))>((float(ind))/(len(all_text_lines)))):
						desired_text_lines.append(textline)

			print("Retreiving Relavant text related to theme of the page only...")
			fw.write(u" ".join(unicode(t.strip()) for t in desired_text_lines))
			fw.close()
		except requests.ConnectionError as e:
			print("Connection Error. Make sure connected to Internet.Details given below.\n")
			print(str(e))
		except KeyboardInterrupt:
			print("Someone closed the program")

def main(argv):
	inputfile = ''
	outputfile = ''
	opts, args = getopt.getopt(argv,"hi:o:",["ifile="])

	for opt, arg in opts:
		if opt == '-h':
			print('test.py -i <inputfile>')
 			sys.exit()
 		elif opt in ("-i", "--ifile"):
			inputfile = arg

	extractor(inputfile)

if __name__ == "__main__":
	main(sys.argv[1:])







