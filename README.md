# Bullying Detection in Tweets Using BERT

## Overview

This project leverages a fine-tuned BERT model for the classification of tweets, with a specific focus on detecting bullying and abusive language. By utilizing BERT's advanced natural language understanding capabilities, the model can effectively identify and categorize harmful content in tweets, contributing to a safer online environment.

## Features

### 1. **BERT-Based Tweet Classification**
- **What It Does:** The project uses a fine-tuned BERT model to classify tweets, identifying those that contain bullying or abusive language.
- **Why It’s Used:** BERT's ability to understand the context and nuances of language makes it highly effective for tasks like bullying detection, where subtle differences in wording can significantly alter the meaning.
- **How It Works:** The model processes input tweets and assigns them to predefined categories (e.g., bullying, non-bullying) based on the detected content.

### 2. **Fine-Tuned BERT Model**
- **What It Does:** The BERT model used in this project has been fine-tuned specifically for the task of bullying detection.
- **Why It’s Used:** Fine-tuning BERT on a specific dataset related to bullying enables the model to better recognize patterns and language that indicate harmful behavior.
- **How It Works:** The pre-trained BERT model is further trained on a dataset containing examples of bullying and non-bullying tweets, refining its ability to distinguish between the two.

### 3. **Detection and Categorization of Harmful Language**
- **What It Does:** The model not only detects bullying but also categorizes the type of harmful language, providing more granular insights into the nature of the abuse.
- **Why It’s Used:** Categorizing harmful language helps in understanding the severity and type of bullying, which is crucial for intervention and prevention strategies.
- **How It Works:** The model assigns tweets to specific categories of abuse based on the language used, such as insults, threats, or harassment.

## Installation and Setup

### 1. **Clone the Repository**
```bash
git clone https://github.com/AsawirShafiq/BERT-tweet-classification.git
cd BERT-tweet-classification
```
### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```
### 3. **Set up the environment**
- Ensure you have the necessary environment variables set up, including paths to your datasets and any required API keys.
### 4. **Install Dependencies**
- Option 1: Train the BERT model from scratch using the provided dataset:
```bash
python train_model.py

```
- Option 2: Load the pre-trained and fine-tuned model directly:
```bash
python load_model.py

```
### 5. **Run the classification Script**
```bash
python classify_tweets.py --input data/tweets.csv --output results.csv

```
