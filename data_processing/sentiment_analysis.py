# run the following line if you run it for the first time
# import nltk

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import time
import pickle
import re
import logging
from dotenv import load_dotenv
import os

# Setup default logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()

# Data Storage Area
Storage_Area = os.getenv("DATA_STORAGE")

# Define date range
start_date = "20241001"
end_date = "20241130"

# Directories
# # Used for analyzer validation
# comments_csv_dir = os.path.join(Storage_Area, f"sampled_{start_date}_{end_date}_comments_data.csv")
# vader_annotated_dir = os.path.join(Storage_Area, "vader_annotated", f"sampled_{start_date}_{end_date}_comments_data_annotated.csv")
# roberta_annotated_dir = os.path.join(Storage_Area, "roberta_annotated", f"sampled_{start_date}_{end_date}_comments_data_annotated.csv")

# Used for main analysis
batch = "batch_1"
comments_csv_dir = os.path.join(Storage_Area, "comments_data", f"{start_date}_{end_date}_comments_data_{batch}.csv")
roberta_annotated_dir = os.path.join(Storage_Area, "roberta_annotated", f"{start_date}_{end_date}_comments_data_annotated_{batch}.csv")

# run the following line if you run it for the first time
# nltk.download('vader_lexicon')

### Sentiment Analysis using VADER Lexicon ###
## Used for validation only, and is not used for main analysis, due to its quality.
#
# def sentiment_analysis_label(sentiment_value):
#     if sentiment_value >= 0.05:
#         label = "positive"
#     elif sentiment_value <= -0.05:
#         label = "negative"
#     else:
#         label = "neutral"
#     return label
#
# def sentiment_analysis_vader(text):
#     sentiment_value = SentimentIntensityAnalyzer().polarity_scores(text)['compound']
#     label = sentiment_analysis_label(sentiment_value)
#     return label
#
# df = pd.read_csv(comments_csv_dir)
# texts = df["text"]
# sentiment_label_list_vader = []
# for text in tqdm(texts):
#     text = str(text)
#     sentiment_label = sentiment_analysis_vader(text)
#     sentiment_label_list_vader.append(sentiment_label)
#
# df["sentiment_label"] = sentiment_label_list_vader
# df.to_csv(vader_annotated_dir)


### Sentiment Analysis using Twitter-roBERTa-base-sentiment-latest ###

model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"

sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)

def sentiment_analysis_roberta(text):
    sentiment = sentiment_task(text)[0]['label']
    return sentiment

df = pd.read_csv(comments_csv_dir)
texts = df["text"]
sentiment_value_list_roberta = []
for text in tqdm(texts):
    text = str(text)
    try:
        sentiment = sentiment_analysis_roberta(text)
    except RuntimeError as e:
        error_message = str(e)
        matches = re.findall(r'\((\d+)\)', error_message)
        if matches:
            try:
                expanded_size = int(matches[0])
                lentgh_text = len(text)
                shorter_length = int(lentgh_text * (500/expanded_size))
                shorter_text = text[:shorter_length]
                sentiment = sentiment_analysis_roberta(shorter_text)
            except Exception as e:
                sentiment = "ERROR"
                logging.warning("ERROR has occurred, sentiment = ERROR used")
    except Exception as e:
        sentiment = "ERROR"
        logging.warning("ERROR has occurred, sentiment = ERROR used")

    sentiment_value_list_roberta.append(sentiment)

    if len(sentiment_value_list_roberta) % 1000 == 0:
        filepath = open(os.path.join(Storage_Area, "sentiment_value_list_roberta.pkl"), "wb")
        pickle.dump(sentiment_value_list_roberta, filepath) # save analysis result per 1000 annotation for data backup

df["sentiment_value"] = sentiment_value_list_roberta
df.to_csv(roberta_annotated_dir)
