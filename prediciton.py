import numpy as np
import pickle
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler

X = pd.DataFrame()
load_model = pickle.load(open('savemodel.sav', 'rb'))

def dataPreporcessing(df):
    #load the model 
   

    
    numerical_ix = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_ix = df.select_dtypes(include=['object', 'bool']).columns

    column_trans = ColumnTransformer(
    [('cat', OrdinalEncoder(),categorical_ix),
        ('num', MinMaxScaler(feature_range=(1, 3)), numerical_ix)],
        remainder='drop')
    column_trans.fit(df)
    # dump(column_trans,"models/column_trans.joblib")
    # %timeit joblib.dump(column_trans, 'models/column_trans.pkl', compress=1)
    df2 = column_trans.transform(df)
    df2 = pd.DataFrame(df2)


    df.isna().sum()

    mean_value=df2[2].mean()
    df2[2].fillna(value=mean_value, inplace=True)

    mean_value=df2[3].mean()
    df2[3].fillna(value=mean_value, inplace=True)

    mean_value=df2[4].mean()
    df2[4].fillna(value=mean_value, inplace=True)

    mean_value=df2[5].mean()
    df2[5].fillna(value=mean_value, inplace=True)
    mean_value=df2[6].mean()
    df2[6].fillna(value=mean_value, inplace=True)
    mean_value=df2[7].mean()
    df2[7].fillna(value=mean_value, inplace=True)
    # mean_value=df2[8].mean()
    # df2[8].fillna(value=mean_value, inplace=True)
    # df2.isna().sum()
    X=df2[[0,2,3,4,5,6, 7]] #Coloumns included are :- ip, request, Status, size, Referer.
    return df2

def prediciton(name):
    # print(X) 
    df = pd.read_csv("C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\prediction\\{}.csv".format(name))
    x = dataPreporcessing(df)  
    createCSV(x, "NumDataCSV")
    X=x[[0,2,3,4,5,6, 7]] #Coloumns included are :- ip, request, Status, size, Referer. 
    # load_model = pickle.load(open(filename,'rb'))
    load_model.predict(X)
    y_predict = load_model.predict(X)
    y_predict = pd.DataFrame(y_predict)
    y_predict.columns = ["Detected"]
    # y_predict
    outputDF=pd.concat([df, y_predict], axis=1)
    return outputDF

def createCSV(df, name):
    filePath = "C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\prediction\\{}.csv".format(name)
    df.to_csv(filePath, encoding='utf-8', index=False)
    return filePath
