import re
import nltk

import numpy as np
# Uncomment to download "stopwords"
# nltk.download("stopwords")
from nltk.corpus import stopwords
from sklearn.model_selection import StratifiedKFold, cross_val_score

def text_preprocessing(s: str) -> str:
    """This function removes stop words, most punctionution and special 
    charecters and reduces the case.  Specifically:

    - Change "'t" to "not"
    - Remove "@name" < - not needed.
    - Isolate and remove punctuations except "?"
    - Remove other special characters
    - Remove stop words except "not" and "can"
    - Remove trailing whitespace   

    Returns:
        [str]: preprocessed sentence. 
    """    

    s = s.lower()
    # Change 't to 'not'
    s = re.sub(r"\'t", " not", s)
    # Remove @name
    s = re.sub(r'(@.*?)[\s]', ' ', s)
    # Isolate and remove punctuations except '?'
    s = re.sub(r'([\'\"\.\(\)\!\?\\\/\,])', r' \1 ', s)
    s = re.sub(r'[^\w\s\?]', ' ', s)
    # Remove some special characters
    s = re.sub(r'([\;\:\|•«\n])', ' ', s)
    # Remove stopwords except 'not' and 'can'
    s = " ".join([word for word in s.split()
                  if word not in stopwords.words('english')
                  or word in ['not', 'can']])
    # Remove trailing whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    
    return s


def get_auc_CV(model):
    """
    Return the average AUC score from cross-validation.
    """
    # Set KFold to shuffle data before the split
    kf = StratifiedKFold(5, shuffle=True, random_state=1)

    # Get AUC scores
    auc = cross_val_score(
        model, X_train_tfidf, y_train, scoring="roc_auc", cv=kf)

    return auc.mean()

def middle_selection(all_s:str, length:int, all_split:bool):
    if all_split == True:
        s = re.split("\W+", all_s)
    else:
        s = re.split("\s+", all_s)
    start = int(len(s)//2 - length/2)
    end = start+length
    separator = ' '
    new_s = separator.join(s[start:end])
    return new_s


def long_to_middle_bert(text_array:np.array, max_length:int, all_split=True) -> np.array:
    mid_doc_list = []
    for text_ in text_array:
        mid_doc_list.append(middle_selection(text_, max_length, all_split=all_split))
    return np.array(mid_doc_list)
