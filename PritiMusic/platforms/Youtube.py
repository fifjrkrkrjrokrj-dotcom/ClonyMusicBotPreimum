import asyncio
import os
import re
import glob
import json
import random
from typing import Union

import aiohttp
import aiofiles
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from py_yt import VideosSearch, CustomSearch, Playlist

from PritiMusic import LOGGER
from PritiMusic.utils.database import is_on_off
from PritiMusic.utils.formatters import time_to_seconds

# --- CONFIG VARIABLES IMPORT ---
from config import (
    YT_API_KEY,           
    YTPROXY_URL as YTPROXY, 
    API_URL,              
    VIDEO_API_URL,        
    API_KEY               
)

logger = LOGGER(__name__)

# --- GLOBAL SESSION & DYNAMIC FALLBACK API ---
FALLBACK_API_URL = "https://shrutibots.site"
YOUR_API_URL = None
CLIENT_SESSION = None

async def get_session():
    """Hyper-Optimized Global aiohttp session with NO TCP LIMITS"""
    global CLIENT_SESSION
    if CLIENT_SESSION is None or CLIENT_SESSION.closed:
        connector = aiohttp.TCPConnector(
            limit=0,  
            ttl_dns_cache=300, 
            enable_cleanup_closed=True 
        )
        CLIENT_SESSION = aiohttp.ClientSession(connector=connector)
    return CLIENT_SESSION

async def load_api_url():
    global YOUR_API_URL
    try:
        session = await get_session()
        async with session.get("https://pastebin.com/raw/rLsBhAQa", timeout=5) as response:
            YOUR_API_URL = (await response.text()).strip() if response.status == 200 else FALLBACK_API_URL
    except:
        YOUR_API_URL = FALLBACK_API_URL

try:
    loop = asyncio.get_event_loop()
    if loop.is_running(): asyncio.create_task(load_api_url())
    else: loop.run_until_complete(load_api_url())
except RuntimeError: pass


# --- UTILITIES ---
def cookie_txt_file():
    try:
        folder = f"{os.getcwd()}/cookies"
        filename = f"{folder}/logs.csv"
        txt_files = glob.glob(os.path.join(folder, '*.txt'))
        if not txt_files: return None
        cookie_file = random.choice(txt_files)
        with open(filename, 'a') as file:
            file.write(f'Choosen File : {cookie_file}\n')
        return f"cookies/{os.path.basename(cookie_file)}"
    except:
        return None

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    return out.decode("utf-8") if out else err.decode("utf-8")

# 🛡️ NEW: FILE VERIFICATION FUNCTION (Corrupt Check)
async def verify_file(path):
    """Checks if the downloaded file is actually a valid and playable media file."""
    if not path or not os.path.exists(path):
        return False
    # Check 1: Size (A real song/video is never less than 50KB)
    if os.path.getsize(path) < 50000:
        return False
    # Check 2: Media Integrity using FFprobe
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"'
    out = await shell_cmd(cmd)
    # If FFprobe successfully reads the duration, it's a valid media file
    if out and out.strip().replace('.', '', 1).isdigit():
        return True
    return False

# --- CORE DOWNLOADER ---
async def _download_stream(url, path, headers=None):
    try:
        session = await get_session()
        async with session.get(url, headers=headers, timeout=30) as response:
            if response.status == 200:
                async with aiofiles.open(path, mode='wb') as f:
                    async for chunk in response.content.iter_chunked(4 * 1024 * 1024):
                        await f.write(chunk)
                if os.path.exists(path) and os.path.getsize(path) > 2048:
                    return path
    except Exception as e:
        logger.error(f"aiohttp stream failed, trying curl: {e}")
    
    cmd = ["curl", "-L", "-C", "-", "--retry", "5", "--silent", "-o", path, url]
    if headers:
        for k, v in headers.items(): cmd.extend(["-H", f"{k}: {v}"])
    
    try:
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await proc.communicate()
        if proc.returncode == 0 and os.path.exists(path) and os.path.getsize(path) > 2048:
            return path
    except: pass

    if os.path.exists(path): os.remove(path)
    return None

