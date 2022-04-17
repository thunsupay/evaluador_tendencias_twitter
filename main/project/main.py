from datetime import datetime
import json
import os
import time
from attr import fields
from dotenv import load_dotenv
from pathlib import Path

from sqlalchemy import Integer, null
from project.apiservicerepository.trends.trends_api import TrendsAPI
from project.db.models.trends import TwitterUsers, TwitterUserTweets, TwitterUserFollowers, TwitterUserFollowing, TwitterSearchTweets, MainTrends, MainUsers
import tweepy
from project.models.project_models import CountryTrendsServiceType, MonthType

from project.util.customMessages import CustomMessages
from project.db.db import session

import re
regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
match_iso8601 = re.compile(regex).match

def validate_iso8601(str_val):
    try:            
        if match_iso8601( str_val ) is not None:
            return True
    except:
        pass
    return False

def validate_start_time_vs_end_time(start_time, end_time):
    start_time = datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.strptime(end_time,'%Y-%m-%dT%H:%M:%SZ')
    
    return end_time >= start_time
    

class Main:

    # Inicialización de la clase
    def __init__(self,path_env: str = ""):

        if path_env:
            CustomMessages.ok_blue(
                "Cargando variables de entorno desde archivo")
        else:
            CustomMessages.ok_blue("Cargando variables de entorno")

        if os.path.exists(path_env):
            dotenv_path = Path(path_env)
            load_dotenv(dotenv_path=dotenv_path)

        self.bearer_token = os.getenv('bearer_token')
        self.consumer_key = os.getenv('consumer_key')
        self.consumer_secret = os.getenv('consumer_secret')
        self.access_token = os.getenv('access_token')
        self.access_token_secret = os.getenv('access_token_secret')

        self.wait_on_rate_limit = os.getenv('wait_on_rate_limit') == 'true'

    # Verificar carga de variables de entorno
    def check_env_var(self,need_to_print: bool = False):
        if need_to_print:
            CustomMessages.ok_cyan("Método check_env_var")
            print(f"bearer_token: {self.bearer_token} ")
            print(f"consumer_key: {self.consumer_key} ")
            print(f"consumer_secret: {self.consumer_secret} ")
            print(f"access_token: {self.access_token} ")
            print(f"access_token_secret: {self.access_token_secret} ")
            print(f"wait_on_rate_limit: {self.wait_on_rate_limit} ")

        return self.bearer_token and (self.consumer_key or self.consumer_secret or self.access_token or self.access_token_secret or self.wait_on_rate_limit)

    # Obtener el cliente tweepy
    def get_tweepy_client(self):
        client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            wait_on_rate_limit=self.wait_on_rate_limit
        )
        
        CustomMessages.ok_cyan("* Cliente Tweepy ... OK")
        
        return client

    # La entrada deben ser 2 palabras o un hashtag relacionado
    # con la política peruana. Ejemplo: ["#VacanciaYa", "#Congreso87VotosYa", "#KarelimLopez", "Pedro Castillo"]
    def get_tweets_users_by_trends(self, list_trends):
        if self.check_env_var():
            # Cargando el cliente Twitter API 2.0
            client = self.get_tweepy_client()
            # Configurando para Devolver JSON
            client.return_type = dict
                
            tweet_fields = "author_id,created_at,public_metrics,text,referenced_tweets,id,source"
            # considerar otros datos para futuras investigaciones
            #expansions = "author_id,referenced_tweets.id,in_reply_to_user_id,geo.place_id,entities.mentions.username,referenced_tweets.id.author_id"
            #tweet_fields = "author_id,attachments,entities,geo,lang,conversation_id,created_at,public_metrics,source,text,reply_settings,referenced_tweets,id,context_annotations"
            #user_fields = "created_at,description,entities,id,location,name,pinned_tweet_id,protected,public_metrics,url,username,verified,withheld"
            #place_fields = "id,geo,full_name,country,country_code,name,place_type,contained_within"
            
            # parámetros:
            for i in range(len(list_trends)):
                #list_trends[i]['trend'] = f"({list_trends[i]['trend']} -is:retweet lang:es)"
                list_trends[i]['trend'] = f"({list_trends[i]['trend']} lang:es)"
                
            for trend in list_trends:
                query = trend['trend']
                
                # Orden recency | relevancy
                #sort_order = "relevancy"
                total_result = 1000
                
                next_token = ''
                
                while total_result > 0:
                    
                    max_results = 100
                    
                    if total_result > 100:
                        total_result = total_result - max_results
                    else:
                        max_results = total_result
                        total_result = 0

                    if next_token == '':
                        json_data = client.search_recent_tweets(
                            query=query,
                            max_results=max_results,
                            tweet_fields=tweet_fields,
                            start_time=trend['start_time'],
                            end_time=trend['end_time']
                            #sort_order=sort_order,
                            #expansions=expansions,
                            #user_fields=user_fields,
                            #place_fields=place_fields
                        )
                    else:
                        json_data = client.search_recent_tweets(
                            query=query,
                            max_results=max_results,
                            tweet_fields=tweet_fields,
                            next_token=next_token,
                            start_time=trend['start_time'],
                            end_time=trend['end_time']
                            #sort_order=sort_order,
                            #expansions=expansions,
                            #user_fields=user_fields,
                            #place_fields=place_fields
                        )

                    # Guardar en BD
                    record = TwitterSearchTweets(load_keywords=query, response=json_data)
                    session.add(record)
                    session.commit()
                    session.close()
                    
                    meta = json_data['meta']
                    next_token = meta['next_token'] if 'next_token' in meta else ''
                    
                    if next_token == '':
                        break
                
                # Preparando la búsqueda del id del tweet inicial y final de la búsqueda.
                twitter_search_tweets = session.query(TwitterSearchTweets).filter_by(load_keywords=query).all()
                session.close()
                
                meta_ids = []
                
                for twitter_search_tweets_item in twitter_search_tweets:
                    meta_ids.append(int(twitter_search_tweets_item.response['meta']['newest_id']))
                    meta_ids.append(int(twitter_search_tweets_item.response['meta']['oldest_id']))
                
                main_record = MainTrends(trend=query, start_time=trend['start_time'], end_time=trend['end_time'], newest_id=str(max(meta_ids)), oldest_id=str(min(meta_ids)))
                session.add(main_record)
                session.commit()
                session.close()
                
                CustomMessages.ok_green(f"Se recolectó y almacenó los tweets de la tendencia '{trend['trend']}' con el rango de fecha siguiente: '{trend['start_time']}' - '{trend['end_time']}' ")
        else:
            CustomMessages.warning('No tiene variables de entorno')
            
    def get_users_metadata(self, users_id):
        total_result = users_id.__len__()
        count_value = 0
        # Cargando el cliente Twitter API 2.0
        client = self.get_tweepy_client()
        # Configurando para Devolver JSON
        client.return_type = dict
        # Indicar metadata del usuario
        user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
        # Constante por defecto para el máximo número resultado de resultados en Twitter (max = 100)
        const_max_result = 100
        
        while total_result > 0:
            max_results = const_max_result
            users_selection = []
                
            if total_result > const_max_result:
                total_result = total_result - max_results
            else:
                max_results = total_result
                total_result = 0
                
            users_selection = users_id[const_max_result*count_value:(const_max_result*count_value) + max_results]
            
            # Obtener metada de un listado de usuarios
            json_data = client.get_users(
                ids = users_selection,
                user_fields = user_fields
            )
            
            count_value = count_value + 1
            
            record = TwitterUsers(users_id=",". join(users_selection), response=json_data)
            session.add(record)
            session.commit()
            session.close()
            
        # Preparando la búsqueda del id del tweet inicial y final de la búsqueda.
        twitter_users = session.query(TwitterUsers).all()
        
        for twitter_user in twitter_users:
            
            twitter_user_data = twitter_user.response['data']
            
            
            
            for data in twitter_user_data:
                if not session.query(MainUsers).filter_by(id=data['id']).scalar():
                    main_record = MainUsers(
                        id=data['id'], 
                        verified=data['verified'], 
                        created_at=data['created_at'], 
                        username=data['username'], 
                        protected=data['protected'], 
                        name=data['name'], 
                        location= data['location'] if 'location' in data else '',
                        description= str(data['description']), 
                        profile_image_url=data['profile_image_url'], 
                        public_metrics_followers_count=data['public_metrics']['followers_count'], 
                        public_metrics_following_count=data['public_metrics']['following_count'], 
                        public_metrics_tweet_count=data['public_metrics']['tweet_count'], 
                        public_metrics_listed_count=data['public_metrics']['listed_count'],
                        user_error='',
                        user_state='Actived')
                    session.add(main_record)
                    session.commit()
                else:
                    main_record_modify = session.query(MainUsers).filter_by(id=data['id']).first()
                    main_record_modify.verified='1' if data['verified'] == True else '0'
                    main_record_modify.created_at=data['created_at']
                    main_record_modify.username=data['username']
                    main_record_modify.protected='1' if data['protected'] == True else '0'
                    main_record_modify.name=data['name']
                    main_record_modify.location=data['location'] if 'location' in data else ''
                    main_record_modify.description= str(data['description']), 
                    main_record_modify.profile_image_url=data['profile_image_url']
                    main_record_modify.public_metrics_followers_count=data['public_metrics']['followers_count']
                    main_record_modify.public_metrics_following_count=data['public_metrics']['following_count']
                    main_record_modify.public_metrics_tweet_count=data['public_metrics']['tweet_count']
                    main_record_modify.public_metrics_listed_count=data['public_metrics']['listed_count']
                    main_record_modify.user_error=''
                    main_record_modify.user_state='Actived'
                
            twitter_user_errors = twitter_user.response['errors'] if hasattr(twitter_user.response, 'errors') else []
            
            for error in twitter_user_errors:
                
                if not session.query(MainUsers).filter_by(id=error['resource_id']).scalar():
                    main_record = MainUsers(
                        id=error['resource_id'], 
                        verified='0', 
                        created_at='', 
                        username='', 
                        protected='0', 
                        name='', 
                        location='', 
                        description= '',
                        profile_image_url='', 
                        public_metrics_followers_count=0, 
                        public_metrics_following_count=0, 
                        public_metrics_tweet_count=0, 
                        public_metrics_listed_count=0,
                        user_error=error['detail'] if hasattr(error, 'detail') else error['detail'],
                        user_state='Suspended')
                    session.add(main_record)
                    session.commit()
                else:
                    main_record_modify = session.query(MainUsers).filter_by(id=error['resource_id']).first()
                    main_record_modify.verified='0'
                    main_record_modify.created_at=''
                    main_record_modify.username=''
                    main_record_modify.protected='0'
                    main_record_modify.name=''
                    main_record_modify.location=''
                    main_record_modify.description= '',
                    main_record_modify.profile_image_url=''
                    main_record_modify.public_metrics_followers_count=0
                    main_record_modify.public_metrics_following_count=0
                    main_record_modify.public_metrics_tweet_count=0
                    main_record_modify.public_metrics_listed_count=0
                    main_record_modify.user_error=error['detail'] if hasattr(error, 'detail') else error['detail']
                    main_record_modify.user_state='Suspended'  
        
        session.close()
        CustomMessages.ok_green("Se recolectó y almacenó la metadata de los usuarios")

    def get_users_tweets(self, select_trends):
        # Cargando el cliente Twitter API 2.0
        client = self.get_tweepy_client()
        # Configurando para Devolver JSON
        client.return_type = dict
        # Indicar metadata del tweet
        tweet_fields="created_at,author_id"
        # Constante por defecto para el máximo número resultado de resultados en Twitter (max = 100)
        const_max_result = 100
        
        for select_trend in select_trends:
            
            trend = select_trend['trend']
            
            users_id = TrendsAPI.get_all_users(keywords=trend)
            
            main_trend = session.query(MainTrends).filter_by(trend=trend).first()
            session.close()
            
            for user_id in users_id:
                # Obtener metada de un listado de usuarios
                json_data = client.get_users_tweets(
                    id = user_id,
                    max_results=const_max_result,
                    since_id=main_trend.oldest_id,
                    until_id=main_trend.newest_id,
                    tweet_fields=tweet_fields
                )
                
                record = TwitterUserTweets(user_id=user_id, main_trend_id=main_trend.id, response=json_data)
                session.add(record)
                session.commit()
                session.close()
        
        CustomMessages.ok_green("Se recolectó y almacenó los tweets de los usuarios")

    def get_users_followers(self, users_id):
        # Cargando el cliente Twitter API 2.0
        client = self.get_tweepy_client()
        # Configurando para Devolver JSON
        client.return_type = dict
        # Constante por defecto para el máximo número resultado de resultados en Twitter (max = 1000)
        const_max_result = 1000
        
        for user_id in users_id:
            # Obtener metada de un listado de usuarios
            json_data = client.get_users_followers(
                id = user_id,
                max_results=const_max_result
            )
            
            record = TwitterUserFollowers(user_id=user_id, response=json_data)
            session.add(record)
            session.commit()
            session.close()
        
        CustomMessages.ok_green("Se recolectó y almacenó los seguidores de los usuarios")

    def get_users_following(self, users_id):
        # Cargando el cliente Twitter API 2.0
        client = self.get_tweepy_client()
        # Configurando para Devolver JSON
        client.return_type = dict
        # Constante por defecto para el máximo número resultado de resultados en Twitter (max = 1000)
        const_max_result = 1000
        
        for user_id in users_id:
            # Obtener metada de un listado de usuarios
            json_data = client.get_users_following(
                id = user_id,
                max_results=const_max_result
            )
            
            record = TwitterUserFollowing(user_id=user_id, response=json_data)
            session.add(record)
            session.commit()
            session.close()
            
        CustomMessages.ok_green("Se recolectó y almacenó los seguidos de los usuarios")
    
    # Identificación de tendencias
    def get_trends_by_days(self, country: str):
        CustomMessages.ok_cyan("Iniciando la descarga de tendencias")
        
        hasTrends = TrendsAPI.get_trends_by_days(country)
        
        CustomMessages.ok_cyan("Finalizando la descarga de tendencias")
        
        return hasTrends

    # Generar reporte con la data de las tendencias
    def show_trends_by_days(self):
        CustomMessages.ok_cyan("Iniciando la creación del excel de tendencias")
        
        TrendsAPI.show_trends_by_days()
        
        CustomMessages.ok_cyan("Finalizando la creación del excel de tendencias")
        
    def search_trend_list(self):
        CustomMessages.ok_cyan("Ingresar su selección de tendencias como en los siguientes ejemplos:")
        CustomMessages.ok_cyan("\U0001F449 tendencia_1, tendencia_2, tendencia_3")
        CustomMessages.ok_cyan("\U0001F449 tendencia_individual")
        # Validador de tendencias | mejora futura | búsqueda para validar que la tendencia exista en la base de datos
        # trend_names = TrendsAPI.get_all_trends()
        
        select_trends = []
        
        while True:
            words = input("Ingresar sus tendencias (enter para finalizar):")
            
            if words == '':
                break
            
            start_time = ''
            
            while start_time == '':
                start_time = input("Rango inicial YYYY-MM-DDTHH:mm:ssZ (obligatorio):")
                
                if not validate_iso8601(start_time):
                    CustomMessages.warning(f"El formato correcto es YYYY-MM-DDTHH:mm:ssZ.")
                    start_time = ''
            
            end_time = ''
            
            while end_time == '':
                end_time = input("Rango final YYYY-MM-DDTHH:mm:ssZ (obligatorio):")
                
                if not validate_iso8601(end_time):
                    CustomMessages.warning(f"El formato correcto es YYYY-MM-DDTHH:mm:ssZ.")
                    end_time = ''
                
                if not validate_start_time_vs_end_time(start_time, end_time):
                    CustomMessages.warning(f"El rango de fecha final siempre debe ser mayor o igual al rango de fecha inicial.")
                    end_time = ''
            
            trends = words.split(",")
            
            for trend in trends:
                trend = trend.strip()
                trend = trend.lower()
                data = {
                        "trend": trend, 
                        "start_time": start_time,
                        "end_time": end_time
                        }
                if data in select_trends:
                    CustomMessages.warning(f"Ya existe '{trend}' con el rango de fecha siguiente: '{start_time}' - '{end_time}' ")
                else:
                    select_trends.append(data)
                    CustomMessages.ok_green(f"Se seleccionó '{trend}' con el rango de fecha siguiente: '{start_time}' - '{end_time}' ")
                # Validador de tendencias | mejora futura | búsqueda para validar que la tendencia exista en la base de datos
                # elif item in trend_names:
                #     select_trends.append(item)
                #     CustomMessages.ok_green(f"'{item}' se seleccionó")
                # else:
                #     CustomMessages.warning(f"'{item}' no se encuentra entre las tendencias")
        
        if select_trends:
            
            condition = ''
            
            while True:
                condition = input("¿Desea continuar con la búsqueda de Tweets en Twitter? (S/N):")
                condition = condition.upper()
                if condition == 'S' or condition == 'N':
                    break
                
            if condition == 'S':
                CustomMessages.ok_blue("Iniciando búsqueda de tweets en Twitter.")
                self.get_tweets_users_by_trends(select_trends)
                
                CustomMessages.ok_blue("Iniciando búsqueda de la metadata de usuarios.")
                users_id = TrendsAPI.get_all_users(keywords='')
                main.get_users_metadata(users_id)
                
                CustomMessages.ok_blue("Iniciando búsqueda de tweets de usuarios.")
                main.get_users_tweets(select_trends)
                
                CustomMessages.ok_blue("Iniciando migración de los tweets en JSON a una tabla.")
                TrendsAPI.json_tweets_to_table()
                
                # Recolección de seguidos y seguidores se puede considerar en futuros trabajos.
                #CustomMessages.ok_blue("Iniciando búsqueda de seguidores del usuarios.")
                #CustomMessages.ok_green("Se recolectó y almacenó los seguidores de los usuarios")
                ##main.get_users_followers(users_id)
                #CustomMessages.ok_blue("Iniciando búsqueda de seguidos por el usuarios.")
                #CustomMessages.ok_green("Se recolectó y almacenó los seguidos de los usuarios")
                #main.get_users_following(users_id)                
                
                CustomMessages.ok_blue("Finalizando recolección de datos desde Twitter")
            else:
                CustomMessages.warning("Regresar al menú.")
                
            
        else:
            CustomMessages.warning(f"No se seleccionó ninguna tendencia.")
    
    # Procesar de datos recolectados
    def data_process(self):
        CustomMessages.ok_cyan("Iniciando el procesador de datos")
        
        TrendsAPI.data_process()
        
        CustomMessages.ok_cyan("Finalizando el procesador de datos")
    
    # Procesar de datos recolectados
    def data_analizer(self):
        CustomMessages.ok_cyan("Iniciando el analizador de información")
        
        TrendsAPI.data_analizer()
        
        CustomMessages.ok_cyan("Finalizando el analizador de información")
        
    #def search_tweets_by_trends(select_trends):
    #    select_trends = []
    #    
    #    if select_trends:
    #        TrendsAPI.get_tweets_by_trends(select_trends)
    #    else:
    #        CustomMessages.warning("La selección de tendencias está vacía")
    #    
    #    return True
        
# Ejecución del proyecto
# Con variables en un sistema
# main = Main()
# Con variables de entorno en archivo
main = Main('./main/project/.env')

# Limpiar tablas de la base de datos
TrendsAPI.clean_data_base()

# Obtener y listar las tendencias de twitter de los últimos 7 días en el Perú
hasTrends: bool = main.get_trends_by_days(country=CountryTrendsServiceType.PERU.value)

if hasTrends:
    # Generar data con las tendencias de los últimos 7 días
    main.show_trends_by_days()

    # Ingresar una lista de tendencias y recolectar la información referente.
    main.search_trend_list()
    
    # Procesamiento de los datos.
    main.data_process()
    
    # Análisis de la información
    main.data_analizer()
    