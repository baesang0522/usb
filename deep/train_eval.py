import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from fc.fully_connect import SimpleNet, DropoutNet, BatchNormDoNet
from data_loader import prepare_dataset, TrainData, TestData
from config import config

Config = config["DEV"]
train_data, train_label, test_data = prepare_dataset(train_path=Config.TRAIN_PATH,
                                                     test_path=Config.TEST_PATH)
X_train, X_test, y_train, y_test = train_test_split(train_data, train_label, test_size=0.1)
train_tensor = TrainData(torch.FloatTensor(X_train.values),
                         torch.FloatTensor(y_train.values))
test_tensor = TestData(torch.FloatTensor(X_test.values))

train_loader = DataLoader(dataset=train_tensor, batch_size=Config.BATCH_SIZE, shuffle=True)
test_loader = DataLoader(dataset=test_tensor, batch_size=1)

model = SimpleNet().to(Config.DEVICE)
# model = DropoutNet().to(Config.DEVICE)
# model = BatchNormDoNet().to(Config.DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = nn.BCEWithLogitsLoss()


def binary_acc(y_pred, y_test):
    y_pred_tag = torch.round(torch.sigmoid(y_pred))
    correct_results_sum = (y_pred_tag == y_test).sum().float()
    acc = correct_results_sum/y_test.shape[0]
    acc = torch.round(acc * 100)

    return acc


def train_model():
    model.train()
    for e in range(1, Config.EPOCHS+1):
        epoch_loss = 0
        epoch_acc = 0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(Config.DEVICE), y_batch.to(Config.DEVICE)
            optimizer.zero_grad()

            y_pred = model(X_batch)

            loss = criterion(y_pred, y_batch)
            acc = binary_acc(y_pred, y_batch)

            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            epoch_acc += acc.item()

        print(f'Epoch {e+0:03}: | Loss: {epoch_loss/len(train_loader):.5f} | Acc: {epoch_acc/len(train_loader):.3f}')


def model_eval():
    y_pred_list = []
    model.eval()
    with torch.no_grad():
        for X_batch in test_loader:
            X_batch = X_batch.to(Config.DEVICE)
            y_test_pred = model(X_batch)
            y_pred_tag = torch.round(torch.sigmoid(y_test_pred))
            y_pred_list.append(y_pred_tag.cpu().numpy())
    y_pred_list = [a.squeeze().tolist() for a in y_pred_list]
    accuracy = accuracy_score(y_test, y_pred_list)
    print(f'Test Acc: {accuracy*100:.3f}')
