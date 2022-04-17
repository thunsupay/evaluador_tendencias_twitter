from typing import List, Optional
from enum import Enum
from datetime import datetime


class Attachments:
    media_keys: List[str]

    def __init__(self, media_keys: List[str]) -> None:
        self.media_keys = media_keys


class Domain:
    id: str
    name: str
    description: Optional[str]

    def __init__(self, id: str, name: str, description: Optional[str]) -> None:
        self.id = id
        self.name = name
        self.description = description


class ContextAnnotation:
    domain: Domain
    entity: Domain

    def __init__(self, domain: Domain, entity: Domain) -> None:
        self.domain = domain
        self.entity = entity


class AnnotationType(Enum):
    ORGANIZATION = "Organization"
    OTHER = "Other"
    PERSON = "Person"
    PLACE = "Place"


class Annotation:
    start: int
    end: int
    probability: float
    type: AnnotationType
    normalized_text: str

    def __init__(self, start: int, end: int, probability: float, type: AnnotationType, normalized_text: str) -> None:
        self.start = start
        self.end = end
        self.probability = probability
        self.type = type
        self.normalized_text = normalized_text


class Hashtag:
    start: int
    end: int
    tag: str

    def __init__(self, start: int, end: int, tag: str) -> None:
        self.start = start
        self.end = end
        self.tag = tag


class Mention:
    start: int
    end: int
    username: str
    id: str

    def __init__(self, start: int, end: int, username: str, id: str) -> None:
        self.start = start
        self.end = end
        self.username = username
        self.id = id


class PurpleURL:
    start: int
    end: int
    url: str
    expanded_url: str
    display_url: str

    def __init__(self, start: int, end: int, url: str, expanded_url: str, display_url: str) -> None:
        self.start = start
        self.end = end
        self.url = url
        self.expanded_url = expanded_url
        self.display_url = display_url


class DatumEntities:
    mentions: Optional[List[Mention]]
    urls: Optional[List[PurpleURL]]
    hashtags: Optional[List[Hashtag]]
    annotations: Optional[List[Annotation]]

    def __init__(self, mentions: Optional[List[Mention]], urls: Optional[List[PurpleURL]], hashtags: Optional[List[Hashtag]], annotations: Optional[List[Annotation]]) -> None:
        self.mentions = mentions
        self.urls = urls
        self.hashtags = hashtags
        self.annotations = annotations


class DatumGeo:
    place_id: str

    def __init__(self, place_id: str) -> None:
        self.place_id = place_id


class Lang(Enum):
    EN = "en"
    ES = "es"
    UND = "und"


class DatumPublicMetrics:
    retweet_count: int
    reply_count: int
    like_count: int
    quote_count: int

    def __init__(self, retweet_count: int, reply_count: int, like_count: int, quote_count: int) -> None:
        self.retweet_count = retweet_count
        self.reply_count = reply_count
        self.like_count = like_count
        self.quote_count = quote_count


class ReferencedTweetType(Enum):
    QUOTED = "quoted"
    REPLIED_TO = "replied_to"
    RETWEETED = "retweeted"


class ReferencedTweet:
    type: ReferencedTweetType
    id: str

    def __init__(self, type: ReferencedTweetType, id: str) -> None:
        self.type = type
        self.id = id


class ReplySettings(Enum):
    EVERYONE = "everyone"


class Source(Enum):
    FLAMINGO_FOR_ANDROID = "Flamingo for Android"
    OLINDA_BOT = "OlindaBot"
    SOCIAL_FLOW = "SocialFlow"
    TWITTER_FOR_ANDROID = "Twitter for Android"
    TWITTER_FOR_I_PHONE = "Twitter for iPhone"
    TWITTER_WEB_APP = "Twitter Web App"


class Datum:
    referenced_tweets: Optional[List[ReferencedTweet]]
    entities: DatumEntities
    created_at: datetime
    id: str
    conversation_id: str
    author_id: str
    context_annotations: Optional[List[ContextAnnotation]]
    lang: Lang
    public_metrics: DatumPublicMetrics
    source: Source
    reply_settings: ReplySettings
    possibly_sensitive: bool
    text: str
    attachments: Optional[Attachments]
    in_reply_to_user_id: Optional[str]
    geo: Optional[DatumGeo]

    def __init__(self, referenced_tweets: Optional[List[ReferencedTweet]], entities: DatumEntities, created_at: datetime, id: str, conversation_id: str, author_id: str, context_annotations: Optional[List[ContextAnnotation]], lang: Lang, public_metrics: DatumPublicMetrics, source: Source, reply_settings: ReplySettings, possibly_sensitive: bool, text: str, attachments: Optional[Attachments], in_reply_to_user_id: Optional[str], geo: Optional[DatumGeo]) -> None:
        self.referenced_tweets = referenced_tweets
        self.entities = entities
        self.created_at = created_at
        self.id = id
        self.conversation_id = conversation_id
        self.author_id = author_id
        self.context_annotations = context_annotations
        self.lang = lang
        self.public_metrics = public_metrics
        self.source = source
        self.reply_settings = reply_settings
        self.possibly_sensitive = possibly_sensitive
        self.text = text
        self.attachments = attachments
        self.in_reply_to_user_id = in_reply_to_user_id
        self.geo = geo


class MediaType(Enum):
    PHOTO = "photo"
    VIDEO = "video"


