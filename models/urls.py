from db import db

class Urls(db.Model):
    #unique id of each row
    #id is string because it is too large
    id_ = db.Column("id_",db.String(),primary_key = True)
    #the long form of the url with an index to make query faster since we filter by long url form each time to see if it exists (must be unique)
    long = db.Column("long",db.String(),nullable=False,index=True,unique=True)
    #the shortened form of the url (must be unique)
    short = db.Column("short",db.String(3),nullable=False,unique=True)

    #constructor
    def __init__(self,id,long,short):
        self.id_ = id
        self.long = long
        self.short = short
