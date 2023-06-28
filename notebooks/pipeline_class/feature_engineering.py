#Class for Pipeline Feature Engineering
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineering(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = self.feature_engineering(X)
        
        return X
    
    def feature_engineering(self, df):
        data = df.copy()
        
        #divide df in purchases and returns
        df_purchase = data.loc[data['quantity'] >=0, :]
        df_returns = data.loc[data['quantity'] < 0,:]
        
        #create df_ref
        df_ref = pd.DataFrame()

        ## 3.1 Monetary 

        #Monetary - O quanto cada cliente gera de $
        aux_monetary = pd.DataFrame()
        aux_monetary['valor_bruto'] = df_purchase['quantity'] * df_purchase['unit_price']
        aux_monetary['customer_id'] = df_purchase['customer_id']
        df_ref = aux_monetary.loc[:,['valor_bruto', 'customer_id']].groupby('customer_id').sum().reset_index().rename(columns={'valor_bruto':'monetary'})
        

        ## 3.2 Unique Products

        uniq_prod = (df_purchase.loc[:,['customer_id','stock_code']].groupby('customer_id')
                               .nunique()
                               .reset_index()
                               .rename(columns={'stock_code':'unique_prods'}))
        df_ref = pd.merge(df_ref, uniq_prod, on='customer_id', how='left')
        

        ## 3.3 Quantity of Products

        uniq_prod = (df_purchase.loc[:,['customer_id','stock_code']].groupby('customer_id')
                               .count()
                               .reset_index()
                               .rename(columns={'stock_code':'qt_prods'}))
        df_ref = pd.merge(df_ref, uniq_prod, on='customer_id', how='left')
        

        ## 3.4 Average Basket Size

        #qtd de produtos diferentes dentro de uma compora
        basket_size = (df_purchase.loc[:,['customer_id','stock_code','invoice_no']]
                                 .groupby(['customer_id'])
                                 .agg(
                                 number_buys = ('invoice_no', 'nunique'),
                                 number_prods = ('stock_code', 'count'))
                                 .reset_index())
        basket_size['avg_basket_size'] = basket_size['number_prods'] / basket_size['number_buys']
        basket_size = basket_size.drop(['number_prods','number_buys'], axis=1)
        df_ref = pd.merge(df_ref, basket_size, on='customer_id', how='left')
        

        ## 3.5 Recency

        #Recency
        aux_recency = df_purchase.loc[:,['customer_id','invoice_date']].groupby('customer_id').max().reset_index()
        date_max = df_purchase['invoice_date'].max()
        aux_recency['recency'] = (date_max - aux_recency['invoice_date']).dt.days
        df_ref = pd.merge(df_ref, aux_recency, on='customer_id', how='left')
        df_ref = df_ref.drop(['invoice_date'],axis=1)
        

        ## 3.6 Relationship Duration

        aux_min = df_purchase.loc[:,['customer_id', 'invoice_date']].groupby('customer_id').min().reset_index()
        aux_max = df_purchase.loc[:,['customer_id', 'invoice_date']].groupby('customer_id').max().reset_index()
        aux_relationship = aux_max.copy()
        aux_relationship['invoice_date'] = aux_max['invoice_date'].sub(aux_min['invoice_date']).dt.days
        aux_relationship = aux_relationship.rename(columns={'invoice_date':'relationship_duration'})
        df_ref = pd.merge(df_ref, aux_relationship, on='customer_id', how='left')
        

        ## 3.7 Purchase Count

        aux_invoice = df_purchase.loc[:,['invoice_no','customer_id']].drop_duplicates().groupby('customer_id').count().reset_index().rename(columns={'invoice_no':'purchase_count'})
        df_ref = pd.merge(df_ref, aux_invoice, on='customer_id', how='left')
        

        ## 3.8 Returns Count

        qtd_returns = df_returns.loc[:,['customer_id','quantity']].groupby('customer_id').sum().reset_index().rename(columns={'quantity':'returns_count'})
        qtd_returns['returns_count'] = qtd_returns['returns_count']*-1

        #merge
        df_ref = pd.merge(df_ref, qtd_returns, on='customer_id', how='left')

        #Os NaNs gerados são pessoas que não devolveram
        df_ref.loc[df_ref['returns_count'].isna(),'returns_count'] = 0
        

        ## 3.9 Monetary Return

        aux_monetary_return = pd.DataFrame()
        aux_monetary_return['valor_bruto'] = df_returns['quantity'] * df_returns['unit_price']
        aux_monetary_return['customer_id'] = df_returns['customer_id']
        aux_monetary_return = (aux_monetary_return.loc[:,['customer_id', 'valor_bruto']]
                                                .groupby('customer_id').sum()).reset_index()
        aux_monetary_return = aux_monetary_return.rename(columns={'valor_bruto':'monetary_returns'})

        #merge values
        df_ref = pd.merge(df_ref, aux_monetary_return, on='customer_id', how='left')
        df_ref.loc[df_ref['monetary_returns'].isna(),'monetary_returns'] = 0
        

        ## 3.10 Average Unit Price

        aux_unit_price = df_purchase.loc[:,['customer_id','unit_price']].groupby('customer_id').mean().reset_index().rename(columns={'unit_price':'avg_unit_price'})
        df_ref = pd.merge(df_ref, aux_unit_price, on='customer_id', how='left')
        

        ## 3.11 Return Rate

        df_ref['return_rate'] = df_ref['returns_count'] / df_ref['purchase_count']
        

        ## 3.12 Average Purchase Interval

        df_ref['avg_purchase_interval'] = df_ref.apply(lambda x: (x['purchase_count'] / x['relationship_duration']) if x['relationship_duration'] != 0 else x['relationship_duration'], axis=1)
        

        ## 3.13 Frequency

        df_ref['frequency'] = df_ref.apply(lambda x: (x['purchase_count'] / x['relationship_duration']) if x['relationship_duration'] != 0 else 0, axis=1)

        ## 3.15 Average Order Value

        df_ref['avg_order_value'] = df_ref.apply(lambda x: (x['monetary'] / x['purchase_count']) if x['purchase_count'] != 0 else x['monetary'], axis=1)
        

        return df_ref