# --- ENGINE 1: DYNAMIC FALLBACK API ---
async def download_fallback_engine(vid_id: str, is_video: bool) -> str:
    global YOUR_API_URL
    if not YOUR_API_URL: await load_api_url()
    ext = "mp4" if is_video else "mp3"
    path = os.path.join("downloads", f"{vid_id}_fallback.{ext}") # Distinct name
    try:
        session = await get_session()
        v_type = "video" if is_video else "audio"
        async with session.get(f"{YOUR_API_URL}/download", params={"url": vid_id, "type": v_type}, timeout=10) as resp:
            if resp.status != 200: return None
            token = (await resp.json()).get("download_token")
            if not token: return None
        return await _download_stream(f"{YOUR_API_URL}/stream/{vid_id}?type={v_type}", path, {"X-Download-Token": token})
    except: return None

# --- ENGINE 2: PROXY API ---
async def download_proxy_engine(vid_id: str, is_video: bool) -> str:
    ext = "mp4" if is_video else "mp3"
    path = os.path.join("downloads", f"{vid_id}_proxy.{ext}") # Distinct name
    try:
        session = await get_session()
        headers = {"x-api-key": YT_API_KEY}
        async with session.get(f"{YTPROXY}/info/{vid_id}", headers=headers, timeout=10) as resp:
            if resp.status != 200: return None
            data = await resp.json()
        if data.get('status') == 'success':
            url = data['video_url'] if is_video else data['audio_url']
            return await _download_stream(url, path, headers)
        return None
    except: return None

