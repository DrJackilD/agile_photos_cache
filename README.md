# AGILE PHOTO SEARCH APP

This app cache all images from http://interview.agileengine.com and provide search URL to search by metadata fields

## Installation
Make sure you have `Docker` and `docker-compose` installed in your system

Then create `.env` file with settings (list of available and required settings you can find in the following section)
 
Then run `docker-compose up -d`

Application will start on 8000 port

You're all set :)

## Available env variables
APP_AGILE_PHOTO_API_KEY - API key to Agile API **(required)**

APP_DEBUG - start applciation in debug mode (optional)

APP_CACHE_UPDATE_DELAY - delay for cache rebuild in seconds (optional, default: 600)
