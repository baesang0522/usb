import pandas as pd
import torch
import numpy as np


class Config:
    TRAIN_PATH = 'train_data/train.csv'
    TEST_PATH = 'test_data/test.csv'
    LABEL = './test_data/test.csv'
    DROPOUT_RATIO = 0.3
    BATCH_SIZE = 32
    EPOCHS = 20
    # if torch.cuda.is_available():
    #     DEVICE = torch.device('cuda')
    # else:
    DEVICE = torch.device('cpu')


class DevConfig(Config):
    pass


class ProdConfig(Config):
    pass


config = {"DEV": DevConfig,
          "PROC": ProdConfig}

data = pd.read_csv('train_data/train.csv')
data = data.fillna(0)
