import tensorflow as tf
import pandas as pd
import numpy as np
import os
import time
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from transformers import TFBertForSequenceClassification, BertTokenizer

# Load the Vietnamese BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

# Load the dataset
data = pd.read_csv('inputs.csv')

# Convert labels to one-hot encoding
labels = to_categorical(data['label'])

# Split the data into training and validation sets
train_texts, val_texts, train_labels, val_labels = train_test_split(data['Title'], labels, test_size=0.2, random_state=42)

# Tokenize the input texts
train_encodings = tokenizer(list(train_texts), truncation=True, padding=True)
val_encodings = tokenizer(list(val_texts), truncation=True, padding=True)

# Convert the input IDs and attention masks to NumPy arrays
train_input_ids = np.array(train_encodings['input_ids'])
train_attention_masks = np.array(train_encodings['attention_mask'])
val_input_ids = np.array(val_encodings['input_ids'])
val_attention_masks = np.array(val_encodings['attention_mask'])

model = TFBertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=2)

# Compile the model
optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08)
loss = tf.keras.losses.BinaryCrossentropy(from_logits=True)
metric = tf.keras.metrics.BinaryAccuracy('accuracy')
model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

# Set the output activation function to sigmoid
model.layers[-1].activation = tf.keras.activations.sigmoid

# # Train the model
# history = model.fit(
#     [train_input_ids, train_attention_masks],
#     train_labels,
#     epochs=3,
#     batch_size=2,
#     validation_data=([val_input_ids, val_attention_masks], val_labels)
# )
import matplotlib.pyplot as plt
num_samples = 3
# Save the trained model
# inputs = ["Vai trò, trách nhiệm của thanh niên trong bảo vệ nền tảng tư tưởng của Đảng", "Công an đập nhà, đánh dân tại Vườn Rau Lộc Hưng ở Sài Gòn"]
model.save_pretrained('vietnamese_bert_classification')
model = TFBertForSequenceClassification.from_pretrained('vietnamese_bert_classification')
outputs = model.predict([val_input_ids[:num_samples], val_attention_masks[:num_samples]])
predictions = tf.nn.softmax(outputs.logits, axis=1).numpy()
print(val_texts.head(num_samples))
for i in range(num_samples):
    print("Prediction:\t", predictions[i])
    print("True label:\t", val_labels[i])

# Plot the training and validation loss over epochs
# plt.plot(history.history['loss'], label='train_loss')
# plt.plot(history.history['val_loss'], label='val_loss')
# plt.title('Training and Validation Loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()

# # Plot the training and validation accuracy over epochs
# plt.plot(history.history['accuracy'], label='train_accuracy')
# plt.plot(history.history['val_accuracy'], label='val_accuracy')
# plt.title('Training and Validation Accuracy')
# plt.xlabel('Epochs')
# plt.ylabel('Accuracy')
# plt.legend()
# plt.show()