import discord
from discord.ext import commands
import json
# -*- coding: utf-8 -*-
import feedparser
from random import randint
import discord
from time import sleep
import datetime
from collections import OrderedDict
import pprint
import requests
from urllib.request import build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
import http
from http.cookiejar import CookieJar
import urllib
import os
import sys
import traceback
from mimetypes import guess_extension
from time import time, sleep
from urllib.request import urlopen, Request
from urllib.parse import quote
from bs4 import BeautifulSoup
import shutil
import discord as d
from discord.ext.commands import Bot
from discord.ext.commands import bot_has_permissions
from discord.ext.commands import has_permissions
from discord.ext import commands as c
import wikipedia
wikipedia.set_lang('ja')
bot = commands.Bot(command_prefix='tb:')
@bot.event
async def on_ready():
    print('ろぐんしたよ!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='ヘルプは"tb:help"!DMでも使えます。'))
@bot.command()
async def NEWS():
    feed = feedparser.parse('https://www3.nhk.or.jp/rss/news/cat0.xml')
    for x in feed.entries:
        embed = discord.Embed(title="NHK NEWS", description="NHK NEWS", color=0xff0000)
        embed.add_field(name="タイトル:", value=(x.title), inline=False)
        embed.add_field(name="日時:", value=(x.updated), inline=False)
        embed.add_field(name="リンク:", value=(x.links[0].href), inline=False)
        await bot.say(embed=embed) 

@bot.command()
async def jaDiscussionforum():
    feed = feedparser.parse('https://scratch.mit.edu/discuss/feeds/forum/18/')
    jaDiscussion = 0
    for x in feed.entries:
        embed = discord.Embed(title="Scratch Discussionforum(日本語)の最近の投稿", description="Discussionforumの最近の更新", color=0xffa500)
        embed.add_field(name="タイトル:", value=(x.title), inline=False)
        embed.add_field(name="日時:", value=(x.updated), inline=False)
        embed.add_field(name="投稿者:", value=(x.author), inline=False)
        embed.add_field(name="リンク", value=(x.links[0].href), inline=False) 
        if jaDiscussion == 5:
            break
        else:
            await bot.say(embed=embed)
            jaDiscussion = jaDiscussion + 1

@bot.command(pass_context = True)
async def status(msg):
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content )
    wd = msg.message.content.replace("tb:status ", "")
    if f'{msg.message.author.name}' == 'T-taku':
        await bot.say("statusを" + wd + "に変更しました。")
        await bot.change_presence(game=discord.Game(name=wd))
    else:
        await bot.say("あなたオーナーじゃないでしょうが!!")

@bot.command(pass_context=True)
async def Wikipedia(msg):
    wd = msg.message.content.replace("tb:Wikipedia ", "")
    try:
        page = wikipedia.page(wd)
        sw = wikipedia.search(wd, results=1)
        sw1 = sw[0].replace(" ", "_")
        sr = wikipedia.page(sw1)
        await bot.say(wd +'を検索したら:' + sr.url + " がヒットしたよ")
    except:
        await bot.say("見つからなかったよ...")

@bot.command()
async def JPScratchWiki():
    feed = feedparser.parse('https://ja.scratch-wiki.info/w/api.php?hidebots=1&days=1&limit=5&hidecategorization=1&action=feedrecentchanges&feedformat=atom')
    for x in feed.entries:
        embed = discord.Embed(title="JPScratchWikiの最近の更新", description="Japanese Scratch Wikiでの最近の更新をお知らせします。", color=0x824880)
        embed.add_field(name="ページ:", value=(x.title), inline=False)
        embed.add_field(name="日時:", value=(x.updated), inline=False)
        embed.add_field(name="編集者:", value=(x.author), inline=False)
        embed.add_field(name="リンク:", value=(x.links[0].href), inline=False)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def weather(msg):
    # URL,保存するファイルのパスを指定
    url = "https://www.jma.go.jp/jp/yoho/images/000_telop_today.png" # 保存したいファイルのパスを指定
    save_name = "weather.png" # test1.pngという名前で保存される。
    urllib.request.urlretrieve(url, save_name)
    await bot.send_file(msg.message.channel, "weather.png")
    await bot.say("全国の天気です。詳しく:https://www.jma.go.jp/jp/yoho/")

