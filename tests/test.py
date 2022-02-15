import json
import unittest
import requests

class Tests(unittest.TestCase):
    
    ENCODE_PATH = "http://localhost:5000/encode"
    DECODE_PATH = "http://localhost:5000/decode"

    #test if it returns 400 when an unvalid url is given to the encode path
    def test_encode_unvalid_url(self):
        r = requests.get(self.ENCODE_PATH,json = {"url" : "hssp:/dfslkj.com"} )
        self.assertEqual(r.status_code,400)

    #test that it returns 400 when not a valid json is provided
    def test_valid_json(self):
        r = requests.get(self.ENCODE_PATH)
        self.assertEqual(r.status_code,400)
        r = requests.get(self.DECODE_PATH)
        self.assertEqual(r.status_code,400)
        r = requests.get(self.ENCODE_PATH,json = {"sdf":"lkjsdf"})
        self.assertEqual(r.status_code,400)
        r = requests.get(self.DECODE_PATH,json = {"sdf":"lkjsdf"})

    #test if the response is in json format
    def test_json(self):
        url = "http://google.com/gmail"
        r = requests.get(self.ENCODE_PATH,json = {"url" : url})
        self.assertEqual(r.headers.get("Content-Type"),"application/json")
        r = requests.get(self.DECODE_PATH,json = {"url" : url})
        self.assertEqual(r.headers.get("Content-Type"),"application/json")

    #test the decode and encode functionalities
    def test_encode_decode(self):
        #test the encode response is 200 and that it returns the same value each time
        url = "http://google.com/gmail"
        r = requests.get(self.ENCODE_PATH,json = {"url" : url})
        self.assertEqual(r.status_code,200)
        self.assertTrue(r.json().get("short_url") is not None)
        short = r.json().get("short_url")
        for i in range(3):
            r = requests.get(self.ENCODE_PATH,json = {"url" : url})
            self.assertEqual(r.status_code,200)
            self.assertTrue(r.json().get("short_url") is not None)
            self.assertEqual(r.json().get("short_url"),short)
        
        #test the decode with full path 
        r = requests.get(self.DECODE_PATH,json = {"url" : short})
        self.assertEqual(r.json().get("original_url"),url)
        r = requests.get(self.DECODE_PATH,json = {"url" : short.split("/")[-1]})
        self.assertEqual(r.json().get("original_url"),url)

    #test if the decode returns 404 if short url does not exist
    def test_decode_404(self):
        short = "aaaabbbbssdsdf"
        r = requests.get(self.DECODE_PATH,json = {"url" : short})
        self.assertEqual(r.status_code,404)
           
        
    
if __name__ == "__main__":
    unittest.main()