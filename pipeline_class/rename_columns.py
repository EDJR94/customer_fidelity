#Class for Pipeline Rename columns
import pandas as pd
import inflection
from sklearn.base import BaseEstimator, TransformerMixin

class RenameColumns(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = self.rename_columns(X)
        
        return X
    
    def rename_columns(self, df):
        data = df.copy()
        
        data.columns = data.columns.map(lambda x: inflection.underscore(x))

        return data