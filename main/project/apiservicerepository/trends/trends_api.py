from ast import And
import calendar
from concurrent.futures import process
from datetime import datetime, timedelta
import time
from typing import List

import requests
import collections
from project.apiservicerepository.trends.model import Trend

from project.db.models.trends import MainUsers, Trends, TwitterSearchTweets, MainTrends, TwitterUserTweets, MainUserTweets, MainTrendTweets, MainTrendTweetAnalized, MainUserTweetAnalized, MainUserAnalized, MainUserAnalizedScore
from project.util.customMessages import CustomMessages

from project.db.db import session

from tabulate import tabulate

import uuid

class TrendsAPI:
    
    @staticmethod
    def get_tweets_by_trends(select_trends):
        
        return True
    
    @staticmethod
    def show_trends_by_days():
        trends_result = session.query(Trends).all()
        session.close()
        trend_names = []
        
        trend_records = []
        
        # Identify the trends words
        for trend_result in trends_result:
            rank: int = 0
            for json_trend in trend_result.response:
                rank += 1
                trend = Trend(**json_trend)
                
                #if trend.name not in trend_names:
                trend_names.append(trend.name)
                
                trend_records.append({
                    #'country': trend_result.country,
                    'date': trend_result.query_params['date'],
                    'hour': trend_result.query_params['hour'],
                    'rank': rank,
                    'name': trend.name,
                    'tweet_volume': trend.tweet_volume
                })
                
        table_trends_str = tabulate(trend_records,headers="keys",tablefmt="html")
        
        filename = str(uuid.uuid4())
        
        with open(f"{filename}.xls", "w", encoding="utf-8") as text_file:
            text_file.write(table_trends_str)
            CustomMessages.ok_green(f"Archivo creado: {filename}.xls")
        
        #trend_search = [item for item in trend_records if item['name'] in ['#5MPeru','TERRORISMO','Chotano']]
                
        #print(tabulate(trend_search,headers="keys"))
        #counter = collections.Counter(trend_names)
        #print(trend_names.__len__())
        #print(counter.most_common(20))        
        #print(list(counter.keys()))
    
    @staticmethod
    def get_all_trends():
        trends_result = session.query(Trends).all()
        trend_names = []
        
        session.close()
        
        for trend_result in trends_result:
            for json_trend in trend_result.response:
                trend = Trend(**json_trend)
                
                if trend.name not in trend_names:
                    trend_names.append(trend.name)
        
        return trend_names
    
    @staticmethod    
    def get_trends_by_days(country: str):
        try:
            url = f"https://api.exportdata.io/trends/locations/{country}"
            base = datetime.utcnow()
            ## Rango 7 días
            date_list = [base - timedelta(hours=x) for x in range(8*24)]
            
            for date in date_list:
                date_str = date.strftime("%Y-%m-%d")
                hour = date.strftime("%H")
                
                params = {
                    'date': date_str,
                    'hour': hour
                }
                
                response = requests.get(url, params)
            
                record = Trends(country, params, response.json())
                session.add(record)
                session.commit()
                session.close()
                
                CustomMessages.ok_green(f"* Guardar en BD Tendencias de UTC {date_str} {hour} horas ({country.upper()}) ... OK")
                time.sleep(2)
                
            return True
        except:  # Noncompliant
            CustomMessages.fail("Sucedió un error, al obtener las tendencias del día. Favor de volver a intentarlo en un momento...")
            
            return False
    
    @staticmethod
    def get_all_users(keywords):
        
        twitter_search_tweets = []
        main_users = []
        if keywords == '':
            twitter_search_tweets = session.query(TwitterSearchTweets).all()  
            session.close()
        else: 
            twitter_search_tweets = session.query(TwitterSearchTweets).filter_by(load_keywords=keywords).all()
            main_users = session.query(MainUsers).filter_by(user_state='Actived').all()
            session.close()
            
        users_id = []
        
        for tweet_result in twitter_search_tweets:
            
            for data in tweet_result.response['data']:
                
                if data['author_id'] not in users_id:
                    
                    if main_users:
                        for main_user in main_users:
                            if data['author_id'] in main_user.id:
                                users_id.append(data['author_id'])
                    else:
                        users_id.append(data['author_id'])
            
        return users_id
    
    @staticmethod
    def json_tweets_to_table():
        
        main_trends = session.query(MainTrends).filter(MainTrends.processed != 1)
        # Migrar los tweets de la tendencia a un formato tabla
        for main_trend in main_trends:
            listTwitterSearchTweets = session.query(TwitterSearchTweets).filter_by(load_keywords=main_trend.trend).all()
            
            mainTrendTweets=[]
            
            for twitterSearchTweets in listTwitterSearchTweets:
                meta = twitterSearchTweets.response['meta']
                if meta['result_count'] > 0:
                    for data in twitterSearchTweets.response['data']:
                        record = MainTrendTweets(
                            user_id=data['author_id'], 
                            main_trend_id=main_trend.id, 
                            tweet_id=data['id'], 
                            tweet_text=data['text'], 
                            tweet_created_at=data['created_at'],
                            tweet_source=data['source'],
                            tweet_public_metrics_retweet_count=data['public_metrics']['retweet_count'],
                            tweet_public_metrics_reply_count=data['public_metrics']['reply_count'],
                            tweet_public_metrics_like_count=data['public_metrics']['like_count'],
                            tweet_public_metrics_quote_count=data['public_metrics']['quote_count']
                            )
                        mainTrendTweets.append(record)   
            
            if mainTrendTweets:
                session.bulk_save_objects(mainTrendTweets)
                session.commit()
            
            session.commit()
        
        # Migrar los tweets de los usuarios en un formato tabla
        
        for main_trend in main_trends:
            listTwitterUserTweets = session.query(TwitterUserTweets).filter_by(main_trend_id=main_trend.id).all()
            
            mainUserTweets=[]
            
            for twitterUserTweets in listTwitterUserTweets:
                meta = twitterUserTweets.response['meta']
                if meta['result_count'] > 0:
                    for data in twitterUserTweets.response['data']:
                        record = MainUserTweets(user_id=twitterUserTweets.user_id, main_trend_id=twitterUserTweets.main_trend_id, tweet_id=data['id'], tweet_text=data['text'], tweet_created_at=data['created_at'])
                        mainUserTweets.append(record)   
            
            if mainUserTweets:
                session.bulk_save_objects(mainUserTweets)
                session.commit()
                
        session.close()
        CustomMessages.ok_blue("Se finalizó la migración.")
            
    # @staticmethod
    def data_process():
        dt_utcnow = datetime.utcnow()
        main_trends = session.query(MainTrends).filter(MainTrends.processed != 1)
        
        # Evaluación de los tweets de las tendencias
        for main_trend in main_trends:
            mainTrendTweets = session.query(MainTrendTweets).filter_by(main_trend_id=main_trend.id).all()
            
            listMainTrendTweetAnalized=[]
            
            for mainTrendTweet in mainTrendTweets:
                # Identificar si es un retweet
                tweet_text = mainTrendTweet.tweet_text
                retweet_text = tweet_text[0:3]
                is_retweet = retweet_text == 'RT '
                # Obtener la hora e identificar si fue posteado en una hora anormal
                ## Variables de evaluación 22 horas hasta las 08 horas Perú
                ## convertir las horas de Perú a UTC
                begin_anormal_hour = 3
                end_anormal_hour = 13
                dt_tweet_created_at = datetime.strptime(mainTrendTweet.tweet_created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
                is_posted_anormal_hours = (begin_anormal_hour <= dt_tweet_created_at.hour < end_anormal_hour)
                
                record = MainTrendTweetAnalized(
                    main_trend_tweet_id = mainTrendTweet.id,
                    is_retweet = is_retweet,
                    is_posted_anormal_hours = is_posted_anormal_hours,
                    is_similar_another_tweets = 0,
                    year = dt_tweet_created_at.year,
                    month = dt_tweet_created_at.month,
                    day = dt_tweet_created_at.day,
                    hour = dt_tweet_created_at.hour,
                    minutes = dt_tweet_created_at.minute,
                    seconds = dt_tweet_created_at.second
                )
                
                listMainTrendTweetAnalized.append(record)
            
            
            if listMainTrendTweetAnalized:
                session.bulk_save_objects(listMainTrendTweetAnalized)
                session.commit()
        CustomMessages.ok_green(f"Finalizó el procesamiento de los tweets de las tendencias")
        
        # Evaluación de los tweets de los usuarios
        for main_trend in main_trends:
            mainUserTweets = session.query(MainUserTweets).filter_by(main_trend_id=main_trend.id).all()
            
            listMainUserTweetAnalized=[]
            
            for mainUserTweet in mainUserTweets:
                # Identificar si es un retweet
                tweet_text = mainUserTweet.tweet_text
                retweet_text = tweet_text[0:3]
                is_retweet = retweet_text == 'RT '
                # Obtener la hora e identificar si fue posteado en una hora anormal
                ## Variables de evaluación 22 horas hasta las 08 horas Perú
                ## convertir las horas de Perú a UTC
                begin_anormal_hour = 3
                end_anormal_hour = 13
                dt_tweet_created_at = datetime.strptime(mainUserTweet.tweet_created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
                is_posted_anormal_hours = (begin_anormal_hour <= dt_tweet_created_at.hour < end_anormal_hour)
                
                record = MainUserTweetAnalized(
                    main_user_tweet_id = mainUserTweet.id,
                    is_retweet = is_retweet,
                    is_posted_anormal_hours = is_posted_anormal_hours,
                    is_similar_another_tweets = 0,
                    year = dt_tweet_created_at.year,
                    month = dt_tweet_created_at.month,
                    day = dt_tweet_created_at.day,
                    hour = dt_tweet_created_at.hour,
                    minutes = dt_tweet_created_at.minute,
                    seconds = dt_tweet_created_at.second
                )
                
                listMainUserTweetAnalized.append(record)
            
            
            if listMainUserTweetAnalized:
                session.bulk_save_objects(listMainUserTweetAnalized)
                session.commit()
        CustomMessages.ok_green(f"Finalizó el procesamiento de los tweets de los usuarios")
        
        # Evaluación de los usuarios recolectados
        mainUsers = session.query(MainUsers).all()
        
        listMainUserAnalized=[]
        
        for mainUser in mainUsers:
            # ¿Es relativamente nuevo?
            ## Fecha de creacion menor a un mes
            dt_created_at = datetime.strptime(mainUser.created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
            num_months = (dt_utcnow.year - dt_created_at.year) * 12 + (dt_utcnow.month - dt_created_at.month)
            is_relative_new = (num_months <= 1)
            # ¿No tiene foto de perfil?
            default_profile_image='default_profile_normal.png'
            profile_image_url=mainUser.profile_image_url
            has_not_profile_picture = (default_profile_image in profile_image_url)
            # ¿No tienen biografía?
            description = mainUser.description
            has_no_bio_info = (description=='')
            # ¿Tiene bajo número de seguidores? 
            ## Número de seguidores menor a 200
            public_metrics_followers_count = mainUser.public_metrics_followers_count
            has_low_followers= (public_metrics_followers_count < 100)
            # ¿Número de tweets y retweets muy elevado?
            ## Promedio mayor a 200 tweets_retweets/día
            public_metrics_tweet_count= mainUser.public_metrics_tweet_count
            diff_dates = dt_utcnow-dt_created_at
            num_days= diff_dates.days
            has_high_tweet_retweet_number= ((public_metrics_tweet_count/num_days) > 200)
            # ¿Usualmente hace spam de retweets?
            ## Promedio mayor a 30 retweets/hora
            usually_spams_retweets= 0
            retweets_by_hour = session.execute(
                'Select user_id From( '+
                'Select mu.user_id, hour, count(1) count From main_user_tweets mu '+
                'inner join main_user_tweet_analized muta on mu.id = muta.main_user_tweet_id and muta.is_retweet = 1 '+
                'where mu.user_id=:user_id '+
                'group by mu.user_id, hour order by 3 desc'+
                ') where count > 30 group by user_id',
                {
                    'user_id':mainUser.id
                }
            )
            for retweets_by_hour_item in retweets_by_hour:
                usually_spams_retweets = 1
                break
            # ¿Tiene tweets en horarios irregulares?
            ## Rango de horas 20:01 y 07:59 horas
            has_tweets_in_anormal_hours= 0
            posted_anormal_hours = session.execute(
                'Select mu.user_id From main_user_tweets mu '+
                'inner join main_user_tweet_analized muta on mu.id = muta.main_user_tweet_id and muta.is_posted_anormal_hours = 1 '+
                'where mu.user_id=:user_id group by mu.user_id',
                {
                    'user_id':mainUser.id
                }
            )
            for posted_anormal_hour in posted_anormal_hours:
                has_tweets_in_anormal_hours = 1
                break
            
            record = MainUserAnalized(
                user_id = mainUser.id,
                is_relative_new = is_relative_new,
                has_not_profile_picture = has_not_profile_picture,
                has_no_bio_info = has_no_bio_info,
                has_low_followers = has_low_followers,
                has_high_tweet_retweet_number = has_high_tweet_retweet_number,
                usually_spams_retweets = usually_spams_retweets,
                has_tweets_in_anormal_hours = has_tweets_in_anormal_hours
            )
            
            listMainUserAnalized.append(record)
        
        CustomMessages.ok_green(f"Finalizó el procesamiento de los usuarios")
        
        if listMainUserAnalized:
            session.bulk_save_objects(listMainUserAnalized)
            session.commit()
                
        # Actualizar a procesadas las tendencias
        for main_trend in main_trends:
           main_trend.processed = True
           session.commit()
           
        CustomMessages.ok_green(f"Se actualizaron las tendencias a procesadas")
        
        session.close()
                
    # @staticmethod
    def data_analizer():
        list_main_user_analized = session.query(MainUserAnalized).all()
        
        listMainUserAnalizedScore = []
        
        for list_main_user_analized_item in list_main_user_analized:
            total_score = 0            
            total_score = 5 if list_main_user_analized_item.is_relative_new == 1 else 0
            total_score = total_score + (10 if list_main_user_analized_item.has_not_profile_picture == 1 else 0)
            total_score = total_score + (5 if list_main_user_analized_item.has_no_bio_info == 1 else 0)
            total_score = total_score + (20 if list_main_user_analized_item.has_low_followers == 1 else 0)
            total_score = total_score + (30 if list_main_user_analized_item.has_high_tweet_retweet_number == 1 else 0)
            total_score = total_score + (25 if list_main_user_analized_item.usually_spams_retweets == 1 else 0)
            total_score = total_score + (5 if list_main_user_analized_item.has_tweets_in_anormal_hours == 1 else 0)
            
            record = MainUserAnalizedScore(main_user_analized_id=list_main_user_analized_item.id, user_id=list_main_user_analized_item.user_id, total_score=total_score)
            listMainUserAnalizedScore.append(record)
        
        if listMainUserAnalizedScore:
            session.bulk_save_objects(listMainUserAnalizedScore)
            session.commit()
        
        CustomMessages.ok_green(f"Finalizó el análisis de los usuarios")
        
        trends_result = session.execute(
                "Select trend, CASE is_false WHEN 1 THEN 'Falso' ELSE 'Verdadero' END user_type, count(1) count " +
                "From( " +
                "Select mut.main_trend_id, mt.trend, mut.user_id, (muas.total_score >= 16 ) is_false From main_user_tweets mut " +
                "Inner Join main_trends mt on mt.id = mut.main_trend_id " +
                "Inner Join main_user_analized_score muas on mut.user_id = muas.user_id " +
                "group by mut.main_trend_id, mt.trend, mut.user_id, muas.total_score " +
                ") " +
                "group by main_trend_id, trend, is_false"
            )
        
        print(tabulate(trends_result,headers=["Tendencia"," Calificación Usuario"," Cantidad"]))
        
        CustomMessages.ok_green(f"Se generó el cuadro resumen de información")
        
        session.close()
            
    # @staticmethod
    def clean_data_base():
        session.execute('delete from main_trend_tweet_analized')
        session.execute('delete from main_trend_tweets ')
        session.execute('delete from main_trends ')
        session.execute('delete from main_user_analized ')
        session.execute('delete from main_user_analized_score ')
        session.execute('delete from main_user_tweet_analized ')
        session.execute('delete from main_user_tweets ')
        session.execute('delete from main_users ')
        session.execute('delete from trends ')
        session.execute('delete from twitter_search_tweets ')
        session.execute('delete from twitter_user_followers ')
        session.execute('delete from twitter_user_following ')
        session.execute('delete from twitter_user_tweets ')
        session.execute('delete from twitter_users ')
        session.commit()
        session.close()
    