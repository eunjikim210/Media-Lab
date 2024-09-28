import nltk
nltk.download('punkt')
import re
import pandas as pd

from funcs.utils import *
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

out_path = "/"
data_path = "/"

the_data = file_walker(data_path)


def load_lexicons():
    with open('/positive-words.txt', 'r') as file:
        positive_lexicon = set(file.read().splitlines())
    with open('/negative-words.txt', 'r') as file:
        negative_lexicon = set(file.read().splitlines())
    return positive_lexicon, negative_lexicon

def gen_senti(text):
    positive_lexicon, negative_lexicon = load_lexicons()
    
    # Regex
    text_no_punctuation = re.sub(r'[^\w\s]', '', text.lower())
    
    # Splits the text into words
    tokens = word_tokenize(text_no_punctuation)
    
    pc, nc = 0, 0  
    
    for token in tokens:
        if token in positive_lexicon:
            pc += 1
        if token in negative_lexicon:
            nc += 1
    
    # Make sure the text contains both positive and negative words
    if pc > 0 and nc > 0:
        S = (pc - nc) / (pc + nc)
        return S
    else:
        # Return None if text doesn't have both positive and negative words
        return None  



def apply_gen_senti(text):
    # Make sure the text is string
    if isinstance(text, str):
        return gen_senti(text)
    else:
        return None  

the_data['simple_senti'] = the_data['body'].apply(apply_gen_senti)




analyzer = SentimentIntensityAnalyzer()
def get_vader_score(text):
    if isinstance(text, str):
        scores = analyzer.polarity_scores(text)
        return scores['compound']
    else:
        return None
    
the_data['vader'] = the_data['body'].apply(get_vader_score)


# simple_senti
mean_simple_senti = the_data['simple_senti'].mean()
median_simple_senti = the_data['simple_senti'].median()
std_dev_simple_senti = the_data['simple_senti'].std()

# vader
mean_vader = the_data['vader'].mean()
median_vader = the_data['vader'].median()
std_dev_vader = the_data['vader'].std()

# result
print('Simple Senti Statistics:')
print(f'Mean: {mean_simple_senti}')
print(f'Median: {median_simple_senti}')
print(f'Standard Deviation: {std_dev_simple_senti}')

print('\nVader Statistics:')
print(f'Mean: {mean_vader}')
print(f'Median: {median_vader}')
print(f'Standard Deviation: {std_dev_vader}')


the_data.to_excel('output_file.xlsx', index=True)