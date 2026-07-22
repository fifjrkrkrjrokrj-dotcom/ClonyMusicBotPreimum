# ───────────────────────────────
# YouTube Download Functions
# ───────────────────────────────

# Step 1: Get your API key
# Go to Telegram and open @InflexAPIBot
# 1️⃣ Start the bot
# 2️⃣ Follow the instructions to get your personal API key
# 3️⃣ Copy the key

# Step 2: Replace API_KEY below with your key
# Step 3: Optionally, change API_URL if different

API_URL = "https://teaminflex.xyz"  # <-- Keep as is unless bot provides a different URL
API_KEY = "INFLEX49143828D"  # <-- Replace this with your key from @InflexAPIBot


# ==============================================
# 🎵 AUDIO DOWNLOAD
# ==============================================
async def download_song(link: str) -> str:
    video_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link
    logger = LOGGER("InflexMusic/platforms/Youtube.py")
    logger.info(f"🎵 [AUDIO] Starting download process for ID: {video_id}")

    if not video_id or len(video_id) < 3:
        return

    DOWNLOAD_DIR = "downloads"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.webm")

    if os.path.exists(file_path):
        logger.info(f"🎵 [LOCAL] Found existing file for ID: {video_id}")
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            payload = {"url": video_id, "type": "audio"}
            headers = {
                "Content-Type": "application/json",
                "X-API-KEY": API_KEY
            }

            # 🔹 Step 1: Trigger API and wait until it's ready
            async with session.post(f"{API_URL}/download", json=payload, headers=headers) as response:
                data = await response.json(content_type=None)

                # Handle non-200 responses
                if response.status != 200:
                    logger.error(f"[AUDIO] API returned HTTP {response.status} → {data}")
                    return

                # Handle explicit API-side errors
                if data.get("status") == "error":
                    detail = data.get("detail", "Unknown error")
                    logger.error(f"[AUDIO] API Error: {detail}")
                    return

                # Handle unexpected response
                if data.get("status") != "success" or not data.get("download_url"):
                    logger.error(f"[AUDIO] Unexpected API response: {data}")
                    return

                download_link = f"{API_URL}{data['download_url']}"

            # 🔹 Step 2: Download the ready file
            async with session.get(download_link) as file_response:
                if file_response.status != 200:
                    logger.error(f"[AUDIO] Download failed ({file_response.status}) for ID: {video_id}")
                    return
                with open(file_path, "wb") as f:
                    async for chunk in file_response.content.iter_chunked(8192):
                        f.write(chunk)

        logger.info(f"🎵 [API] Download completed successfully for ID: {video_id}")
        return file_path

    except Exception as e:
        logger.error(f"[AUDIO] Exception for ID: {video_id} - {e}")
        return


# ==============================================
# 🎥 VIDEO DOWNLOAD
# ==============================================
async def download_video(link: str) -> str:
    video_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link
    logger = LOGGER("InflexMusic/platforms/Youtube.py")
    logger.info(f"🎥 [VIDEO] Starting download process for ID: {video_id}")

    if not video_id or len(video_id) < 3:
        return

    DOWNLOAD_DIR = "downloads"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mkv")

    if os.path.exists(file_path):
        logger.info(f"🎥 [LOCAL] Found existing file for ID: {video_id}")
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            payload = {"url": video_id, "type": "video"}
            headers = {
                "Content-Type": "application/json",
                "X-API-KEY": API_KEY
            }

            # 🔹 Step 1: Trigger API and wait internally
            async with session.post(f"{API_URL}/download", json=payload, headers=headers) as response:
                data = await response.json(content_type=None)

                # Handle non-200 responses
                if response.status != 200:
                    logger.error(f"[VIDEO] API returned HTTP {response.status} → {data}")
                    return

                # Handle explicit API-side errors
                if data.get("status") == "error":
                    detail = data.get("detail", "Unknown error")
                    logger.error(f"[VIDEO] API Error: {detail}")
                    return

                # Handle unexpected response
                if data.get("status") != "success" or not data.get("download_url"):
                    logger.error(f"[VIDEO] Unexpected API response: {data}")
                    return

                download_link = f"{API_URL}{data['download_url']}"

            # 🔹 Step 2: Download the ready file
            async with session.get(download_link) as file_response:
                if file_response.status != 200:
                    logger.error(f"[VIDEO] Download failed ({file_response.status}) for ID: {video_id}")
                    return
                with open(file_path, "wb") as f:
                    async for chunk in file_response.content.iter_chunked(8192):
                        f.write(chunk)

        logger.info(f"🎥 [API] Download completed successfully for ID: {video_id}")
        return file_path

    except Exception as e:
        logger.error(f"[VIDEO] Exception for ID: {video_id} - {e}")
        return
