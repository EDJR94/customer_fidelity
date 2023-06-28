#Class for Pipeline TreeBased Model
import umap
import numpy          as np
import pandas         as pd
import sklearn.ensemble as en
from sklearn.base     import BaseEstimator, TransformerMixin

class TreeEmbedding(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = self.tree_embedding(X)
        
        return X
    
    def tree_embedding(self, df):
        data = df.copy()
        
        X = data.drop('monetary', axis=1).copy()
        y = data['monetary'].copy()
        
        #model definition
        rf = en.RandomForestRegressor(random_state=42, n_estimators=100, criterion='squared_error')

        rf.fit(X, y)
       
        #create leafs
        df_leafs = pd.DataFrame(rf.apply(X))
        
        #UMAP Reducer
        reducer = umap.UMAP(random_state=42, n_neighbors=120, min_dist=0.015)
        embedding = reducer.fit_transform(df_leafs)

        #embedding
        df_tree = pd.DataFrame()
        df_tree['embedding_x'] = embedding[:,0]
        df_tree['embedding_y'] = embedding[:,1]

        return df_tree