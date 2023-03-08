import requests

class API:
    def __init__(self) -> None:
        pass

    def getUserInfo(self, unique_id: str = None, user_id: str = None):
        if not unique_id and not user_id:
            raise ValueError("unique_id or user_id is required")
        
        BASE_URL = "https://tiktok-video-no-watermark2.p.rapidapi.com/user/info"

        querystring = {"unique_id": f"@{unique_id}", "user_id": user_id}

        headers = {
            "X-RapidAPI-Key": "d3c238816amsh07560e941edd79dp1cc25cjsn3e163deab38e",
            "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }

        response = requests.request("GET", BASE_URL, headers=headers, params=querystring)
        return response.json()['data']['user']
    
    def getUserFeed(self, unique_id: str = None, user_id: str = None, count: str = "10", cursor: str = "0"):
        BASE_URL = "https://tiktok-video-no-watermark2.p.rapidapi.com/user/posts"
        querystring = {"unique_id":unique_id,"count":count,"cursor":"0"}

        if user_id:
            querystring['user_id'] = user_id

        headers = {
        'X-RapidAPI-Key': 'd3c238816amsh07560e941edd79dp1cc25cjsn3e163deab38e',
        'X-RapidAPI-Host': 'tiktok-video-no-watermark2.p.rapidapi.com'
        }

        response = requests.request("GET", BASE_URL, headers=headers, params=querystring)
        return response.json()['data']