from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from threading import Thread
import bot

load_dotenv()

app = FastAPI()
bot_client = bot.bot
bot_thread = None

class Token(BaseModel):
    token: str

class PlayMusicRequest(BaseModel):
    session_id: str
    user_id: int
    guild_id: int
    channel_id: int
    music: str
    folder: str

@app.post("/start-bot")
async def start_bot(token: Token):
    global bot_thread
    if bot_thread and bot_thread.is_alive():
        raise HTTPException(status_code=400, detail="Bot ya está corriendo")
    
    bot_thread = Thread(target=bot.run_bot, args=(token.token,))
    bot_thread.start()
    
    session_id = bot_client.create_session()
    return {"message": "Bot iniciado", "session_id": session_id}

@app.post("/play-music")
async def play_music(request: PlayMusicRequest):
    if not bot_client.is_ready():
        raise HTTPException(status_code=400, detail="Bot no está listo")
    
    await bot_client.join_voice_channel(request.session_id, request.user_id, request.guild_id, request.channel_id)
    await bot_client.play_music(request.session_id, request.music, request.folder)
    
    return {"message": "Intentando reproducir música"}

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API para controlar el bot de Discord"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

