from sqlalchemy import Column, Integer, String, JSON, DateTime, Text, Boolean
from sqlalchemy.sql import func
from project.db import db

class Trends(db.Base):
    __tablename__ = 'trends'

    id = Column(Integer, primary_key=True)
    country = Column(String, nullable=False)
    query_params = Column(JSON, nullable=False)
    response = Column(JSON, nullable=False)

    def __init__(self, country, query_params, response):
        self.country = country
        self.query_params = query_params
        self.response = response
        
class TwitterSearchTweets(db.Base):
    __tablename__ = 'twitter_search_tweets'
    
    id = Column(Integer, primary_key=True)
    load_keywords = Column(Text, nullable=False)
    response = Column(JSON, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, load_keywords, response):
        self.load_keywords = load_keywords
        self.response = response
        
class TwitterUsers(db.Base):
    __tablename__ = 'twitter_users'

    id = Column(Integer, primary_key=True)
    users_id = Column(Text, nullable=False)
    response = Column(JSON, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, users_id, response):
        self.users_id = users_id
        self.response = response
        
class TwitterUserTweets(db.Base):
    __tablename__ = 'twitter_user_tweets'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    response = Column(JSON, nullable=False)
    main_trend_id = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, response, main_trend_id):
        self.user_id = user_id
        self.response = response
        self.main_trend_id = main_trend_id
        
class TwitterUserFollowers(db.Base):
    __tablename__ = 'twitter_user_followers'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    response = Column(JSON, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, response):
        self.user_id = user_id
        self.response = response
        
class TwitterUserFollowing(db.Base):
    __tablename__ = 'twitter_user_following'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    response = Column(JSON, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, response):
        self.user_id = user_id
        self.response = response

class MainTrends(db.Base):
    __tablename__ = 'main_trends'
    
    id = Column(Integer, primary_key=True)
    trend = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    newest_id = Column(String, nullable=False)
    oldest_id = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    processed = Column(Boolean, nullable=True)

    def __init__(self, trend, start_time, end_time, newest_id, oldest_id):
        self.trend = trend
        self.start_time = start_time
        self.end_time = end_time
        self.newest_id = newest_id
        self.oldest_id = oldest_id
        self.processed = False

class MainUsers(db.Base):
    __tablename__ = 'main_users'
    
    id = Column(String, primary_key=True)
    verified = Column(String, nullable=True)
    created_at = Column(String, nullable=True)
    username = Column(String, nullable=True)
    protected = Column(String, nullable=True)
    name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    profile_image_url = Column(String, nullable=True)
    public_metrics_followers_count = Column(Integer, nullable=True)
    public_metrics_following_count = Column(Integer, nullable=True)
    public_metrics_tweet_count = Column(Integer, nullable=True)
    public_metrics_listed_count = Column(Integer, nullable=True)
    user_error = Column(String, nullable=True)
    user_state = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, id, verified, created_at, username, protected, name, location, description, profile_image_url, public_metrics_followers_count, public_metrics_following_count, public_metrics_tweet_count, public_metrics_listed_count, user_error, user_state):
        self.id = id
        self.verified = verified
        self.created_at = created_at
        self.username = username
        self.protected = protected
        self.name = name
        self.location = location
        self.description = description
        self.profile_image_url = profile_image_url
        self.public_metrics_followers_count = public_metrics_followers_count
        self.public_metrics_following_count = public_metrics_following_count
        self.public_metrics_tweet_count = public_metrics_tweet_count
        self.public_metrics_listed_count = public_metrics_listed_count
        self.user_error = user_error
        self.user_state = user_state
    
    
class MainTrendTweets(db.Base):
    __tablename__ = 'main_trend_tweets'
    
    id = Column(Integer, primary_key=True)
    user_id= Column(String, nullable=True)
    main_trend_id= Column(Integer, nullable=True)
    tweet_id= Column(String, nullable=True)
    tweet_text= Column(String, nullable=True)
    tweet_created_at= Column(String, nullable=True)
    tweet_source= Column(String, nullable=True)
    tweet_public_metrics_retweet_count= Column(Integer, nullable=True)
    tweet_public_metrics_reply_count= Column(Integer, nullable=True)
    tweet_public_metrics_like_count= Column(Integer, nullable=True)
    tweet_public_metrics_quote_count= Column(Integer, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, main_trend_id, tweet_id, tweet_text, tweet_created_at, tweet_source, tweet_public_metrics_retweet_count, tweet_public_metrics_reply_count, tweet_public_metrics_like_count, tweet_public_metrics_quote_count):
        self.user_id = user_id
        self.main_trend_id = main_trend_id
        self.tweet_id = tweet_id
        self.tweet_text = tweet_text
        self.tweet_created_at = tweet_created_at
        self.tweet_source = tweet_source
        self.tweet_public_metrics_retweet_count = tweet_public_metrics_retweet_count
        self.tweet_public_metrics_reply_count = tweet_public_metrics_reply_count
        self.tweet_public_metrics_like_count = tweet_public_metrics_like_count
        self.tweet_public_metrics_quote_count = tweet_public_metrics_quote_count
        