# --- ENGINE 3: AVIAX POLLING API ---
async def download_polling_engine(vid_id: str, is_video: bool) -> str:
    ext = "mp4" if is_video else "mp3"
    path = os.path.join("downloads", f"{vid_id}_aviax.{ext}") # Distinct name
    try:
        url = f"{VIDEO_API_URL}/video/{vid_id}?api={API_KEY}" if is_video else f"{API_URL}/song/{vid_id}?api={API_KEY}"
        session = await get_session()
        for _ in range(5): 
            async with session.get(url, timeout=8) as resp:
                if resp.status != 200: return None
                data = await resp.json()
                status = data.get("status", "").lower()
                
                if status == "done":
                    dl_url = data.get("link")
                    return await _download_stream(dl_url, path) if dl_url else None
                elif status == "downloading":
                    await asyncio.sleep(3) 
                else: 
                    return None
    except: return None


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="

    def _find_file(self, vid_id):
        if not os.path.exists("downloads"): return None
        for ext in ["mp4", "mp3", "webm", "m4a"]:
            # Check all possible engine variations
            for suffix in ["", "_proxy", "_fallback", "_aviax", "_ytdlp"]:
                filepath = f"downloads/{vid_id}{suffix}.{ext}"
                if os.path.exists(filepath):
                    if os.path.getsize(filepath) > 50000: return os.path.abspath(filepath)
                    else: 
                        try: os.remove(filepath)
                        except: pass
        return None

    async def resolve_stream_url(self, direct_url):
        try:
            session = await get_session()
            async with session.head(direct_url, allow_redirects=True, timeout=3) as resp:
                return str(resp.url)
        except: return direct_url

    async def _get_video_details(self, link: str, limit: int = 1) -> Union[dict, None]:
        try:
            results = VideosSearch(link, limit=limit)
            search_results = (await results.next()).get("result", [])
            for result in search_results: return result

            search = CustomSearch(query=link, searchPreferences="EgIYAw==", limit=1)
            for res in (await search.next()).get("result", []): return res
        except: return None

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message: messages.append(message_1.reply_to_message)
        for msg in messages:
            for ent in (msg.entities or []):
                if ent.type == MessageEntityType.URL: return (msg.text or msg.caption)[ent.offset : ent.offset + ent.length]
            for ent in (msg.caption_entities or []):
                if ent.type == MessageEntityType.TEXT_LINK: return ent.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        link = link.split("&")[0].split("?si=")[0]
        res = await self._get_video_details(link)
        if not res: raise ValueError("No suitable video found")
        dur = res.get("duration", "0:00")
        sec = 0 if "live" in str(dur).lower() else int(time_to_seconds(dur))
        thumb = res.get("thumbnails", [{"url": ""}])[0].get("url").split("?")[0]
        return res["title"], dur, sec, thumb, res["id"]

    async def title(self, link: str, videoid: Union[bool, str] = None):
        return (await self.details(link, videoid))[0]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        return (await self.details(link, videoid))[1]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        return (await self.details(link, videoid))[3]

    async def track(self, link: str, videoid: Union[bool, str] = None):
        t, d, _, th, v = await self.details(link, videoid)
        return {"title": t, "link": link, "vidid": v, "duration_min": d, "thumb": th}, v

    # 🎵 MULTI-ENGINE PLAYLIST LOGIC
    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid: link = self.listbase + link
            
        # Sirf tabhi & hatayein jab ye playlist ka part na ho
        if "&" in link and "list=" not in link:
            link = link.split("&")[0]

        result = []

        # --- ENGINE 1: FAST API EXTRACTION ---
        try:
            logger.info(f"⚡ API se playlist fetch kar raha hoon: {link}")
            playlist_data = await Playlist.get(link)
            if playlist_data and "videos" in playlist_data:
                for video in playlist_data["videos"][:limit]:
                    if video and video.get("id"):
                        result.append(video["id"])
                if result:
                    logger.info(f"✅ API se {len(result)} gaane instantly load ho gaye!")
                    return result
        except Exception as e:
            logger.warning(f"⚠️ Playlist API fail, yt-dlp use kar raha hoon.")

        # --- ENGINE 2: YT-DLP FALLBACK ---
        cookie_file = cookie_txt_file() or ""
        cookie_arg = f'--cookies "{cookie_file}"' if cookie_file else ""
        
        cmd = f'yt-dlp -i --get-id --flat-playlist {cookie_arg} --playlist-end {limit} --skip-download "{link}"'
        
        try:
            playlist_output = await shell_cmd(cmd)
            if playlist_output:
                raw_list = playlist_output.split("\n")
                for key in raw_list:
                    if key.strip() != "":
                        result.append(key.strip())
            logger.info(f"✅ yt-dlp se {len(result)} gaane load ho gaye!")
        except Exception as e:
            logger.error(f"❌ yt-dlp playlist extraction fail: {e}")
            
        return result

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        link = link.split("&")[0]
        ydl_opts = {"quiet": True, "cookiefile": cookie_txt_file()}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            formats = [{"format": f["format"], "filesize": f.get("filesize"), "format_id": f["format_id"], "ext": f["ext"], "format_note": f.get("format_note"), "yturl": link} 
                       for f in ydl.extract_info(link, download=False)["formats"] if "dash" not in str(f.get("format", "")).lower()]
        return formats, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        link = link.split("&")[0]
        res = (await VideosSearch(link, limit=10).next()).get("result", [])
        if not res or query_type >= len(res): raise ValueError("No video found")
        sel = res[query_type]
        return sel["title"], sel["duration"], sel["thumbnails"][0]["url"].split("?")[0], sel["id"]

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        
        vid_id = link if videoid else link.split('v=')[-1].split('&')[0] if 'v=' in link else link.split('/')[-1]
        if videoid: link = self.base + link
        
        loop = asyncio.get_running_loop()
        is_video_req = bool(video)

        # 🔴 LARGE FILE & LIVE STREAM DIRECT PLAY BYPASS (⚡ ANTI-LAG MODE)
        try:
            check_cmd = f'yt-dlp --print "%(is_live)s|%(duration)s" "{link}"'
            check_info = await shell_cmd(check_cmd)
            
            is_live = False
            duration_sec = 0
            
            if check_info:
                parts = check_info.strip().split('|')
                if "True" in parts[0]: is_live = True
                if len(parts) > 1 and parts[1].isdigit(): duration_sec = int(parts[1])

            if is_live or duration_sec > 600:
                logger.info(f"⚡ Bypass Triggered: Live or Large File ({duration_sec}s) for {vid_id} - Streaming Direct...")
                
                # 🛠️ ANTI-LAG FIX: Limit resolution to 480p/720p at max 30FPS
                video_format = "bestvideo[height<=480][fps<=30]+bestaudio/best" if is_video_req else "bestaudio/best"
                cmd = f'yt-dlp -g -f "{video_format}" "{link}"'
                
                stream_url = await shell_cmd(cmd)
                
                if stream_url:
                    return stream_url.split('\n')[0].strip(), False
        except Exception as e:
            logger.error(f"Live/Large file check failed: {e}")

        # --- EXECUTOR FOR SPECIFIC FORMATS ---
        if songvideo or songaudio:
            def format_dl():
                opts = {
                    "format": f"{format_id}+140" if songvideo else format_id,
                    "outtmpl": f"downloads/{title}.{'mp4' if songvideo else '%(ext)s'}",
                    "geo_bypass": True, "nocheckcertificate": True, "quiet": True,
                    "cookiefile": cookie_txt_file(), "prefer_ffmpeg": True,
                }
                if songvideo: opts["merge_output_format"] = "mp4"
                if songaudio: opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}]
                yt_dlp.YoutubeDL(opts).download([link])
            
            await loop.run_in_executor(None, format_dl)
            return f"downloads/{title}.{'mp4' if songvideo else 'mp3'}"

        # --- INSTANT STREAM RESOLUTION ---
        if is_video_req:
            session = await get_session()
            try:
                async with session.get(f"{YTPROXY}/info/{vid_id}", headers={"x-api-key": YT_API_KEY}, timeout=3) as r:
                    if r.status == 200:
                        data = await r.json()
                        if data.get("status") == "success" and data.get("video_url"):
                            real_url = await self.resolve_stream_url(data["video_url"])
                            return f"{real_url}#.mp4", False
            except: pass

        # --- CHECK LOCAL CACHE ONLY ---
        file_path = self._find_file(vid_id)
        if file_path: return file_path, True

        # --- 🏎️ THE ULTIMATE VERIFIED RACE CONDITION ---
        logger.info(f"🏎️ Race Condition Started for: {vid_id} (Verifying results)")
        tasks = [
            asyncio.create_task(download_proxy_engine(vid_id, is_video_req)),
            asyncio.create_task(download_fallback_engine(vid_id, is_video_req)),
            asyncio.create_task(download_polling_engine(vid_id, is_video_req))
        ]

        # Loop tab tak chalega jab tak koi verified file nahi milti ya engines khatam nahi hote
        for future in asyncio.as_completed(tasks):
            try:
                result = await future
                if result:
                    # 🛡️ VERIFY THE FILE
                    is_valid = await verify_file(result)
                    
                    if is_valid:
                        logger.info("✅ File 100% Asli aur Playable Hai! Winner Decided.")
                        # Baaki slow/pending engines ko cancel karo
                        for t in tasks: t.cancel() 
                        return result, True
                    else:
                        logger.warning(f"⚠️ Fake/Corrupt file pakdi gayi: {result}. Deleting and waiting for next engine...")
                        try: os.remove(result)
                        except: pass
            except Exception as e:
                pass

        # --- LAST FALLBACK (⚡ ANTI-LAG yt-dlp ⚡) ---
        logger.info(f"⚙️ Saari APIs fail/corrupt, using lag-free local yt-dlp for: {vid_id}")
        def fallback_ytdl():
            opts = {
                # 🛠️ ANTI-LAG FIX: Limited to 480p 30fps to save Server CPU
                "format": "bestvideo[height<=480][fps<=30][ext=mp4]+bestaudio[ext=m4a]/best" if is_video_req else "bestaudio/best",
                "outtmpl": f"downloads/{vid_id}_ytdlp.%(ext)s",
                "cookiefile": cookie_txt_file(),
                "quiet": True,
                "nocheckcertificate": True, 
                "no_warnings": True,         
                "ignoreerrors": True,        
                "retries": 5,           # Retry badha diya taaki network issue jhel sake
                "fragment_retries": 5,
                "http_chunk_size": 10485760 # 10MB chunk buffering
            }
            if not is_video_req: opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]
            yt_dlp.YoutubeDL(opts).download([link])
            
        await loop.run_in_executor(None, fallback_ytdl)
        
        # Verify Fallback Download
        for ext in ["mp4", "mp3", "webm", "m4a"]:
            final_path = f"downloads/{vid_id}_ytdlp.{ext}"
            if os.path.exists(final_path) and await verify_file(final_path):
                return final_path, True

        return None, False