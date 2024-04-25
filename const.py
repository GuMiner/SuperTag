DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")

METRIC = False
SIMULATE_NETWORK = False

SIMULATED_RESPONSE = """{
    "updated": "2024-04-25T10:40:25+00:00",
    "units": "us",
    "forecastGenerator": "BaselineForecastGenerator",
    "generatedAt": "2024-04-25T15:16:54+00:00",
    "updateTime": "2024-04-25T10:40:25+00:00",
    "validTimes": "2024-04-25T04:00:00+00:00/P7DT21H",
    "elevation": {
        "unitCode": "wmoUnit:m",
        "value": 131.97839999999999
    },
    "periods": [
        {
            "number": 1,
            "name": "Today",
            "startTime": "2024-04-25T08:00:00-07:00",
            "endTime": "2024-04-25T18:00:00-07:00",
            "isDaytime": true,
            "temperature": 54,
            "temperatureUnit": "F",
            "temperatureTrend": "falling",
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": 100
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 10.555555555555555
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 99
            },
            "windSpeed": "8 to 12 mph",
            "windDirection": "S",
            "icon": "https://api.weather.gov/icons/land/day/rain,100?size=medium",
            "shortForecast": "Rain",
            "detailedForecast": "Rain. Cloudy. High near 54, with temperatures falling to around 52 in the afternoon. South wind 8 to 12 mph. Chance of precipitation is 100%. New rainfall amounts between a half and three quarters of an inch possible."
        },
        {
            "number": 2,
            "name": "Tonight",
            "startTime": "2024-04-25T18:00:00-07:00",
            "endTime": "2024-04-26T06:00:00-07:00",
            "isDaytime": false,
            "temperature": 47,
            "temperatureUnit": "F",
            "temperatureTrend": null,
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": 100
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 9.4444444444444446
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 97
            },
            "windSpeed": "7 to 10 mph",
            "windDirection": "S",
            "icon": "https://api.weather.gov/icons/land/night/rain,100/rain,80?size=medium",
            "shortForecast": "Rain",
            "detailedForecast": "Rain. Cloudy, with a low around 47. South wind 7 to 10 mph. Chance of precipitation is 100%. New rainfall amounts between a quarter and half of an inch possible."
        },
        {
            "number": 3,
            "name": "Friday",
            "startTime": "2024-04-26T06:00:00-07:00",
            "endTime": "2024-04-26T18:00:00-07:00",
            "isDaytime": true,
            "temperature": 58,
            "temperatureUnit": "F",
            "temperatureTrend": "falling",
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": 90
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 10
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 97
            },
            "windSpeed": "7 mph",
            "windDirection": "S",
            "icon": "https://api.weather.gov/icons/land/day/rain,90?size=medium",
            "shortForecast": "Light Rain",
            "detailedForecast": "Rain. Cloudy. High near 58, with temperatures falling to around 56 in the afternoon. South wind around 7 mph. Chance of precipitation is 90%. New rainfall amounts less than a tenth of an inch possible."
        },
        {
            "number": 4,
            "name": "Friday Night",
            "startTime": "2024-04-26T18:00:00-07:00",
            "endTime": "2024-04-27T06:00:00-07:00",
            "isDaytime": false,
            "temperature": 46,
            "temperatureUnit": "F",
            "temperatureTrend": null,
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": 70
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 9.4444444444444446
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 97
            },
            "windSpeed": "5 to 8 mph",
            "windDirection": "SSW",
            "icon": "https://api.weather.gov/icons/land/night/rain,70/rain,40?size=medium",
            "shortForecast": "Light Rain Likely",
            "detailedForecast": "Rain likely. Mostly cloudy, with a low around 46. South southwest wind 5 to 8 mph. Chance of precipitation is 70%. New rainfall amounts less than a tenth of an inch possible."
        },
        {
            "number": 5,
            "name": "Saturday",
            "startTime": "2024-04-27T06:00:00-07:00",
            "endTime": "2024-04-27T18:00:00-07:00",
            "isDaytime": true,
            "temperature": 56,
            "temperatureUnit": "F",
            "temperatureTrend": null,
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": 70
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 8.3333333333333339
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 96
            },
            "windSpeed": "8 to 12 mph",
            "windDirection": "SSW",
            "icon": "https://api.weather.gov/icons/land/day/rain,60/rain,70?size=medium",
            "shortForecast": "Light Rain Likely",
            "detailedForecast": "Rain likely. Mostly cloudy, with a high near 56. South southwest wind 8 to 12 mph. Chance of precipitation is 70%. New rainfall amounts less than a tenth of an inch possible."
        },
        {
            "number": 6,
            "name": "Saturday Night",
            "startTime": "2024-04-27T18:00:00-07:00",
            "endTime": "2024-04-28T06:00:00-07:00",
            "isDaytime": false,
            "temperature": 46,
            "temperatureUnit": "F",
            "temperatureTrend": null,
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": 70
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 7.7777777777777777
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 95
            },
            "windSpeed": "9 to 13 mph",
            "windDirection": "SSW",
            "icon": "https://api.weather.gov/icons/land/night/rain,70/rain,50?size=medium",
            "shortForecast": "Light Rain Likely",
            "detailedForecast": "Rain likely. Mostly cloudy, with a low around 46. Chance of precipitation is 70%. New rainfall amounts less than a tenth of an inch possible."
        },
        {
            "number": 7,
            "name": "Sunday",
            "startTime": "2024-04-28T06:00:00-07:00",
            "endTime": "2024-04-28T18:00:00-07:00",
            "isDaytime": true,
            "temperature": 55,
            "temperatureUnit": "F",
            "temperatureTrend": null,
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": 90
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 8.3333333333333339
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 94
            },
            "windSpeed": "10 to 15 mph",
            "windDirection": "SSW",
            "icon": "https://api.weather.gov/icons/land/day/rain,90?size=medium",
            "shortForecast": "Light Rain",
            "detailedForecast": "Rain. Mostly cloudy, with a high near 55. Chance of precipitation is 90%."
        },
        {
            "number": 8,
            "name": "Sunday Night",
            "startTime": "2024-04-28T18:00:00-07:00",
            "endTime": "2024-04-29T06:00:00-07:00",
            "isDaytime": false,
            "temperature": 41,
            "temperatureUnit": "F",
            "temperatureTrend": null,
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": null
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 6.666666666666667
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 92
            },
            "windSpeed": "10 to 15 mph",
            "windDirection": "SSW",
            "icon": "https://api.weather.gov/icons/land/night/rain?size=medium",
            "shortForecast": "Light Rain",
            "detailedForecast": "Rain. Mostly cloudy, with a low around 41."
        },
        {
            "number": 9,
            "name": "Monday",
            "startTime": "2024-04-29T06:00:00-07:00",
            "endTime": "2024-04-29T18:00:00-07:00",
            "isDaytime": true,
            "temperature": 54,
            "temperatureUnit": "F",
            "temperatureTrend": null,
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": null
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 5
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 90
            },
            "windSpeed": "13 mph",
            "windDirection": "SSW",
            "icon": "https://api.weather.gov/icons/land/day/rain?size=medium",
            "shortForecast": "Light Rain",
            "detailedForecast": "Rain. Mostly cloudy, with a high near 54."
        },
        {
            "number": 10,
            "name": "Monday Night",
            "startTime": "2024-04-29T18:00:00-07:00",
            "endTime": "2024-04-30T06:00:00-07:00",
            "isDaytime": false,
            "temperature": 40,
            "temperatureUnit": "F",
            "temperatureTrend": null,
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": null
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 4.4444444444444446
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 90
            },
            "windSpeed": "7 to 13 mph",
            "windDirection": "S",
            "icon": "https://api.weather.gov/icons/land/night/rain?size=medium",
            "shortForecast": "Light Rain Likely",
            "detailedForecast": "Rain likely. Mostly cloudy, with a low around 40."
        },
        {
            "number": 11,
            "name": "Tuesday",
            "startTime": "2024-04-30T06:00:00-07:00",
            "endTime": "2024-04-30T18:00:00-07:00",
            "isDaytime": true,
            "temperature": 58,
            "temperatureUnit": "F",
            "temperatureTrend": null,
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": null
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 5
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 88
            },
            "windSpeed": "7 to 12 mph",
            "windDirection": "S",
            "icon": "https://api.weather.gov/icons/land/day/rain?size=medium",
            "shortForecast": "Chance Light Rain",
            "detailedForecast": "A chance of rain. Partly sunny, with a high near 58."
        },
        {
            "number": 12,
            "name": "Tuesday Night",
            "startTime": "2024-04-30T18:00:00-07:00",
            "endTime": "2024-05-01T06:00:00-07:00",
            "isDaytime": false,
            "temperature": 41,
            "temperatureUnit": "F",
            "temperatureTrend": null,
            "probabilityOfPrecipitation": {
                "unitCode": "wmoUnit:percent",
                "value": null
            },
            "dewpoint": {
                "unitCode": "wmoUnit:degC",
                "value": 5.5555555555555554
            },
            "relativeHumidity": {
                "unitCode": "wmoUnit:percent",
                "value": 87
            },
            "windSpeed": "6 to 12 mph",
            "windDirection": "S",
            "icon": "https://api.weather.gov/icons/land/night/rain?size=medium",
            "shortForecast": "Chance Light Rain",
            "detailedForecast": "A chance of rain. Mostly cloudy, with a low around 41."
        }
    ]
}"""