@bot.command(pass_context=True)
async def earthquake(msg):
    feed = feedparser.parse('http://weather.goo.ne.jp/earthquake/index.rdf')
    NB = 0
    for x in feed.entrie:
        embed = discord.Embed(title="地震情報", description="最新の地震情報", color=0x824880)
        embed.add_field(name="震源地・最大震度・時間:", value=(x.title), inline=False)
        embed.add_field(name="リンク:", value=(x.links[0].href), inline=False)
        if NB == 5:
            await bot.say("")    
        else:
            await bot.say(embed=embed)
            NB = NB + 1

@bot.command(pass_context=True)
async def User(msg, mus=None):
    if mus == None:
        info = msg.message.author
    else:
        info = msg.message.mentions[0]
    embed = discord.Embed(title="ユーザー情報", description=info.name, color=info.color)
    if not info.avatar_url == None:
        embed.set_thumbnail(url=info.avatar_url)
    else:
        embed.set_thumbnail(url=info.default_avatar_url)
    embed.add_field(name="Discordに参加した時刻", value=info.created_at)
    embed.add_field(name="ユーザーID", value=info.id)
    embed.add_field(name="ステータス", value=str(info.status).replace("online","オンライン").replace("offline","オフライン").replace("idle","退席中").replace("dnd","起こさないで!"))
    embed.add_field(name="botかどうか", value=str(info.bot).replace("True","はい").replace("False","いいえ"))
    embed.add_field(name="表示名", value=info.display_name)
    embed.add_field(name="このサーバーに参加した時刻", value=info.joined_at)
    if not info.game == None:
        embed.add_field(name="now playing", value=info.game)
    if not info.nick == None:
        embed.add_field(name="ニックネーム", value=info.nick)
    embed.add_field(name="このサーバーでの最高役職", value=info.top_role)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def Scratchmall(msg):
    wd = msg.message.content.replace("tb:Scratchmall ", "")
    try:
        url = 'https://api.scratch.mit.edu/users/'+wd+'/messages/count'
        response = urllib.request.urlopen(url)
        content = json.loads(response.read().decode('utf8'))
        await bot.say(wd+"さんのメッセージ件数は"+str(content['count'])+"件だよ。")
        if not ["count"]:
            await bot.say("存在しないユーザーだよ!")
    except:
        ("うーんなんで?取得できなかったよAPIが落ちてるみたい")

@bot.command(pass_context=True)
async def update(msg):
        if f'{msg.message.author.name}' == 'T-taku':
            await bot.say("Wikipediaの検索機能を付けたよ!使ってみよう!**tb:Wikipedia [検索ワード]")
        else:
            await bot.say("そのようなコマンドは存在しないよ!")
bot.remove_command('help')

@bot.command(pass_context = True)
async def help(msg,so=None):
    embed = discord.Embed(title="何ができるか教えるよ！", description="先頭には\"tb:\"がいるから気を付けてね！", color=0x7cfc00)
    embed.set_thumbnail(url="https://raw.githubusercontent.com/T-taku/Discord-T-takubot/master/T-taku.png")
    embed.add_field(name="NEWS", value="NHK NEWSを返すよ。", inline=False)
    embed.add_field(name="JPScratchWiki", value="Japanese Scratch-Wikiの24時間以内の更新を返すよ。", inline=False)
    embed.add_field(name="earthquake", value="地震情報をお伝えします。", inline=False)
    embed.add_field(name="jaDiscussionforum", value="ScratchのDiscussionforum(Japan)の最近の投稿を集めるよ!", inline=False)
    embed.add_field(name="weather", value="全国の天気情報", inline=False)
    embed.add_field(name="Scratchmall [Username]", value="Scratchのメッセージ件数を返すよ", inline=False)
    embed.add_field(name="User [任意でユーザー名へのメンション]", value="Discordのユーザー情報を返すよ", inline=False)
    embed.add_field(name="Wikipedia [検索ワード]", value="Wikipediaで検索できるよ", inline=False)
    embed.add_field(name="クレジット表記", value="mii-10さんありがとう! mii-10:mii-10#0739(twitter:mii_10_scratch)", inline=False)
    if so == None:
        try:
            await bot.start_private_message(msg.message.author)
            await bot.send_message(msg.message.author, embed=embed)
            await bot.say("ヘルプをDMに送信したよ!")
        except:
            await bot.say("ヘルプを送信できませんでした.....")
    else:
        await bot.say(embed=embed)

bot.run("token")
