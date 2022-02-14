import pandas as pd
from config import config
from torch.utils.data import Dataset

Config = config["DEV"]


def prepare_dataset(train_path, test_path):
    t_data = pd.read_csv(train_path)
    t_data = t_data.fillna(0)
    train_data = t_data[['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']]
    train_label = t_data[['Survived']]
    test_data = pd.read_csv(test_path)
    test_data = test_data[['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']]

    return train_data, train_label, test_data


class TrainData(Dataset):
    def __init__(self, X_data, y_data):
        self.X_data = X_data
        self.y_data = y_data

    def __getitem__(self, index):
        return self.X_data[index], self.y_data[index]

    def __len__(self):
        return len(self.X_data)


class TestData(Dataset):
    def __init__(self, X_data):
        self.X_data = X_data

    def __getitem__(self, index):
        return self.X_data[index]

    def __len__(self):
        return len(self.X_data)

