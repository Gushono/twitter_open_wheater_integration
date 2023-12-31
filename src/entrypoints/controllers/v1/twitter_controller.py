from fastapi import HTTPException

from src.dtos.dtos import CityInfoBody, CityLatLong
from src.exceptions.client_exceptions import (NotAuthorizedException,
                                              TwitterSendMessageException)
from src.services.search_weather_service import WeatherSearchService
from src.services.social_media_service import TwitterService


async def post_weather_on_twitter(city_info_body: CityInfoBody):
    try:
        message = await get_weather_information(city_info_body)
        tweet_service = TwitterService()
        await tweet_service.publish(message=message)

        return {"message": message}

    except NotAuthorizedException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except TwitterSendMessageException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_weather_information(city_info_body: CityInfoBody) -> str:
    try:
        weather_search_service = WeatherSearchService()
        city_lat_long: CityLatLong = await weather_search_service.get_city_lat_long(
            city=city_info_body.city.lower().strip(),
            state=city_info_body.state.lower().strip(),
        )
        weather_information = (
            await weather_search_service.get_median_temperature_for_next_five_days(
                city_lat_long=city_lat_long
            )
        )
        return format_tweet_message(weather_information, city_lat_long.name)
    except NotAuthorizedException:
        raise NotAuthorizedException("Unauthorized")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def format_tweet_message(weather_information: dict[dict], city_name: str):
    today_date, today_weather = next(iter(weather_information.items()))
    weather_information.pop(today_date)

    today_temp = today_weather["average_temp"]
    today_desc = today_weather["description"]

    initial_message = f"{today_temp}°C e {today_desc} em {city_name} em {today_date}. "

    median_message = ", ".join(
        [
            f"{temp['average_temp']}°C em {day}"
            for day, temp in weather_information.items()
        ]
    )
    message = f"Média para os próximos dias: {median_message}."

    tweet_message = initial_message + message
    return tweet_message
