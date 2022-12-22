import numpy as np
import pandas as pd
from tqdm import tqdm
import tensorflow as tf
from transformers import BertTokenizer

max_seq_len = 128

def convert_examples_to_features(examples, labels, max_seq_len, tokenizer):
    
    input_ids, attention_masks, token_type_ids, data_labels = [], [], [], []
    
    for example, label in tqdm(zip(examples, labels), total=len(examples)):
        input_id = tokenizer.encode(example, max_length=max_seq_len, pad_to_max_length=True)
        padding_count = input_id.count(tokenizer.pad_token_id)
        attention_mask = [1] * (max_seq_len - padding_count) + [0] * padding_count
        token_type_id = [0] * max_seq_len

        assert len(input_id) == max_seq_len, "Error with input length {} vs {}".format(len(input_id), max_seq_len)
        assert len(attention_mask) == max_seq_len, "Error with attention mask length {} vs {}".format(len(attention_mask), max_seq_len)
        assert len(token_type_id) == max_seq_len, "Error with token type length {} vs {}".format(len(token_type_id), max_seq_len)

        input_ids.append(input_id)
        attention_masks.append(attention_mask)
        token_type_ids.append(token_type_id)
        data_labels.append(label)

    input_ids = np.array(input_ids, dtype=int)
    attention_masks = np.array(attention_masks, dtype=int)
    token_type_ids = np.array(token_type_ids, dtype=int)

    data_labels = np.asarray(data_labels, dtype=np.int32)

    return (input_ids, attention_masks, token_type_ids), data_labels


def prediction(df):
    df['y'] = 0

    tokenizer = BertTokenizer.from_pretrained('klue/bert-base')

    test_X, _ = convert_examples_to_features(df['reviews'], df['y'], max_seq_len=max_seq_len, tokenizer=tokenizer)
    
    sent_model = tf.keras.models.load_model('./modeling/nlp/model/sentimentBert')
    sent_pred = sent_model.predict(test_X)
    sent_pred = np.where(sent_pred>0.2, 1, 0).reshape(-1)

    keyword_model = tf.keras.models.load_model('./modeling/nlp/model/keywordBert')
    keyword_pred = keyword_model.predict(test_X)
    keyword_pred = np.where(keyword_pred>0.5, 1, 0)

    keywords = ['price', 'drink', 'dessert', 'service', 'customers', 'interior', 'view', 'parking', 'trash']
    tmp_1 = pd.DataFrame({'sentiment': sent_pred})
    tmp_2 = pd.DataFrame(keyword_pred, columns=keywords)

    result = pd.concat([df, tmp_1, tmp_2], axis=1)
    result.drop('y', axis=1, inplace=True)
    
    return result