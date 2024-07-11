import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from BOT.funciones.func import search_download_return_url
from uuid import uuid4
import asyncio

load_dotenv()

class BotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='?', intents=discord.Intents().all())
        self.sessions = {}

    async def on_ready(self):
        print(f'Bot conectado como {self.user}')
    
    

    def create_session(self):
        session_id = str(uuid4())
        self.sessions[session_id] = {"voice_client": None}
        return session_id

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def end_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    async def join_voice_channel(self, session_id, user_id, guild_id, channel_id):
        try:
            guild = self.get_guild(guild_id)
            if not guild:
                raise commands.CommandError(f"Guild {guild_id} no encontrado")
            
            member = guild.get_member(user_id)
            if not member:
                raise commands.CommandError(f"Miembro {user_id} no encontrado en el guild")

            voice_channel = guild.get_channel(channel_id)
            if not voice_channel or not isinstance(voice_channel, discord.VoiceChannel):
                raise commands.CommandError(f"Canal {channel_id} no es un canal de voz válido")

            if member in voice_channel.members:
                voice_client = await voice_channel.connect()
                self.sessions[session_id]["voice_client"] = voice_client
                print(f"Bot se unió al canal de voz {voice_channel.name}")
            else:
                raise commands.CommandError(f"Miembro {user_id} no está en el canal de voz {channel_id}")

        except Exception as e:
        # Ignorar cualquier error y mostrar el mensaje del error
            print(f"Se produjo un error al intentar unirse al canal de voz: {e}")

    async def play_music(self, session_id, music, folder):
        try:
        # Llamar a la función asíncrona de búsqueda y descarga de música
            mp3_path = await search_download_return_url(music, folder)

            session = self.get_session(session_id)
            if not session:
                raise commands.CommandError("Sesión no válida.")

        # Obtener el cliente de voz actual del bot
            voice_client = discord.utils.get(self.voice_clients)

        # Verificar si el bot está conectado a un canal de voz
            if not voice_client:
                raise commands.CommandError("Bot is not in a voice channel.")

        # Verificar si el archivo MP3 existe
            if not os.path.exists(mp3_path):
                raise commands.CommandError(f"File {mp3_path} not found.")

            def bot_done_playing(error):
            # Esta función se llama después de que termine de reproducirse la canción
                if error:
                    print(f"Player error: {error}")
            # Desconectar el bot después de que termine la canción
                asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.loop)

        # Reproducir el archivo MP3 en el canal de voz
            voice_client.play(discord.FFmpegPCMAudio(mp3_path), after=bot_done_playing)

        except commands.CommandError as e:
        # Capturar y manejar errores específicos de comandos
            print(f"Error executing play_music command: {e}")

        except Exception as e:
        # Capturar cualquier otra excepción inesperada
            print(f"Unexpected error during play_music: {e}")

            


bot = BotClient()

def run_bot(token):
    bot.run(token)

