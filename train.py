import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import pickle as pk

import joblib

from model import PimaClassifier

dataset = np.loadtxt("./data/pima-indians-diabetes.csv", delimiter=",")
x = dataset[:, 0:8]
y = dataset[:, 8]
x = torch.tensor(x, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

def add_noise(mean, std_dev):
    noise_x = np.random.normal(mean, std_dev, x_train.shape)
    noise_x = torch.tensor(noise_x, dtype=torch.float32)
    noise_y = np.random.randint(2, size=(len(y_train)))
    noise_y = torch.tensor(noise_y, dtype=torch.float32).reshape(-1, 1)
    augmented_x_train = torch.cat((x_train, noise_x))
    augmented_y_train = torch.cat((y_train, noise_y))
    augmented_x_train, augmented_y_train = shuffle(augmented_x_train, augmented_y_train)
    return augmented_x_train, augmented_y_train

accuracy_per_epoch = []
loss_per_epoch = []

def lossfn_optimizer(model, lr):
    loss_fn = nn.BCELoss()  # binary cross entropy
    optimizer = optim.Adam(model.parameters(), lr=lr)
    return optimizer, loss_fn


def train_model(n_epochs, batch_size, optimizer, loss_fn):
    for epoch in range(n_epochs):
        epoch_loss = 0
        epoch_accuracy = 0
        num_batches = len(augmented_x_train) // batch_size
        model.train()
        for i in range(0, len(augmented_x_train), batch_size):

            xbatch = augmented_x_train[i : i + batch_size]
            ybatch = augmented_y_train[i : i + batch_size]

            y_pred = model(xbatch)
            loss = loss_fn(y_pred, ybatch)
            accuracy = (y_pred.round() == ybatch).float().mean()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            epoch_accuracy += accuracy.item()

        avg_loss = epoch_loss / num_batches
        avg_accuracy = epoch_accuracy / num_batches
        loss_per_epoch.append(avg_loss)
        accuracy_per_epoch.append(avg_accuracy)
        print(
            f"Epoch {epoch}, Loss: {avg_loss:.4f}, Accuracy: {avg_accuracy * 100:.2f}%"
        )

    model.eval()
    y_pred = model(x_test).detach().numpy()
    y_pred = np.round(y_pred)
    test_accuracy = (y_pred == y_test.numpy()).mean()
    print(f"Test Accuracy: {test_accuracy:.4f}")
    return loss_per_epoch, accuracy_per_epoch, y_pred


if __name__ == "__main__":
    augmented_x_train, augmented_y_train = add_noise(mean=1, std_dev=0.5)
    model = PimaClassifier()
    n_epochs = 200
    batch_size = 10
    lr = 0.004
    optimizer, loss_fn = lossfn_optimizer(model=model, lr=lr)
    losses, accuracys, y_pred = train_model(
        n_epochs=n_epochs,
        batch_size=batch_size,
        optimizer=optimizer,
        loss_fn=loss_fn,
    )
    joblib.dump(model, "model.pkl")
    
    print("pickle file created!")
