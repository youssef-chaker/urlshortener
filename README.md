# URL Shortening app using Flask
## encode url example
- http://localhost:5000/encode
### request body (GET/POST) :

{"url": "http://urlthatyouwanttoshorten.com/finn" }
### response body:
{
"original_url":  "http://urlthatyouwanttoshorten.com/finn",
"short_url":  "http://shorturl.com/fWRtaSAG3M1"
}

## decode url example
- http://localhost:5000/decode
### request body (GET/POST) :

{"url": "http://shorturl.com/fWRtaSAG3M1" }
### response body:
{
"original_url":  "http://urlthatyouwanttoshorten.com/finn",
"short_url":  "http://shorturl.com/fWRtaSAG3M1"
}

# If you have Docker
## run app
docker container run -d -p 5000:5000 --name **container_name** youssefchaker/urlshortener
## run tests
docker container exec -it 	**container_name** python tests/test.py

# If you do not have Docker
## run app
>must have python >= 3
- clone the project 
- pip  install  -r  requirements.txt
- python app.py
## run tests
> app must be running
- python tests/test.py
