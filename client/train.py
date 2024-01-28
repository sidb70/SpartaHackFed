import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

import torch

def train_model(state_dict=None):

    # if mergeddf_sample.csv does not exist, create it
    try:
        mergeddf_sample = pd.read_csv('mergeddf_sample.csv')
    except FileNotFoundError:
        application_data = pd.read_csv('application_data.csv')
        previous_application = pd.read_csv('previous_application.csv')
        # columns_description = pd.read_csv(r'columns_description.csv',skiprows=1)

        mergeddf =  pd.merge(application_data,previous_application,on='SK_ID_CURR')
        mergeddf_sample = mergeddf.sample(10000)
        # save mergeddf_sample to csv
        mergeddf_sample.to_csv('mergeddf_sample.csv', index=False)

    # mergeddf_sample = mergeddf_sample.sample(10000)

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


    model = torch.nn.Sequential(
        torch.nn.Linear(X_train.shape[1], 100),
        torch.nn.ReLU(),
        torch.nn.Linear(100, 50),
        torch.nn.ReLU(),
        torch.nn.Linear(50, 1),
        torch.nn.Sigmoid()
    )
    # if pth is provided, load weights from pth
    if state_dict is not None:
        print('Loading state_dict')
        model.load_state_dict(state_dict)

    # define loss function and optimizer
    criterion = torch.nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

    # convert data to tensors
    X_train_tensor = torch.from_numpy(X_train).float()
    y_train_tensor = torch.squeeze(torch.from_numpy(y_train.to_numpy()).float())

    # train model
    epochs = 10
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        # Forward pass
        y_pred = model(X_train_tensor).squeeze()
        # Compute Loss
        loss = criterion(y_pred, y_train_tensor)
        # Backward pass
        loss.backward()
        optimizer.step()
        print('Epoch {}: train loss: {}'.format(epoch, loss.item()))

    # calculate accuracy
    X_test_tensor = torch.from_numpy(X_test).float()
    y_test_tensor = torch.squeeze(torch.from_numpy(y_test.to_numpy()).float())

    model.eval()
    y_pred = model(X_test_tensor).squeeze()
    y_pred = torch.round(y_pred)
    correct = torch.sum(y_pred == y_test_tensor)
    print('Accuracy: {}'.format(correct.item()/len(y_test_tensor)))

    # return model weights
    return model.state_dict()



if __name__ == '__main__':
    # load state_dict from model.pth
    try:
        state_dict = torch.load('model.pth')
    except FileNotFoundError:
        state_dict = None
    result = train_model(state_dict)
    # save state_dict to json file
    torch.save(result, 'model.pth')
