import requests
import json
import re, traceback
from urllib.parse import quote


class Tiktok():
    def __init__(self):
        self.BASE_URL = 'https://www.tiktok.com/node/'
        
    def getTrendingFeed(self, max_cursor = 0, cookies = {}):
        param = {
            "type": 5,
            "secUid": "",
            "id": '',
            "count": 30,
            "minCursor": 0,
            "maxCursor": max_cursor,
            "shareUid": "",
            "lang": "",
            "verifyFp": "",
        }
        try:
            url = self.BASE_URL + 'video/feed'
            res = requests.get(
                url, 
                params=param,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "authority": "www.tiktok.com",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Host": "www.tiktok.com",
                    "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
                },
                cookies=cookies
            )
           
            resp = res.json()
            return resp['body'], res.cookies.get_dict()
        except Exception:
            print(traceback.format_exc())
            return False


    def getUserFeed(self, username = '', max_cursor = 0, userid = '0', user_url = '', use_selenium = False):
        if username == '' and userid == '0' and user_url == '':
            return 'Username or Userid is required'
        print("start of getUserFeed")
        param = {
            "type": 1,
            "secUid": "",
            "id": '',
            "count": 30,
            "minCursor": 0,
            "maxCursor": max_cursor,
            "shareUid": "",
            "lang": "",
            "verifyFp": "",
        }
        if userid != '0':
            param['id'] = userid
        else:
            if user_url != '':
                user = self.getInfoUser(user_url=user_url, use_selenium=use_selenium)
            else:
                user = self.getInfoUser(username=username, use_selenium=use_selenium)
            if user:
                username = list(user['users'].keys())[0]
                param['id'] = user['users'][username]['id']
            else:
                return False
        

        try:
            url = self.BASE_URL + 'video/feed'
            res = requests.get(
                url, 
                params=param,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "authority": "www.tiktok.com",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Host": "www.tiktok.com",
                    "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
                }
            )
            resp = res.json()

            return resp['body'], res.cookies.get_dict()
        except Exception:
            print(traceback.format_exc())
            return False

    def getChallengeFeed(self, challenge = '', max_cursor = 0, ch_id = '0'):
        if challenge == '' and ch_id == '0':
            return 'Challenge or Ch_id is required'
        param = {
            "type": 3,
            "secUid": "",
            "id": '',
            "count": 30,
            "minCursor": 0,
            "maxCursor": max_cursor,
            "shareUid": "",
            "lang": "",
            "verifyFp": "",
        }
        if ch_id != '0':
            param['id'] = ch_id
        else:
            ch = self.getInfoChallenge(challenge)
            if ch:
                param['id'] = ch['challengeInfo']['challenge']['id']
            else:
                return False
        try:
            url = self.BASE_URL + 'video/feed'
            res = requests.get(
                url, 
                params=param,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "authority": "www.tiktok.com",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Host": "www.tiktok.com",
                    "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
                }
            )
            resp = res.json()
            return resp['body'], res.cookies.get_dict()
        except Exception:
            print(traceback.format_exc())
            return False

    def getMusicFeed(self, music = '', max_cursor = 0):
        if music == '':
            return 'Challenge or Ch_id is required'
        param = {
            "type": 4,
            "secUid": "",
            "id": '',
            "count": 30,
            "minCursor": 0,
            "maxCursor": max_cursor,
            "shareUid": "",
            "lang": "",
            "verifyFp": "",
        }
        
        # ch = self.getInfoMusic(music)
        if music:
            param['id'] = music
        else:
            return False
        try:
            url = self.BASE_URL + 'video/feed'
            res = requests.get(
                url, 
                params=param,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "authority": "www.tiktok.com",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Host": "www.tiktok.com",
                    "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
                }
            )
            resp = res.json()
            return resp['body'], res.cookies.get_dict()
        except Exception:
            print(traceback.format_exc())
            return False


    def getInfoUser(self, username = '', user_url = '', use_selenium = False):
        if username != '':
            url = 'http://www.tiktok.com/@{}?lang=en'.format(quote(username))
        if user_url != '':
            url = user_url
        try:
            if use_selenium == True:
                from selenium import webdriver
                from webdriver_manager.chrome import ChromeDriverManager
                options = webdriver.ChromeOptions()
                options.add_argument('--disable-gpu')
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
                driver.get(url)
                html = driver.page_source
                driver.close()
                driver.quit()
            else:
                res = requests.get(
                    url,
                    headers={
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "authority": "www.tiktok.com",
                        # "path": "/@{}".format(quote(username)),
                        "Accept-Encoding": "gzip, deflate",
                        "Connection": "keep-alive",
                        "Host": "www.tiktok.com",
                        "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
                    }
                )
                html = res.text

            resp = self.__extra_next_data__(html)
            return json.loads(resp)['UserModule']
        except Exception:
            print(traceback.format_exc())
            return False

    def getInfoChallenge(self, challenge):
        if challenge == '':
            return 'Challenge is required'
        try:
            res = requests.get(
                'https://www.tiktok.com/tag/{}'.format(quote(challenge)),
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "authority": "www.tiktok.com",
                    "path": "/tag/{}".format(quote(challenge)),
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Host": "www.tiktok.com",
                    "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
                }
            )
            resp = self.__extra_next_data__(res.text)
            return json.loads(resp)['ChallengePage']
        except Exception:
            print(traceback.format_exc())
            return False

    def getInfoMusic(self, music_url):
        if music_url == '':
            return 'Challenge is required'
        try:
            res = requests.get(
                music_url,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "authority": "www.tiktok.com",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Host": "www.tiktok.com",
                    "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
                }
            )
            resp = self.__extra_next_data__(res.text)
            return json.loads(resp)['props']['pageProps']
        except Exception:
            print(traceback.format_exc())
            return False

    def getInfoVideo(self, url):
        if url == '':
            return 'URL is required'
        try:
            res = requests.get(
                url,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "authority": "www.tiktok.com",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Host": "www.tiktok.com",
                    "User-Agent": "Mozilla/5.0  (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/86.0.170 Chrome/80.0.3987.170 Safari/537.36",
                }
            )
            resp = self.__extra_next_data__(res.text)
            video_info = json.loads(resp)['ItemModule']
            vid = list(video_info.keys())[0]
            return video_info[vid], res.cookies.get_dict()
        except Exception:
            print(traceback.format_exc())
            return False


    def __extra_next_data__(self, html):
        resp = self.r1(r'window\[\'SIGI_STATE\'\]=(.*?);window\[\'SIGI_RETRY\'\]', html) or \
        self.r1(r'<script id="SIGI_STATE" type="application/json">(.*?)</script>', html)
        return resp

    def r1(self, pattern, text):
        m = re.search(pattern, text)
        if m:
            return m.group(1)

    

