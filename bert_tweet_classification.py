# -*- coding: utf-8 -*-
"""BERT_tweet classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RlErgUqdbbMYBUeSRRkWuVOfludnIkyG

# **BERT Implementation**
"""

import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from sklearn.preprocessing import LabelEncoder
df = pd.read_csv('cyberbullying_tweets.csv')

# Reduce the dataset size to 1000 samples as the full size is too big for current system to handle
df = df.sample(n=1000, random_state=42)

# Change the labeling to numerical values
label_encoder = LabelEncoder()
df['cyberbullying_type'] = label_encoder.fit_transform(df['cyberbullying_type'])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(df['tweet_text'], df['cyberbullying_type'], test_size=0.2, random_state=42)

# Ensure y_train and y_test are numpy arrays before converting to tensors as the .tensor fucntion expects lists, numpys or other tensors
y_train = np.array(y_train)
y_test = np.array(y_test)

# Convert labels to tensors of type Long as many of loss fucntions such as CrossEntropyLoss require tensor of long type
y_train = torch.tensor(y_train).long()
y_test = torch.tensor(y_test).long()

# Load DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=len(df['cyberbullying_type'].unique()))

# Tokenize input texts
def tokenize(batch):

    #PAdding set to true will make all the sequences to same length
    #Trancates sequences longer than max_length which was 512 to same length.
    #pt sets that tokenized outputs should be returned as Pytorch tensors.
    return tokenizer(batch, padding=True, truncation=True, max_length=512, return_tensors='pt')

#Converting to list it is suitable to be tokenzied
train_encodings = tokenize(X_train.tolist())
test_encodings = tokenize(X_test.tolist())

# Create PyTorch datasets for handling input encodings and labels.
class CyberbullyingDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = CyberbullyingDataset(train_encodings, y_train)
test_dataset = CyberbullyingDataset(test_encodings, y_test)

# DataLoader
#shuffle is set to True, so that data is shuffled before each epoch for a more generalized model.
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=8, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=8, shuffle=False)

# Define optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

model.train()
epochs = 3
losses = []
for epoch in range(epochs):
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        inputs = {key: val.to(model.device) for key, val in batch.items()}
        outputs = model(**inputs)
        # outputs.loss is CrossEntropyLoss inside BERT

        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
        print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss} ')

#Plot the loss function
plt.figure(figsize=(10, 6))
plt.plot(range(1, epochs + 1), losses, marker='o', linestyle='-', color='b')
plt.title('Training Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.grid(True)
plt.show()

#Finding out metrics such as accuracy, recall, precision and f1 score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

model.eval()

y_preds = []
y_true = []

with torch.no_grad():
    for batch in test_loader:
        inputs = {key: val.to(model.device) for key, val in batch.items()}
        outputs = model(**inputs)
        logits = outputs.logits
        preds = torch.argmax(logits, dim=1)
        y_preds.extend(preds.cpu().numpy())
        y_true.extend(batch['labels'].cpu().numpy())

y_preds = np.array(y_preds)
y_true = np.array(y_true)

num_classes = len(label_encoder.classes_)

accuracy = accuracy_score(y_true, y_preds)
precision = precision_score(y_true, y_preds, average='macro', labels=np.arange(num_classes))
recall = recall_score(y_true, y_preds, average='macro', labels=np.arange(num_classes))
f1 = f1_score(y_true, y_preds, average='macro', labels=np.arange(num_classes))

print(f'Accuracy: {accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1 Score: {f1:.4f}')

#Testing the model by giving out an example and seeing what we get as the output.
model.eval()
text = "A whale is the biggest animal on the planet"
inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors='pt').to(model.device)
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    preds = torch.argmax(logits, dim=1)
label = label_encoder.inverse_transform(preds.cpu().numpy())[0]
print(label)