from pyrogram.client import Client
from pyrogram.types import Message
import os
import json


def rm_cache(channel=None):
    print("Cleaning Cache...")
    if not channel:
        global image_cache
        image_cache = {}
        try:
            for file in os.listdir("downloads"):
                try:
                    os.remove(f"downloads/{file}")
                    print(f"Removed {file}")
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
    try:
        for file in os.listdir("cache"):
            try:
                if file.endswith(".json"):
                    if channel:
                        if file.startswith(channel):
                            os.remove(f"cache/{file}")
                            print(f"Removed {file}")
                    else:
                        os.remove(f"cache/{file}")
                        print(f"Removed {file}")
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


def get_cache(channel, page):
    if os.path.exists(f"cache/{channel}-{page}.json"):
        with open(f"cache/{channel}-{page}.json", "r") as f:
            return json.load(f)["posts"]
    else:
        return None


def save_cache(channel, cache, page):
    with open(f"cache/{channel}-{page}.json", "w") as f:
        json.dump(cache, f)


async def get_posts(user: Client, channel, page=1):
    page = int(page)
    cache = get_cache(channel, page)
    if cache:
        return cache
    else:
        posts = []
        async for post in user.get_chat_history(
            chat_id=channel, limit=50, offset=(page - 1) * 50
        ):
            post: Message
            if post.video:
                if post.video.file_name:
                    file_name = post.video.file_name
                elif post.caption:
                    file_name = post.caption
                else:
                    file_name = post.video.file_id

                file_name = file_name[:200]

                title = " ".join(file_name.split(".")[:-1])
                posts.append({"msg-id": post.id, "title": title})

        save_cache(channel, {"posts": posts}, page)
        return posts


image_cache = {}


async def get_image(bot: Client, file, channel):
    global image_cache

    cache = image_cache.get(f"{channel}-{file}")
    if cache:
        print(f"Returning img from cache - {channel}-{file}")
        return cache

    else:
        print(f"Downloading img from Telegram - {channel}-{file}")
        msg = await bot.get_messages(channel, int(file))
        img = await bot.download_media(str(msg.video.thumbs[0].file_id))
        image_cache[f"{channel}-{file}"] = img
        return img
