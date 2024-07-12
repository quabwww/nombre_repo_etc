import requests

n = 2
if n == 1:
    paran = {}
    json = {"token": ""}
    url = requests.post("http://localhost:8000/start-bot", json=json)

if n == 2:
    json = {"session_id": "bd73f491-4402-403d-9aaf-8c64f4540110", "user_id": 487430318500872203, "guild_id": 1077968892535775262, "channel_id": 1100148368996573265, "music": "https://www.youtube.com/watch?v=nyXffW_RQI4", "folder": "10000"}
    url = requests.post("http://localhost:8000/play-music", json=json)



print(url.text)