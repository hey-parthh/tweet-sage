import tweepy
import time
import random
import re
import json
import os

def run_scheduler():
    with open('config.json', 'r') as f:
        config=json.load(f)

    api_key = config["api_key"]
    api_secret = config["api_secret"]
    access_token = config["access_token"]
    access_token_secret = config["access_token_secret"]
    file_path = config["file_path"]
    time_interval = config["time_interval"]

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        exit()

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Read the content file
    with open(file_path, 'r') as file:
        text = file.readlines()

    # Function to select and post a tweet
    def post_tweet():
        # Select a random quote from the text file
        quote = random.choice(text).strip()
        tweet = re.split(r'(?<=[.,;])\s*', quote)
        final = "\n\n".join(part.strip() for part in tweet)

        try:
            client.create_tweet(text=final)
            print("Successfully posted:")
            print(final)
            return True  # Return True if tweet is posted successfully
        except tweepy.Forbidden as e:
            # If the error is due to a duplicate tweet, return False
            print("Duplicate tweet error:", e)
            return False
        except Exception as e:
            print("An error occurred", e)
            return False

    # Run the function to post a tweet every 7 hours
    while True:
        if post_tweet():
            time.sleep(time_interval)  # Sleep for 7 hours before posting the next tweet