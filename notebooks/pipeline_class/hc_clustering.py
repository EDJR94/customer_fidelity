import pandas as pd
from scipy.cluster import hierarchy as hc
from sklearn.base import BaseEstimator, TransformerMixin

class HierarchicalClustering(BaseEstimator, TransformerMixin):
    def __init__(self, k=5):
        self.k = k
    
    def fit(self, X, y=None):
        self.hc_model = hc.linkage(X, 'ward')
        return self
    
    def transform(self, X):
        labels_hc = hc.fcluster(self.hc_model, self.k, criterion='maxclust')
        return labels_hc