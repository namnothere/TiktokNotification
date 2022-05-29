
import asyncio
from pystreamable import StreamableApi
from pystreamable.exceptions import StreamableApiServerException
class StreamableHandle():
    def __init__(self, username = None, password = None) -> None:
        self.username = username
        self.password = password
        self.api = StreamableApi(username=username, password=password)



    def upload(self, file, title):
        """
        Upload a file to streamable.
        Need credentials to upload.
        """
        if self.username == None or self.password == None:
            return None
        video = self.api.upload_video(file, title)
        return video

    async def getVideoUrl(self, video):
        info = self.api.get_info(video['shortcode'])
        while "mp4" not in info['files']:
            info = self.api.get_info(video['shortcode'])
            await asyncio.sleep(1)
        return info['files']['mp4']['url']
