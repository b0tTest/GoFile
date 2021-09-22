# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/GoFile-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from gofile import uploadFile


Bot = Client(
    "GoFile-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        text=f"**Hello👋 {update.from_user.mention},\n Please send a media for gofile.io stream link.\n\nMade With❤BY @MyTestBotZ**",
        reply_markup=START_BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.media)
async def media_filter(bot, update):
    try:
        message = await update.reply_text(
            text="`Processing...`",
            quote=True,
            disable_web_page_preview=True
        )
        media = await update.download()
        await message.edit_text(
            text="`Uploading to GoFile...`",
            disable_web_page_preview=True
        )
        response = uploadFile(media)
        await message.edit_text(
            text="`🔗 Generating Link...`",
            disable_web_page_preview=True
        )
        try:
            os.remove(media)
        except:
            pass
    except Exception as error:
        await update.reply_text(
            text=f"Error :- <code>{error}</code>",
            quote=True,
            disable_web_page_preview=True
        )
        return
    text = f"⍟ **File Name:** `{response['fileName']}`" + "\n\n"
    text += f"⍟ **Download Page:** `{response['downloadPage']}`" + "\n\n"
    text += f"⍟ **Direct Download Link:** `{response['directLink']}`" + "\n\n"
    text += f"⍟ **Info:** `{response['info']}`" + "\n\n**© @MyTestBotZ**"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🔗Open Link", url=response['directLink']),
                InlineKeyboardButton(text="🚀Share Link", url=f"https://telegram.me/share/url?url={response['directLink']}")
            ],
            [
                InlineKeyboardButton(text="⭕ Updates Channel ⭕", url="https://telegram.me/MyTestBotZ")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

@Bot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "close":
        await update.message.delete()

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("📡 Update Channel", url="https://t.me/mytestbotz"),
        InlineKeyboardButton("🧞‍♂ Creator", url="https://t.me/OO7ROBOT")
        ],[
        InlineKeyboardButton("🔬 Other BotZ", url="https://t.me/mybotzlist"),
        InlineKeyboardButton("Close 🔒", callback_data="close")
        ]]
    )

Bot.run()
