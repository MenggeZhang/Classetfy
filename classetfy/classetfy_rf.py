import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle

from classetfy import constants

def classify_with_rf(tag_frequencies):
    print(tag_frequencies)
    ret = {}
    fv = []
    for tag in constants.HTML_TAGS:
        fv.append(tag_frequencies[tag])
    # ML, load pkl file
    with open(constants.RF_MODEL_PATH, 'rb') as input:
        regr = pickle.load(input)
        y_pred = regr.predict([fv])[0]
    

    prob_customer = y_pred
    prob_internal = 1-y_pred
    ret['prob_customer'] = prob_customer
    ret['prob_internal'] = prob_internal
    return ret
