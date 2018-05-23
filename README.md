# Content_Extractor

***********************************************************************************************************************

In order to run the content extractor on command line please type :

**python content_extractor.py -i <inputfile_name>**

**inputfile_name** : name of the file containing all the links one per line content of which you want to get extracted.
**Example** : python content_extractor.py url_links.txt

**Prerequisite** : NLTK, Sklearn, BeautifulSoup if not installed please install these packages using pip or any other method.

If even after installing NLTK following errors comes please do the their respective dowloads using nltk only.

Resource **punkt** not found.

  -> nltk.download('punkt')
  
Resource **stopwords** not found.

  -> nltk.download(’stopwords’)
  
Basic workflow of the code :

**1.** Extracting first all the text from webpage

**2.** Picking up main theme of the page

**3.** Retreiving Relavant text based on theme of the page

***********************************************************************************************************************


