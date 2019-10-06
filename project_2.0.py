import bs4 as bs  
import urllib.request  
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import heapq

#function - taking user input
def userinput():
    inp_url=input("Enter a url: ")
    return inp_url

"""function - checking validity of input (This program is dealing with wikipedia pages only. 
Links to other websites are considered invalid )"""
def validity_input(inp_url):
    if inp_url[0:30]!='https://en.wikipedia.org/wiki/':
        return False
    else:
         return True

def get_data(inp_url):
    #storing data scraped from wikipedia page 
    scraped_data = urllib.request.urlopen(inp_url)
    
    #reading the scraped data - type(wikiarticle) = bytes
    wikiarticle = scraped_data.read() 
    
    #converting the data into a BeautifulSoup object. type(parsed_article)=bs4.BeautifulSoup
    parsed_article = bs.BeautifulSoup(wikiarticle,'lxml')
    
    """storing all the text in the webpage, which is enclosed within <p> and </p> tags. type(paragraphs)=bs4.element.ResultSet
    ResultSet is iterable, supports indexing. Basically functions as a list in this program"""
    paragraphs = parsed_article.find_all('p') 
    
    #creating empty string
    wikiarticle_text = ""
    
    #storing all text from the webpage in a string
    for p in paragraphs:  
        wikiarticle_text += p.text
    
    return wikiarticle_text
        
def format_data(inp_url,wikiarticle_text):
    #replacing references - numbers enclosed in square brackets - with spaces
    wikiarticle_text = re.sub(r'\[[0-9]*\]', ' ', wikiarticle_text)
    
    #replacing multiple spaces with single space
    wikiarticle_text = re.sub(r'\s+', ' ', wikiarticle_text)
    
    #replacing punctuations with single space 
    formatted_wikiarticle = re.sub('[^a-zA-Z]', ' ', wikiarticle_text )
    
    #replacing multiple space with single space
    formatted_wikiarticle = re.sub(r'\s+', ' ', formatted_wikiarticle)
    
    """tokenizing the article and storing the tokens in a list - tokenize in this case means to split the data into sentences.
    Here, the default parameter is '.'. Since formatted_wikiarticle doesn't have '.', it cannot be tokenized"""
    sentence_list = nltk.sent_tokenize(wikiarticle_text)
    
    return wikiarticle_text,formatted_wikiarticle,sentence_list
    
"""storing words that are unnecessary in a summary, such as 'a', 'an', 'the', etc. in a list 
(these words are known as stop words). Parameter is 'english' as summarising webpages written in the English language"""
stopwords = nltk.corpus.stopwords.words('english')

def generatesum(formatted_wikiarticle,sentence_list):
    #creating a dictionary to store words as the keys and their frequencies as their values
    word_frequencies = {} 
    
    #iterating through each word in the article
    for word in nltk.word_tokenize(formatted_wikiarticle):  
        #considering only those words which are not stop words
        if word not in stopwords: 
            if word not in word_frequencies.keys():
                #for first occurence of word, setting frequency to 1
                word_frequencies[word] = 1 
            else:
                #for repeated occurence of word, increasing frequency by 1
                word_frequencies[word] += 1 
    
     #finding maximum frequency
    maxfreq = max(word_frequencies.values())
    
    for word in word_frequencies:
        """in the existing dictionary, making the value of the word its relative frequency.
        Relative frequency of a word = its frequency/ maximum frequency"""
        word_frequencies[word] = (word_frequencies[word]/maxfreq) 
    
    """making a dictionary to store sentences as the key and sentence score as the value.
    The sentence score is the sum of the relative frequencies of the words in the sentence"""   
    sentence_scores = {} 
    
    #looping through each sentence in the sentence_list and tokenizing the sentence into words.
    for sent in sentence_list: 
        #considering each word in the sentence, in lowercase
        for word in nltk.word_tokenize(sent.lower()):
            """checking if the word exists in the word_frequencies dictionary.
            This check is performed since we created the sentence_list list from the wikiarticle_text object but the word frequencies were calculated 
            using the formatted_wikiarticle object(which doesn't contain any stop words, numbers, etc.)"""
            if word in word_frequencies.keys(): 
                #considering only those sentences which have less than 30 words
                if len(sent.split(' ')) < 30: 
                    if sent not in sentence_scores.keys():
                        #for first word of sentence, setting frequency to frequency of the first word
                        sentence_scores[sent] = word_frequencies[word] 
                    else:
                        #for other words (not first word) in same sentence, increasing frequency by frequency of the word
                        sentence_scores[sent] += word_frequencies[word]

 #gathering the 7 sentences which have the largest scores into a list
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    
    #making the sentences into a printable format
    summary = ''.join(summary_sentences)
    
    #generating the summary 
    print("Summarised version of the article: ")
    print()
    print(summary)
    
#calling all the above functions
def call():
    print("ICUP LAB PROJECT: AUTOMATIC TEXT SUMMARISATION")
    print()
    print("In this project, we will attempt to summarise the contents of any Wikipedia page provided into a single paragraph.")
    inp_url=userinput()
    print()
    while validity_input(inp_url)!=True:
         print("Invalid url. Please enter the url of any wikipedia page.")
         inp_url=userinput()
    art=get_data(inp_url)
    art,form_art,sentlist=format_data(inp_url,art)
    generatesum(form_art,sentlist)
    
call()   
    
    
    
                        

     
     
     

 
                        
                        