class Media:
    media_key: str
    type: MediaType

    def __init__(self, media_key: str, type: MediaType) -> None:
        self.media_key = media_key
        self.type = type


class Properties:
    pass

    def __init__(self, ) -> None:
        pass


class PlaceGeo:
    type: str
    bbox: List[float]
    properties: Properties

    def __init__(self, type: str, bbox: List[float], properties: Properties) -> None:
        self.type = type
        self.bbox = bbox
        self.properties = properties


class Place:
    geo: PlaceGeo
    name: str
    id: str
    full_name: str
    country_code: str
    country: str
    place_type: str

    def __init__(self, geo: PlaceGeo, name: str, id: str, full_name: str, country_code: str, country: str, place_type: str) -> None:
        self.geo = geo
        self.name = name
        self.id = id
        self.full_name = full_name
        self.country_code = country_code
        self.country = country
        self.place_type = place_type


class Image:
    url: str
    width: int
    height: int

    def __init__(self, url: str, width: int, height: int) -> None:
        self.url = url
        self.width = width
        self.height = height


class FluffyURL:
    start: int
    end: int
    url: str
    expanded_url: str
    display_url: str
    images: Optional[List[Image]]
    status: Optional[int]
    title: Optional[str]
    description: Optional[str]
    unwound_url: Optional[str]

    def __init__(self, start: int, end: int, url: str, expanded_url: str, display_url: str, images: Optional[List[Image]], status: Optional[int], title: Optional[str], description: Optional[str], unwound_url: Optional[str]) -> None:
        self.start = start
        self.end = end
        self.url = url
        self.expanded_url = expanded_url
        self.display_url = display_url
        self.images = images
        self.status = status
        self.title = title
        self.description = description
        self.unwound_url = unwound_url


class TweetEntities:
    annotations: Optional[List[Annotation]]
    hashtags: Optional[List[Hashtag]]
    urls: Optional[List[FluffyURL]]
    mentions: Optional[List[Mention]]

    def __init__(self, annotations: Optional[List[Annotation]], hashtags: Optional[List[Hashtag]], urls: Optional[List[FluffyURL]], mentions: Optional[List[Mention]]) -> None:
        self.annotations = annotations
        self.hashtags = hashtags
        self.urls = urls
        self.mentions = mentions


class Tweet:
    created_at: datetime
    id: str
    conversation_id: str
    author_id: str
    lang: Lang
    entities: TweetEntities
    public_metrics: DatumPublicMetrics
    source: Source
    reply_settings: ReplySettings
    possibly_sensitive: bool
    text: str
    context_annotations: Optional[List[ContextAnnotation]]
    attachments: Optional[Attachments]
    referenced_tweets: Optional[List[ReferencedTweet]]
    in_reply_to_user_id: Optional[int]

    def __init__(self, created_at: datetime, id: str, conversation_id: str, author_id: str, lang: Lang, entities: TweetEntities, public_metrics: DatumPublicMetrics, source: Source, reply_settings: ReplySettings, possibly_sensitive: bool, text: str, context_annotations: Optional[List[ContextAnnotation]], attachments: Optional[Attachments], referenced_tweets: Optional[List[ReferencedTweet]], in_reply_to_user_id: Optional[int]) -> None:
        self.created_at = created_at
        self.id = id
        self.conversation_id = conversation_id
        self.author_id = author_id
        self.lang = lang
        self.entities = entities
        self.public_metrics = public_metrics
        self.source = source
        self.reply_settings = reply_settings
        self.possibly_sensitive = possibly_sensitive
        self.text = text
        self.context_annotations = context_annotations
        self.attachments = attachments
        self.referenced_tweets = referenced_tweets
        self.in_reply_to_user_id = in_reply_to_user_id


class UserPublicMetrics:
    followers_count: int
    following_count: int
    tweet_count: int
    listed_count: int

    def __init__(self, followers_count: int, following_count: int, tweet_count: int, listed_count: int) -> None:
        self.followers_count = followers_count
        self.following_count = following_count
        self.tweet_count = tweet_count
        self.listed_count = listed_count


class User:
    public_metrics: UserPublicMetrics
    verified: bool
    id: str
    username: str
    protected: bool
    created_at: datetime
    location: Optional[str]
    description: str
    name: str

    def __init__(self, public_metrics: UserPublicMetrics, verified: bool, id: str, username: str, protected: bool, created_at: datetime, location: Optional[str], description: str, name: str) -> None:
        self.public_metrics = public_metrics
        self.verified = verified
        self.id = id
        self.username = username
        self.protected = protected
        self.created_at = created_at
        self.location = location
        self.description = description
        self.name = name


class Includes:
    users: List[User]
    tweets: List[Tweet]
    media: List[Media]
    places: List[Place]

    def __init__(self, users: List[User], tweets: List[Tweet], media: List[Media], places: List[Place]) -> None:
        self.users = users
        self.tweets = tweets
        self.media = media
        self.places = places


class Meta:
    newest_id: str
    oldest_id: str
    result_count: int
    next_token: str

    def __init__(self, newest_id: str, oldest_id: str, result_count: int, next_token: str) -> None:
        self.newest_id = newest_id
        self.oldest_id = oldest_id
        self.result_count = result_count
        self.next_token = next_token


class main:
    data: List[Datum]
    includes: Includes
    meta: Meta

    def __init__(self, data: List[Datum], includes: Includes, meta: Meta) -> None:
        self.data = data
        self.includes = includes
        self.meta = meta
