from streamer import media_streamer
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, Response
from bot import get_image, get_posts, rm_cache
from html_gen import posts_html
from pyrogram.client import Client
from config import *
from pyrogram import filters
from pyrogram.types import Message

user = Client(
    "userbot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    session_string=STRING_SESSION,
)
bot = Client(
    "techzindexbot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

app = FastAPI(docs_url=None, redoc_url=None)

with open("templates/home.html") as f:
    HOME_HTML = f.read()
with open("templates/stream.html") as f:
    STREAM_HTML = f.read()


@app.get("/")
async def home():
    return RedirectResponse(HOME_PAGE_REDIRECT)


@app.get("/channel/{channel}")
async def channel(channel):
    posts = await get_posts(user, str(channel).lower())
    phtml = posts_html(posts, channel)
    return HTMLResponse(
        HOME_HTML.replace("POSTS", phtml).replace("CHANNEL_ID", channel)
    )


@app.get("/api/posts/{channel}/{page}")
async def get_posts_api(channel, page: str):
    posts = await get_posts(user, str(channel).lower(), page)
    phtml = posts_html(posts, channel)
    return {"html": phtml}


@app.get("/static/{file}")
async def static_files(file):
    return FileResponse(f"static/{file}")


@app.get("/api/thumb/{channel}/{id}")
async def get_thumb(channel, id):
    img = await get_image(bot, id, channel)
    return FileResponse(img, media_type="image/jpeg")


@app.on_event("startup")
async def startup():
    print("Starting TG Clients...")
    await bot.start()
    await user.start()
    print("TG Clients Started")
    print("========================================")
    print("TechZIndex Started Successfully")
    print("Made By TechZBots | TechShreyash")
    print("========================================")


# Streamer


@app.get("/stream/{channel}/{id}")
async def stream(channel, id):
    return HTMLResponse(
        STREAM_HTML.replace("URL", f"{BASE_URL}/api/stream/{channel}/{id}")
    )


@app.get("/api/stream/{channel}/{id}")
async def stream_api(channel, id, request: Request):
    return await media_streamer(bot, channel, id, request)


# bot commands


@bot.on_message(filters.command("start"))
async def start_cmd(_, msg: Message):
    await msg.reply_text(
        "TechZIndex Up and Running\n\n/clean_cache to clean website cache\n/help to know how to use this bot\n\nMade By @TechZBots | @TechZBots_Support"
    )


@bot.on_message(filters.command("help"))
async def help_cmd(_, msg: Message):
    await msg.reply_text(
        f"""
**How to use this bot?**

1. Add me to your channel as admin
2. Your channel must be public
3. Now open this link domain/channel/<your channel username>

Ex : https://techzindex.herokuapp.com/channel/autoairinganimes

Contact [Owner](tg://user?id={OWNER_ID}) To Get domain of website
Owner Id : {OWNER_ID}"""
    )


@bot.on_message(filters.command("clean_cache"))
async def clean_cache(_, msg: Message):
    if msg.from_user.id in ADMINS:
        x = msg.text.split(" ")
        if len(x) == 2:
            rm_cache(x[1])
        else:
            rm_cache()
        await msg.reply_text("Cache cleaned")
    else:
        await msg.reply_text(
            "You are not my owner\n\nContact [Owner](tg://user?id={OWNER_ID})  If You Want To Update Your Site\n\nRead : https://t.me/TechZBots/524"
        )
