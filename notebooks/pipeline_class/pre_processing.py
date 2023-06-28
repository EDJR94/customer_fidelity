#Class for Pipeline Preprocessing
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import sklearn.preprocessing as pp

class PreProcessing(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = self.pre_processing(X)
        
        return X
    
    def pre_processing(self, df):
        data = df.copy()
        
        data = data.drop('customer_id', axis=1).copy()
        
        #Transform
        mms = pp.MinMaxScaler()
        transf_list = data.columns

        for i in transf_list:
            data[i] = mms.fit_transform(data[i].values.reshape(-1,1))

        return data