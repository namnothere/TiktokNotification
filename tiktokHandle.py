from databaseHandle import Database
from TiktokApi import *
from Download import download
import requests

class TikTokHandle():
    def __init__(self, db = None, username = None, userid = None) -> None:
        self.api = Tiktok()
        self.username = username
        self.userid = userid
        self.user = None
        self.newVideos = []
        if db == None:
            self.db = Database()
        self.db = db

    def getUserID(self):
        """
        getUserFeed won't work if we pass username so I figured I'd make a function to get the userid from another webserver
        and then I think it maybe easier to just pass everyone id to DB and query it from there.
        """
        if self.db.getUserID(self.username) != False:
            self.userid = self.db.getUserID(self.username)
            return self.userid
        
        BASE_URL = "https://getUserID.namnothere.repl.co/getuserid"
        data = {"username": self.username}
        r = requests.post(BASE_URL, json = data).json()
        if "error" in r:
            self.userid = 0
        else:
            self.userid = r['id']
            self.db.addUserID(self.username, self.userid)
            print("User ID: " + self.userid)

    def getUser(self):
        try:
            if self.userid == None:
                self.getUserID()
            self.user = self.api.getUserFeed(userid=self.userid, use_selenium=False)[0]
            return self.user
        except Exception as e:
            print("getUser [Error]: " + str(e))
            return "getUser [Error]: " + str(e)

    def sortVideos(self):
        try:
            if self.user == None:
                self.getUser()
            newV = False
            for video in self.user['itemListData']:
                id = video['itemInfos']['id']
                if not self.db.videoExist(id):
                    download(self.username, id)
                    self.newVideos.append(video)
                    self.db.addVideo(video)
                    newV = True
            return newV
        except Exception as e:
            print("sortVideos [Error]: " + str(e))
            return "sortVideos [Error]: " + str(e)