import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import torch
from .model import Model

import matplotlib.pyplot as plt


losses = []
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line, = ax.plot([0], [0], 'r-')
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
        

def get_loan_defaulter_data(node_hash: int):
    all_data = pd.read_csv('data/loan_data.csv')
    return all_data


class LoanDefaulterModel(Model):

    def __init__(self, data, pth_file_bytes, *args, **kwargs):
        self.data = data
        self.pth_file_bytes = pth_file_bytes
        super().__init__(*args, **kwargs)


    def process_data(self, data):
        # # drop columns with more than 50% missing values
        # data = data.dropna(thresh=0.5*len(data), axis=1)

        # delete categorical columns
        data = data.select_dtypes(exclude=['object'])

        # convert all columns to float
        data = data.astype(float)

        return data


    def train(self):
        print(f"data shape {self.data.shape[1]}")

        mergeddf_sample = self.process_data(self.data)

        print(f"Merged shape {mergeddf_sample.shape[1]}")

        # pipeline to drop na, impute missing values, filter by VIF, and normalize
        num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy="median")),
            ('std_scaler', StandardScaler()),
        ])

        # get features and labels. drop target column
        X = mergeddf_sample.drop(['TARGET'],axis=1)
        X = num_pipeline.fit_transform(X)

        print(f"X shape {X.shape[1]}")

        y = mergeddf_sample['TARGET']

        # if pth is provided, load weights from pth file bytes
        if self.pth_file_bytes is not None:
            model = torch.load(self.pth_file_bytes)
        else:
            model = torch.nn.Sequential(
                torch.nn.Linear(X.shape[1], 100),
                torch.nn.ReLU(),
                torch.nn.Linear(100, 50),
                torch.nn.ReLU(),
                torch.nn.Linear(50, 1),
                torch.nn.Sigmoid()
            )

        # define loss function and optimizer
        criterion = torch.nn.BCELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.00001)

        # convert data to tensors
        X_tensor = torch.from_numpy(X).float()
        y_tensor = torch.squeeze(torch.from_numpy(y.to_numpy()).float())

        # train 1 epoch, in batches of 10
        epochs = 10
        batch_size = 100
        for epoch in range(epochs):
            for i in range(0, len(X_tensor), batch_size):
                X_batch = X_tensor[i:i+batch_size]
                y_batch = y_tensor[i:i+batch_size]
                y_pred = model(X_batch).squeeze()
                loss = criterion(y_pred, y_batch)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            
            losses.append(loss.item())

            ax.set_xlim(0, len(losses))
            ax.set_ylim(0, max(losses))
            line.set_xdata(range(len(losses)))
            line.set_ydata(losses)
            fig.canvas.draw()
            fig.canvas.flush_events()

            print('Epoch {}, Loss: {}'.format(epoch, loss.item()))

        # return model weights
        return model


    def evaluate(self, state_dict):
        try:
            all_data = pd.read_csv('data/mergeddf_sample.csv')
        except FileNotFoundError:
            application_data = pd.read_csv('data/application_data.csv')
            previous_application = pd.read_csv('data/previous_application.csv')
            # columns_description = pd.read_csv(r'columns_description.csv',skiprows=1)

            mergeddf =  pd.merge(application_data,previous_application,on='SK_ID_CURR')
            all_data = mergeddf.sample(10000)
            # save mergeddf_sample to csv
            all_data.to_csv('data/mergeddf_sample.csv', index=False)


        mergeddf_sample = self.process_data(all_data)

        num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy="median")),
            ('std_scaler', StandardScaler()),
        ])

        X = mergeddf_sample.drop(['TARGET'],axis=1)
        X = num_pipeline.fit_transform(X)

        y = mergeddf_sample['TARGET']

        X_test_tensor = torch.from_numpy(X).float()
        y_test_tensor = torch.squeeze(torch.from_numpy(y.to_numpy()).float())
        model = torch.nn.Sequential(
            torch.nn.Linear(X.shape[1], 100),
            torch.nn.ReLU(),
            torch.nn.Linear(100, 50),
            torch.nn.ReLU(),
            torch.nn.Linear(50, 1),
            torch.nn.Sigmoid()
        )
        model.load_state_dict(state_dict)

        model.eval()
        y_pred = model(X_test_tensor).squeeze()
        y_pred = torch.round(y_pred)
        correct = torch.sum(y_pred == y_test_tensor)
        print('Accuracy: {}'.format(correct.item()/len(y_test_tensor)))

