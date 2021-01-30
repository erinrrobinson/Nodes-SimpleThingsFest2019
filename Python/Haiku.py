import tweepy
import re
from datetime import datetime, timedelta
import markovify
import sylco
from re import search


class Haiku:
    ACCESS_TOKEN = "ACCESS_TOKEN"
    ACCESS_TOKEN_SECRET = "ACCESS_TOKEN_SECRET"
    CONSUMER_KEY = "CONSUMER_KEY"
    CONSUMER_SECRET = "CONSUMER_SECRET"

    Twitter_Search_Timeout = 10

    TextFile = "Haiku-Text"
    Haiku = ""

    def __init__(self, search_word, error_timeout):
        self.Start = datetime.now()
        self.SearchWord = search_word
        self.Error_Timeout = error_timeout
        self.auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        self.auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

        # Get initial block of Twitter text and remove unwanted charactes
        self.get_twitter_text()

        # Generate the Haiku
        self.generate_haiku()
        test = 1

    def get_twitter_text(self):

        self.SearchWord = self.SearchWord.lower()
        file = open(self.TextFile, "w")
        tweet_count = 0
        for tweet in tweepy.Cursor(self.api.search, q=self.SearchWord + " -filter:retweets", count=400,
                                   lang="en",
                                   since="2018-06-01").items():
            tweet = self.regex_tweet(tweet.text)
            file.write(tweet)
            tweet_count += 1
            # Break condition
            if datetime.now() - self.Start > timedelta(seconds=self.Twitter_Search_Timeout):
                break
        file.close()

    def regex_tweet(self, tweet_text):

        tweet = ''.join(tweet_text)
        tweet = re.sub(r'\w+…\s?', '', tweet)
        tweet = re.sub('&', '', tweet)
        tweet = re.sub('"', '', tweet)
        tweet = re.sub('\.\.\.', '', tweet)
        tweet = re.sub('#', '', tweet)
        tweet = re.sub('(RT|"|amp;)', '', tweet)
        tweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet)  # Remove URL
        tweet = re.sub(r'@\w+', '', tweet)
        tweet = tweet.lower()

        return tweet

    def generate_haiku(self):

        all_text = ""
        with open(self.TextFile) as f:
            all_text += f.read()
        if all_text == '': # If empty
            self.return_error_haiku()
            return
        else:
            text_model = markovify.Text(all_text)

        # First Line
        print("Generating First Line...")
        first = None
        while first is None or sylco.getsyls(first) != 5:
            first = text_model.make_short_sentence(
                5 * 6,
                tries=1,
                max_overlap_ratio=0.8,
                max_overlap_total=50
            )
            # Break condition
            if datetime.now() - self.Start > timedelta(seconds=self.Error_Timeout):
                self.return_error_haiku()
                return
        print(first)

        # Second Line
        print("Generating Second Line...")
        second = None
        while second is None or sylco.getsyls(second) != 7:
            second = text_model.make_short_sentence(
                7 * 6,
                tries=1,
                max_overlap_ratio=0.8,
                max_overlap_total=50,
            )
            if second is None:
                continue
            second = second.lower()
            # Break condition
            if datetime.now() - self.Start > timedelta(seconds=self.Error_Timeout):
                self.return_error_haiku()
                return
            if search(self.SearchWord, second):
                break

        # Third Line
        print("Generating Third Line...")
        third = None
        while third is None or third == first or sylco.getsyls(third) != 5:
            third = text_model.make_short_sentence(
                5 * 6,
                tries=1,
                max_overlap_ratio=0.8,
                max_overlap_total=50,
            )
            # Break condition
            if datetime.now() - self.Start > timedelta(seconds=self.Error_Timeout):
                self.return_error_haiku()
                return

        self.Haiku = "".join([first, "\n", second, "\n", third])
        self.Haiku = "".join(c for c in self.Haiku if c not in ('.',':',';'))

    def display_haiku(self):
        if self.Haiku is None:
            print("No Haiku available...")

        print("")
        print("***********************")
        print("-----------------------")
        print(self.Haiku)
        print("-----------------------")
        print("***********************")
        return self.Haiku

    def return_error_haiku(self):

        first = "This is an error"
        second = "You've done something really wrong"
        third = "Couldn't get haiku"

        self.Haiku = "".join([first, "\n", second, "\n", third])
        self.Haiku = "".join(c for c in self.Haiku if c not in ('.',':',';'))

        print('Error: unable to retrieve line - timeout')