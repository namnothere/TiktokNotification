import pymongo
import time
import os
from dotenv import load_dotenv

load_dotenv()

DBclient = os.getenv("CLIENT")

class Database():
    def __init__(self):
        self.client = None
        self.connected = False

    def connectDB(self):
        if not self.connected:
            try:
                self.client = pymongo.MongoClient(DBclient, serverSelectionTimeoutMS=3000)
                self.connected = True
            except Exception as e:
                print("connectDB [Error]: " + str(e))
                time.sleep(10)
                return self.connectDB()

    def getAllVideos(self):
        self.connectDB()
        db = self.client.TikTok.bae.find_one({'id':'tiktok'})
        return db['videos']

    def videoExist(self, videoID):
        self.connectDB()
        db = self.client.TikTok.bae.find_one({'id':'tiktok'})
        if videoID in db['videos']:
            return True
        else:
            return False

    def addVideo(self, video):
        self.connectDB()
        videoID = video['itemInfos']['id']
        desc = video['itemInfos']['text']
        createTime = video['itemInfos']['createTime']
        cover = video['itemInfos']['coversOrigin'][0]
        width = video['itemInfos']['video']['videoMeta']['width']
        height = video['itemInfos']['video']['videoMeta']['height']
        username = video['authorInfos']['uniqueId']
        screenName = video['authorInfos']['nickName']
        avatar = video['authorInfos']['coversLarger'][0]
        content = {
            "desc": desc,
            "createTime": createTime,
            "cover": cover,
            "width": width,
            "height": height,
            "username": username,
            "screenName": screenName,
            "avatar": avatar
        }
        self.client.TikTok.bae.find_one_and_update({'id':'tiktok'},{'$set': {f'videos.{videoID}': content}}, return_document = pymongo.ReturnDocument.AFTER)
        return True

    def setUsername(self, username):
        self.connectDB()
        self.client.TikTok.bae.find_one_and_update({'id':'tiktok'},{'$set': {'username': username}}, return_document = pymongo.ReturnDocument.AFTER)
        return True

    def setChannel(self, channelID):
        self.connectDB()
        db = self.client.TikTok.bae.find_one_and_update({'id':'tiktok'},{'$set': {'channel': channelID}}, return_document = pymongo.ReturnDocument.AFTER)
        return True

    def setMessage(self, message):
        self.connectDB()
        self.client.TikTok.bae.find_one_and_update({'id':'tiktok'},{'$set': {'message': message}}, return_document = pymongo.ReturnDocument.AFTER)
        return True

    def getVideo(self, id):
        self.connectDB()
        db = self.client.TikTok.bae.find_one({'id':'tiktok'})
        return db['videos'][str(id)]

    def getUsername(self):
        self.connectDB()
        db = self.client.TikTok.bae.find_one({'id':'tiktok'})
        return db['username']

    def getChannel(self):
        self.connectDB()
        db = self.client.TikTok.bae.find_one({'id':'tiktok'})
        return db['channel']

    def getMessage(self):
        self.connectDB()
        db = self.client.TikTok.bae.find_one({'id':'tiktok'})
        return db['message']

    def getUserID(self, username):
        self.connectDB()
        db = self.client.TikTok.bae.find_one({'id':'tiktok'})
        if username not in db['userLists']:
            return False
        return db['userLists'][username]

    def addUserID(self, username, userID):
        self.connectDB()
        db = self.client.TikTok.bae.find_one({'id':'tiktok'})
        if username not in db["userLists"]:
            db["userLists"][username] = userID
            self.client.TikTok.bae.find_one_and_update({'id':'tiktok'},{'$set': {f'userLists': db["userLists"]}}, return_document = pymongo.ReturnDocument.AFTER)
            return True
        return db['userLists'][username]

    def getloop(self):
        self.connectDB()
        db = self.client.TikTok.bae.find_one({'id':'tiktok'})
        return db['loop']

    def setloop(self, loop):
        self.connectDB()
        self.client.TikTok.bae.find_one_and_update({'id':'tiktok'},{'$set': {'loop': loop}}, return_document = pymongo.ReturnDocument.AFTER)
        return True
    
    
    

    def updateVideoURL(self, videoID, videoURL):
        """update video url (in discord) into database

        
        Parameters
        -----------
        videoID: :class:`str`
            ID from tiktok URL (Example: https://www.tiktok.com/@hakosbaelz_holoen/video/**7100729819205340418**)
        videoURL: :class:`str`
            URL from discord (Example: https://cdn.discordapp.com/attachments/957419729323163699/979363393972633641/7100779151468072193.mp4)

        Raises
        --------
        TypeError
            The parameter name is not found.
        """
        try:
            self.connectDB()
            dict = self.getVideo(videoID)
            dict['video_url'] = videoURL
            self.client.TikTok.bae.find_one_and_update({'id':'tiktok'},{'$set': {f'videos.{videoID}': dict}}, return_document = pymongo.ReturnDocument.AFTER)
            return True
        except TypeError:
            raise TypeError("videoID or videoURL is not found")
        except Exception as e:
            print("updateVideoURL [Error]: " + str(e))
            return False

