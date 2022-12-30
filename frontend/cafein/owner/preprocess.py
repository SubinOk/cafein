from kiwipiepy import Kiwi
from emoji import core
import pandas as pd
import re
import itertools

kiwi = Kiwi(model_type='sbg')

# 정규표현식 컴파일 
noun = re.compile(r'^N') # 명사형 태그
sp_char = re.compile(r'SW|SH') # 특수문자 태그

# 리뷰 문장 단위로 분리
def revToSent(review):
    tmp = []
    sentences = []
    preTag, preForm = '', ''
    sents = kiwi.split_into_sents(review, return_tokens=True)
    for sent in sents:
        toks = sent.tokens
        for tok in toks:

            if bool(sp_char.match(tok.tag)):
                preTag = tok.tag
                preForm = tok.form
                continue

            condition = (preTag == 'EC') and (preForm in ['고', '지만', '은데']) # 연결어미로 나눠지는 문장 분리
            if condition and bool(noun.match(tok.tag)):
                sentences.append(kiwi.join(tmp))
                tmp.clear()

            tmp.append(tok)
            preTag = tok.tag
            preForm = tok.form            
            
        connective = (preTag == 'EF') and (preForm in ['던데', '는데', '은데'])
        if not connective and len(tmp) > 0:
            sentences.append(kiwi.join(tmp))
            tmp.clear()
    
    return sentences

def processData(cafeName, data):

    kiwi.add_user_word('맛집', 'NNG', 0)
    kiwi.add_user_word('디카페인', 'NNG', 0)
    cafeName = cafeName.split(" ")[0]
    kiwi.add_user_word(cafeName, 'NNP', 0)

    preprocess = []

    for review in data['review']:
        review = core.replace_emoji(review, replace="")
        sents = revToSent(review)
        preprocess.append(sents)

    preprocess = list(itertools.chain(*preprocess))
    df = pd.DataFrame({'reviews': preprocess})

    return df