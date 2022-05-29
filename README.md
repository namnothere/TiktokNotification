# TIKTOK notification bot in Python

Get new video on tiktok and send to discord under an embed url cause discord won't let me embed a video.

## Install
```
git clone https://github.com/namnothere/tiktoknotification.git
cd tiktoknotification
pip install -r requirements.txt
```
## Bot configuration

Template configuration file can be found at .env-example. Remove the `-example` part and modify it appropriately.

### `TOKEN`

Your Discord bot token. [Instruction](https://www.writebots.com/discord-bot-token/)

### `CLIENT`

mongodb url to your database. Should be format like this Database[TikTok] -> Collection[bae] -> {
    id: "",
    videos: object,
    channel: 0,
    username: "",
    message: "",
    loop: false,
    userLists: object
}

cause I'm dumb and hardcode it and tired af I don't wanna fix it.

### `embedURL`

Your website domain to handle the embed part since discord won't let us embed video.

### `STREAMABLE`

Your streamable credentials, leave this empty if you want to upload the archive to discord.

### `ArchiveCH`

Channel ID to send archive to. Limit filesize is 8MB.

### `UPLOAD_OPTION`

Either puth "DISCORD" OR "STREAMABLE" here.

## Quick Start

### `setuser`

Username of the account you want to follow.

### `setchannel`

ChannelID to send notification to or leave it empty to register the current channel.

### `setmessage`

Default message to send when new video is posted.

### `start`

Start stalking your oshi.

### `stop`

Your oshi talks too much about feet and you decided to stop.

### Contact 
[Discord](https:/youtu.be/dQw4w9WgXcQ)
