import yt_dlp
import os

def download(username, videoid):
	ydl_opts = {
			'format': "b[vcodec=h264] + [filesize<7.5M]",
			'outtmpl': f'{os.getcwd()}/%(id)s.%(ext)s',
	}
	URL = f'https://www.tiktok.com/@{username}/video/{videoid}'
	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		ydl.download([URL])
	print("Finish downloading")

