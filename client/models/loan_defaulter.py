import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn import model_selection
import torch
from .model import Model

import matplotlib.pyplot as plt


losses = [[0,0]]
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, line2 = ax.plot(losses)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
ax.set_ylim(0, 1)
ax.legend(['Train Loss', 'Validation Loss'])
        


class LoanDefaulterModel(Model):

    def __init__(self, node_hash=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = self.get_loan_defaulter_data(node_hash)
        self.X_train, self.X_valid, self.y_train, self.y_valid = self.train_test_split(self.data)
        self.model = torch.nn.Sequential(
                torch.nn.Linear(self.X_train.shape[1], 100),
                torch.nn.ReLU(),
                torch.nn.Linear(100, 50),
                torch.nn.ReLU(),
                torch.nn.Linear(50, 1),
                torch.nn.Sigmoid()
            )
        
        try:
            with open('model_state_dict.pth', 'rb') as f:
                #file = 'io.BytesIO(f.read())'
                file = 'model_state_dict.pth'
        except FileNotFoundError:
            file = None
        if file:
            self.model.load_state_dict(torch.load(file))
            
        
    def get_loan_defaulter_data(node_hash: int):
        all_data = pd.read_csv('data/loan_data.csv')
        return all_data.sample(10000, random_state=node_hash)

    def process_data(self, data):
        # # drop columns with more than 50% missing values
        # data = data.dropna(thresh=0.5*len(data), axis=1)

        # delete categorical columns
        data = data.select_dtypes(exclude=['object'])

        # convert all columns to float
        data = data.astype(float)

        return data
    def set_state_dict_path(self, path):
        self.state_dict_path = path
    def train_test_split(self, data):
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

        X_train, X_valid, y_train, y_valid = model_selection.train_test_split(X, y, test_size=0.2, random_state=42)
    
            # convert data to tensors
        X_train_tensor = torch.from_numpy(X_train).float()
        y_train_tensor = torch.squeeze(torch.from_numpy(y_train.to_numpy()).float())

        X_valid_tensor = torch.from_numpy(X_valid).float()
        y_valid_tensor = torch.squeeze(torch.from_numpy(y_valid.to_numpy()).float())
        return X_train_tensor, X_valid_tensor, y_train_tensor, y_valid_tensor
    def train(self):
        # define loss function and optimizer
        criterion = torch.nn.BCELoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.01)

        # train 1 epoch, in batches of 10
        epochs = 20
        batch_size = 200
        grads = {name: 0 for name, param in self.model.named_parameters()}
        for epoch in range(epochs):
            for i in range(0, len(self.X_train), batch_size):
                X_batch = self.X_train[i:i+batch_size]
                y_batch = self.y_train[i:i+batch_size]
                y_pred = self.model(X_batch).squeeze()
                loss = criterion(y_pred, y_batch)
                optimizer.zero_grad()
                loss.backward()
                for name, param in self.model.named_parameters():
                    grads[name] += param.grad
                optimizer.step()
                #print(grads['0.bias'])
            print('Epoch {}, Loss: {}'.format(epoch, loss.item()))

            # validation loss
            with torch.no_grad():
                y_pred = self.model(self.X_valid).squeeze()
                valid_loss = criterion(y_pred, self.y_valid)
                print('Epoch {}, Validation Loss: {}'.format(epoch, valid_loss.item()))


            losses.append([loss.item(), valid_loss.item()])

            ax.set_xlim(0, len(losses))
            line1.set_xdata(range(len(losses)))
            line1.set_ydata([loss[0] for loss in losses])
            line2.set_xdata(range(len(losses)))
            line2.set_ydata([loss[1] for loss in losses])
            fig.canvas.draw()
            fig.canvas.flush_events()

            #plt.plot(losses)
        self.save()
        return
    def save(self):
        torch.save(self.model.state_dict(), 'model_state_dict.pth')
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

