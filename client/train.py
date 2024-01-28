import pickle
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

import torch


def train_model(pth_file):
    application_data = pd.read_csv('application_data.csv')
    previous_application = pd.read_csv('previous_application.csv')
    columns_description = pd.read_csv(r'columns_description.csv',skiprows=1)

    mergeddf =  pd.merge(application_data,previous_application,on='SK_ID_CURR')

    mergeddf_sample = mergeddf.sample(10000)

    # drop columns with more than 50% missing values
    mergeddf_sample = mergeddf_sample.dropna(thresh=0.5*len(mergeddf_sample), axis=1)

    # convert categorical columns to numerical
    mergeddf_sample = pd.get_dummies(mergeddf_sample)

    # convert all columns to float
    mergeddf_sample = mergeddf_sample.astype(float)

    # pipeline to drop na, impute missing values, filter by VIF, and normalize
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="median")),
        ('std_scaler', StandardScaler()),
    ])

    # get features and labels. drop target column
    X = mergeddf_sample.drop(['TARGET'],axis=1)
    X = num_pipeline.fit_transform(X)

    y = mergeddf_sample['TARGET']

    # train test split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.2,random_state=42)


    # if pth is provided, load weights from pth
    



    # run additional epochs 






