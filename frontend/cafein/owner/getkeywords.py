import numpy as np
import pandas as pd
from kiwipiepy import Kiwi
from collections import Counter

kiwi = Kiwi(model_type='sbg')

nouns = ['NNG', 'NNP']
morphs = ['NNG', 'NNP', 'VV', 'VA', 'XR', 'SL']
verbs = ['VV', 'VA']
keywords = ['price', 'drink', 'dessert', 'service', 'customers', 'interior', 'view', 'parking', 'trash']

def getWords(data, top_n=20):
    morph_analysis = lambda x: kiwi.tokenize(x) if type(x) is str else None
    data['tokenized'] = data['reviews'].apply(morph_analysis)
    df = pd.DataFrame()
    
    for keyword in keywords:
        if keyword == 'trash':
            continue
        
        tmp = data.loc[data[keyword]==1]
        reviews_morphs = []

        for index, row in tmp.iterrows(): 
            if row['tokenized']:
                result_morphs = [(token.form, token.tag) for token in row['tokenized'] if token.tag in morphs]
                result_morphs = [form+"다" if tag in verbs else form for form, tag in result_morphs]
                reviews_morphs.extend(result_morphs)
        
        reviews_morphs_frequency = Counter(reviews_morphs)
        
        tags = []
        counts = []
        
        for tag, count in reviews_morphs_frequency.most_common(top_n):
            tags.append(tag)
            counts.append(count)

        if len(tags) < top_n:
            while len(tags) < top_n:
                tags.append(np.nan)
                counts.append(np.nan)
            
        df[f'{keyword}_word'] = tags
        df[f'{keyword}_count'] = counts
    
    return df