class MainTrendTweetAnalized(db.Base):
    __tablename__ = 'main_trend_tweet_analized'
    
    id = Column(Integer, primary_key=True)
    main_trend_tweet_id= Column(Integer, nullable=True)
    is_retweet= Column(Integer, nullable=True)
    is_posted_anormal_hours= Column(String, nullable=True)
    is_similar_another_tweets= Column(String, nullable=True)
    year= Column(String, nullable=True)
    month= Column(String, nullable=True)
    day= Column(Integer, nullable=True)
    hour= Column(Integer, nullable=True)
    minutes= Column(Integer, nullable=True)
    seconds= Column(Integer, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, main_trend_tweet_id, is_retweet, is_posted_anormal_hours, is_similar_another_tweets, year, month, day, hour, minutes, seconds):
        self.main_trend_tweet_id = main_trend_tweet_id
        self.is_retweet = is_retweet
        self.is_posted_anormal_hours = is_posted_anormal_hours
        self.is_similar_another_tweets = is_similar_another_tweets
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minutes = minutes
        self.seconds = seconds
        
class MainUserTweets(db.Base):
    __tablename__ = 'main_user_tweets'
    
    id = Column(Integer, primary_key=True)
    user_id= Column(String, nullable=True)
    main_trend_id= Column(Integer, nullable=True)
    tweet_id= Column(String, nullable=True)
    tweet_text= Column(String, nullable=True)
    tweet_created_at= Column(String, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, main_trend_id, tweet_id, tweet_text, tweet_created_at):
        self.user_id = user_id
        self.main_trend_id = main_trend_id
        self.tweet_id = tweet_id
        self.tweet_text = tweet_text
        self.tweet_created_at = tweet_created_at
        
class MainUserTweetAnalized(db.Base):
    __tablename__ = 'main_user_tweet_analized'
    
    id = Column(Integer, primary_key=True)
    main_user_tweet_id= Column(Integer, nullable=True)
    is_retweet= Column(Integer, nullable=True)
    is_posted_anormal_hours= Column(String, nullable=True)
    is_similar_another_tweets= Column(String, nullable=True)
    year= Column(String, nullable=True)
    month= Column(String, nullable=True)
    day= Column(Integer, nullable=True)
    hour= Column(Integer, nullable=True)
    minutes= Column(Integer, nullable=True)
    seconds= Column(Integer, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, main_user_tweet_id, is_retweet, is_posted_anormal_hours, is_similar_another_tweets, year, month, day, hour, minutes, seconds):
        self.main_user_tweet_id = main_user_tweet_id
        self.is_retweet = is_retweet
        self.is_posted_anormal_hours = is_posted_anormal_hours
        self.is_similar_another_tweets = is_similar_another_tweets
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minutes = minutes
        self.seconds = seconds
        
        
class MainUserAnalized(db.Base):
    __tablename__ = 'main_user_analized'
    
    id = Column(Integer, primary_key=True)
    user_id= Column(String, nullable=True)
    is_relative_new= Column(Boolean, nullable=True)
    has_not_profile_picture= Column(Boolean, nullable=True)
    has_no_bio_info= Column(Boolean, nullable=True)
    has_low_followers= Column(Boolean, nullable=True)
    has_high_tweet_retweet_number= Column(Boolean, nullable=True)
    usually_spams_retweets= Column(Boolean, nullable=True)
    has_tweets_in_anormal_hours= Column(Boolean, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, user_id, is_relative_new, has_not_profile_picture, has_no_bio_info, has_low_followers, has_high_tweet_retweet_number, usually_spams_retweets, has_tweets_in_anormal_hours):
        self.user_id= user_id
        self.is_relative_new= is_relative_new
        self.has_not_profile_picture= has_not_profile_picture
        self.has_no_bio_info= has_no_bio_info
        self.has_low_followers= has_low_followers
        self.has_high_tweet_retweet_number= has_high_tweet_retweet_number
        self.usually_spams_retweets= usually_spams_retweets
        self.has_tweets_in_anormal_hours= has_tweets_in_anormal_hours
        
class MainUserAnalizedScore(db.Base):
    __tablename__ = 'main_user_analized_score'
    
    id = Column(Integer, primary_key=True)
    main_user_analized_id= Column(Integer, nullable=True)
    user_id= Column(String, nullable=True)
    total_score= Column(Integer, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, main_user_analized_id, user_id, total_score):
        self.main_user_analized_id= main_user_analized_id
        self.user_id= user_id
        self.total_score= total_score