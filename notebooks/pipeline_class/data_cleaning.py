#Class Data Cleaning
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class DataCleaning(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = self.data_cleaning(X)
        
        return X
        
    
    def data_cleaning(self, df):
        data = df.copy()
        
        #replace NaNs
        df_missing = data.loc[pd.isnull(data['customer_id']),:]

        #create reference
        df_backup = pd.DataFrame(df_missing['invoice_no'].drop_duplicates())
        df_backup['customer_id'] = np.arange(19000, 19000+len(df_backup),1)

        #merge
        data = pd.merge(data, df_backup, on='invoice_no', how='left')

        #coalesce - combina o que tem NaN em uma coluna com o que não tem em outra
        data['customer_id'] = data['customer_id_x'].combine_first(data['customer_id_y'])

        #drop extra columns
        data = data.drop(['customer_id_x','customer_id_y'], axis=1)
        
        #Change Types
        data['invoice_date'] = pd.to_datetime(data['invoice_date'])
        
        #Filter variables
        
        #unit_price
        data = data.loc[data['unit_price'] >= 0.040,:]

        #stock code
        data = data.loc[~data['stock_code'].isin(['POST', 'D', 'DOT', 'M', 'S', 'AMAZONFEE', 'm', 'DCGSSBOY',
               'DCGSSGIRL', 'PADS', 'B', 'CRUK']),:]

        #description
        data = data.drop('description', axis=1)

        #country
        data = data.loc[~data['country'].isin(['Unspecified','European Community']),:]

        #bad users

        data = data.loc[~data['customer_id'].isin([16446]),:]
        data = data.loc[~data['customer_id'].isin([12346]),:]
        
        #divide df in purchases and returns
        df_purchase = data.loc[data['quantity'] >=0, :]
        df_returns = data.loc[data['quantity'] < 0,:]


        return data