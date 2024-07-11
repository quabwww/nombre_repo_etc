import requests

n = 2
if n == 1:
    paran = {}
    json = {"token": "TOKEN BOT"}
    url = requests.post("http://localhost:8000/start-bot", json=json)

if n == 2:
    json = {"session_id": "9b198ae8-3236-40d9-9104-d7fd74c3a68b", "user_id": 1073383604576591974, "guild_id": 1077968892535775262, "channel_id": 1100148368996573265, "music": "https://www.youtube.com/watch?v=nyXffW_RQI4", "folder": "10000"}
    url = requests.post("http://localhost:8000/play-music", json=json)



print(url.text)