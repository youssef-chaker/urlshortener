from flask import Flask,jsonify,request
from db import db
from models.urls import Urls
import validators
import uuid
import os
from utils import base62_encode

app=Flask(__name__)
#database configuration
app.config.from_pyfile("config.py")
db.init_app(app)

#runs before the first request is being made to create the database table 
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/encode',methods=['POST','GET'])
def encode():
    try:
        #get the incoming request's body
        url_received = request.get_json().get("url").strip()
    except:
        return jsonify(error='please provide a valid json object with the format {"url": <url> }'),400
    #if url is not valid return a 400 bad request
    if not validators.url(url_received):
        return jsonify(error="not a valid url"),400
    #check if there is a similar url stored in the database
    found_url = Urls.query.filter_by(long=url_received).first()
    #if it exists return the already shortened url stored in the database
    if found_url:
        return jsonify(original_url=url_received,short_url=f"http://shorturl.com/{found_url.short}")
    #else create a new short url and store it in the database
    # in case we get so unlucky and get the same id (which is very unlikely) reexecute the block of code
    while True:
        try:
            #generating a unique id , uuid4 probability of collision is extremely small 
            #converting it from 128bits to a 64bit integer for shorter url
            id = int(uuid.uuid4()) >> 64
            #base62 encoding the id generated
            short_url = base62_encode(id)
            new_url = Urls(str(id),url_received,short_url)
            db.session.add(new_url)
            db.session.commit()
        except:
            continue
        break
    
    return jsonify(original_url=url_received,short_url=f"http://shorturl.com/{short_url}")

@app.route('/decode',methods=['POST','GET'])
def decode():
    try:
        #get the short url from the request's body
        short_url = request.get_json().get("url").strip()
    except:
        return jsonify(error='please provide a valid json object with the format {"url": <url> }'),400
    #if the url is in full form like http://shorturl.com/dCfOiQCzkWu for example extract just the dCfOiQCzkWu part
    if validators.url(short_url):
        short_url = short_url.split("/")[-1]
    #check if there is a similar url stored in the database
    found_url = Urls.query.filter_by(short=short_url).first()
    #if it exists return the original url stored in the database
    if found_url:
        return jsonify(short_url=f'http://shorturl.com/{short_url}',original_url=found_url.long)
    #else return a 404 not found response
    return jsonify(error="url does not exist please encode it first"),404


if __name__=="__main__":
    app.run(host='0.0.0.0',port=os.environ.get("PORT"),debug=True)