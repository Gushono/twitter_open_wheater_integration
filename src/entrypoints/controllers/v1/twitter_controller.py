from src.dtos.dtos import TweetDto


async def post_weather_on_twitter(tweet_dto: TweetDto):
    print(tweet_dto.city)
    return "Tweet posted successfully"
