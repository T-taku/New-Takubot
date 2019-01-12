import discord
from discord.ext import commands
import json
# -*- coding: utf-8 -*-
import feedparser
import random
from random import randint
import discord as d
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
import re
from mimetypes import guess_extension
from time import time, sleep
from urllib.request import urlopen, Request
from urllib.parse import quote
from bs4 import BeautifulSoup
import shutil
import time
import wikipedia
from PIL import Image, ImageDraw, ImageFont
from emoji import emojize
import scratchapi2 as sa
import qrcode
  
"""""
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    #グローバル
    if message.author.bot == False:
        if message.channel.name == cn :
            embed = discord.Embed(title="内容", description=message.content, color=message.author.color)
            embed.set_footer(text=message.guild.name,icon_url=message.guild.icon_url)
            if not message.application == None:
                embed.add_field(name=message.application["name"]+"へのRPC招待", value="RPC招待はグローバル送信できません。")
            if not message.author.avatar_url == None:
                embed.set_author(name=str(message.author.name), icon_url=message.author.avatar_url)
            else:
                embed.set_author(name=str(message.author.name), icon_url=message.author.default_avatar_url)
            if not message.attachments == []:
                embed.set_image(url=message.attachments[0].url)
            for guild in bot.guilds:
                for channel in guild.channels:
                    if channel.name == cn:
                        await channel.send(embed=embed)
            if message.attachments == []:
                await message.delete()
"""
  
TAKUADMIN = "TAKUTUKIROUADMIN"
   
wikipedia.set_lang('ja')
bot = commands.Bot(command_prefix='tb:')
@bot.event
async def on_ready():
    print('ろぐんしたよ!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='ヘルプは"tb:help"!'))
 
@bot.event
async def on_message(message):
    if (message.content)=="sn:inServer":
        await bot.purge_from(message.channel,limit=2)
    try:
        await bot.process_commands(message)
        if not message.server.id == "serverid":
            if not message.content.startswith('tb:') and message.author.bot == False:
                with open("level/level.json", 'r') as fr:
                    level = json.load(fr)
                    if level.get(str(message.author.id)) == None:
                        level[str(message.author.id)] = {'exp':1,'level':0}
                    else:
                        level[str(message.author.id)]['exp'] = level[str(message.author.id)]['exp'] + 1
                        if level[str(message.author.id)]['exp'] == level[str(message.author.id)]['level'] * 6 + 2:
                            level[str(message.author.id)]['level'] = level[str(message.author.id)]['level'] + 1
                            level[str(message.author.id)]['exp'] = 0
                            try:
                                with open("level/reaction.json", 'r') as dr:
                                    dor = json.load(dr)
                                if dor[str(message.author.id)] == 1:
                                    await bot.add_reaction(message, '🎉')
                                await bot.start_private_message(message.author)
                                await bot.send_message(message.author, 'あなたのレベルが'+str(level[str(message.author.id)]['level'])+'に上がったよ！🎉')
                            except:
                                #エラーで書き込まれなくならないようにするため
                                with open("level/reaction.json", 'r') as dr:
                                    dor = json.load(dr)
                                    if dor.get(str(message.author.id)) == None:
                                        dor[str(message.author.id)] = 1
                                        with open("level/reaction.json", 'w') as wdr:
                                            json.dump(dor,wdr)
                with open("level/level.json", 'w') as fs:
                    json.dump(level,fs)
    except:
        if message.author.bot == False:
            print("DMにメッセージが送信されたかも！messageの中身は\""+message.content+"\"だよ！")
 
@bot.command()
async def NEWS():
    feed = feedparser.parse('http://www.news24.jp/rss/index.rdf')
    for x in feed.entries:
        embed = discord.Embed(title="NITTERENEWS24", description="NEWS", color=0xff0000)
        embed.add_field(name="タイトル:", value=(x.title), inline=False)
        embed.add_field(name="内容:", value=(x.description), inline=False)
        embed.add_field(name="リンク:", value=(x.links[0].href), inline=False)
    await bot.say(embed=embed) 
 
@bot.command(pass_context = True)
async def level(msg, tu=None):#レベル確認
    if  msg.message.server.id == "serverid":
        await bot.say("重要！このサーバーではレベルカウントされません！")
    if tu == None:
        with open("level/level.json", 'r') as fr:
            level = json.load(fr)
            if level.get(str(msg.message.author.id)) == None:
                await bot.say("まだレベルカウントがされてないよ！")
            else:
                nowl = level[str(msg.message.author.id)]['level']
                exp = level[str(msg.message.author.id)]['exp']
                nextl = nowl * 6 + 2
                tonextexp = nextl - exp
                nextl = str(nextl)
                tonextexp = str(tonextexp)
                try:
                    r = requests.get(msg.message.author.avatar_url.replace(".webp",".png"), stream=True)
                    if r.status_code == 200:
                        with open("usericon.png", 'wb') as f:
                            f.write(r.content)
                    dlicon = Image.open('usericon.png', 'r')
                except:
                    dlicon = Image.open('noimg.png', 'r')
                dlicon = dlicon.resize((100, 100))
                cv = Image.open('bkg.png','r')
                cv.paste(dlicon, (0, 0))
                dt = ImageDraw.Draw(cv)
                font = ImageFont.truetype('/d_font/meiryo.ttc', 20)
                if len(msg.message.author.display_name) > 13:
                    etc = "…"
                else:
                    etc = ""
                dt.text((10, 100), msg.message.author.display_name[0:13] +etc+"\nレベル:"+str(level[str(msg.message.author.id)]['level']) + "\n経験:" + str(level[str(msg.message.author.id)]['exp'])+"/"+nextl + "\n次のレベルまで:"+tonextexp+"\n※背景画像は、masa2004\nさんのものです。", font=font, fill='#fff')
                cv.save("taku'slevelcard.png", 'PNG') 
                await bot.send_file(msg.message.channel,"taku'slevelcard.png")
    else:
        if msg.message.mentions[0].bot == False:
            with open("level/level.json", 'r') as fr:
                level = json.load(fr)
                if level.get(str(msg.message.mentions[0].id)) == None:
                    await bot.say("まだレベルカウントがされてないよ！")
                else:
                    nowl = level[str(msg.message.mentions[0].id)]['level']
                    exp = level[str(msg.message.mentions[0].id)]['exp']
                    nextl = nowl * 6 + 2
                    tonextexp = nextl - exp
                    nextl = str(nextl)
                    tonextexp = str(tonextexp)
                    try:
                        r = requests.get(msg.message.mentions[0].avatar_url.replace(".webp",".png"), stream=True)
                        if r.status_code == 200:
                            with open("usericon.png", 'wb') as f:
                                f.write(r.content)
                        dlicon = Image.open('usericon.png', 'r')
                    except:
                        dlicon = Image.open('noimg.png', 'r')
                    dlicon = dlicon.resize((100, 100))
                    cv = Image.open('bkg.png','r')
                    cv.paste(dlicon, (0, 0))
                    dt = ImageDraw.Draw(cv)
                    font = ImageFont.truetype('/d_font/meiryo.ttc', 20)
                    if len(msg.message.mentions[0].display_name) > 13:
                        etc = "…"
                    else:
                        etc = ""
                    dt.text((10, 100), msg.message.mentions[0].display_name[0:13] +etc+"\nレベル:"+str(level[str(msg.message.mentions[0].id)]['level']) + "\n経験:" + str(level[str(msg.message.mentions[0].id)]['exp'])+"/"+nextl + "\n次のレベルまで:"+tonextexp+"\n※背景画像は、masa2004\nさんのものです。", font=font, fill='#fff')
                    cv.save("taku'slevelcard.png", 'PNG') 
                    await bot.send_file(msg.message.channel,"taku'slevelcard.png")
        else:
            await bot.say("botはカウントしないんだ…ごめんね！")
   
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
async def URLQR(msg):
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content)
    wd = msg.message.content.replace("tb:URLQR ", "")
    REGEX = r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)"
    URL_PATTERN = re.compile(REGEX)
    match_obj = URL_PATTERN.search(wd)
    if match_obj:
        img = qrcode.make(wd)
        img.save('qrcode_taku.png')
        await bot.send_file(msg.message.channel,"qrcode_taku.png")
        await bot.say(wd+" のQRコードだよ")
    else:
        await bot.say("URLじゃない物入れたでしょ!わかるんだからね!")
  
@bot.command(pass_context = True)
async def chengenick(msg, name=None)
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content )
    if msg.message.author.id == '462765491325501445':
        await bot.change_nickname(msg.message.server.me, name)
        if name == None:
            await bot.say("僕のニックネームをデフォルトの名前に変更したよ。")
        else:
            await bot.say("僕のニックネームを"+name+"に変更したよ。")
    else:
        await bot.say("このコマンドは使えないよ!")
 
@bot.command(pass_context = True) #メッセージを削除する機能。過去の産物
async def delm(msg, msgid):
    owner = msg.message.author.server.owner.name
    if (msg.message.author.name) == owner or "T-taku":
        print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content )
        dmsg = await bot.get_message(msg.message.channel, msgid)
        print(f'{msg.message.author.name}さんのコマンド実行で、{msg.message.server.name}でメッセージ"{dmsg.content}"が削除されました。')
        await bot.delete_message(dmsg)
        await bot.delete_message(msg.message)
        a = await bot.say(f'{msg.message.author.name}さんのコマンド実行で、{msg.message.server.name}でメッセージ"{dmsg.content}"が削除されました。')
        time.sleep(3)
        await bot.delete_message(a)
    else:
        await bot.say("このコマンドはサーバーownerしか実行できないように設計されています。")
 
@bot.command(pass_context = True)
async def delmsgs(msg, msgcount):
    owner = msg.message.author.server.owner.name
    if (msg.message.author.name) == owner or "T-taku":
        try:
            dmc = msg.message
            await bot.delete_message(dmc)
            await bot.purge_from(dmc.channel,limit=int(msgcount))
            a = await bot.say(f"{msgcount}個のメッセージを削除。")
            time.sleep(2)
            await bot.delete_message(a)
        except:
            await bot.say("僕にメッセージの管理権限がないようです。または以下の理由が原因かもしれません。:\n このチャンネルもしくはサーバーのにて僕のメッセージ制限がかかっている(14日立つと自動的に解除されます)")
    else:
        await bot.say("このコマンドはサーバーownerしか実行できないように設計されています。")
 
@bot.command(pass_context=True)
async def adtuika(msg):
    title = msg.message.content.replace("tb:adtuika ", "")
    embed = discord.Embed(title="広告プレビュー", description="", color=0x00bfff)
    embed.add_field(name="内容", value=title, inline=False)
    embed.add_field(name="広告主", value=(msg.message.author.name), inline=False)
    await bot.say(embed=embed)
  
@bot.command(pass_context=True)
async def Wikipedia(msg):
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content)
    wd = msg.message.content.replace("tb:Wikipedia ", "")
    try:
        a = await bot.say("検索中!")
        page = wikipedia.page(wd)
        sw = wikipedia.search(wd, results=1)
        sw1 = sw[0].replace(" ", "_")
        sr = wikipedia.page(sw1)
        await bot.edit_message(a,wd +'を検索したら:' + sr.url + " がヒットしたよ")
    except:
        try:
            wd = msg.message.content.replace("tb:Wikipedia ", "")  
            sw = wikipedia.search(wd, results=1)
            sw1 = sw[0].replace(" ", "_")
            sr = wikipedia.page(sw1)
            await bot.edit_message(a,wd +'を検索したら:' + sr.url + " がヒットしたよ")
        except:
            try:
                if not sw == None:
                    await bot.edit_message(a,wd +'を検索したら、:https://ja.wikipedia.org/wiki/' + sw1 + " がヒットしたよ")
            except:
                await bot.edit_message(a,"見つからなかったよ...")
  
@bot.command(pass_context = True)
async def JPScratchWiki(msg):
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content )
    content = requests.get('https://ja.scratch-wiki.info/w/api.php?action=query&list=recentchanges&rcprop=title|timestamp|user|comment|flags|sizes&format=json').json()
    await bot.say("最新の更新:")
    for i in range(5):
        try:
            embed = discord.Embed(title="ページ:", description=content["query"]['recentchanges'][i]["title"], color=0x42bcf4)
            embed.add_field(name="編集者:", value=content["query"]['recentchanges'][i]["user"])
            embed.add_field(name="サイズ:", value=str(content["query"]['recentchanges'][i]["oldlen"])+"→"+str(content["query"]['recentchanges'][i]["newlen"])+"("+str(content["query"]['recentchanges'][i]["newlen"]-content["query"]['recentchanges'][i]["oldlen"])+")")
            embed.add_field(name="操作:", value=content["query"]['recentchanges'][i]["type"])
            if not content["query"]['recentchanges'][i]["comment"] == "":
                embed.add_field(name="要約:", value=content["query"]['recentchanges'][i]["comment"])
            else:
                embed.add_field(name="要約:", value="要約はありません。")
            embed.add_field(name="時間:", value=content["query"]['recentchanges'][i]["timestamp"].replace("T"," ").replace("Z","").replace("-","/"))
            await bot.send_message(msg.message.channel,embed=embed)
        except:
            eembed = discord.Embed(title="たくにはわかんない更新だったよ、", description="https://ja.scratch-wiki.info/wiki/%E7%89%B9%E5%88%A5:%E6%9C%80%E8%BF%91%E3%81%AE%E6%9B%B4%E6%96%B0 から見てください！", color=0x42bcf4)
            await bot.send_message(msg.message.channel,embed=eembed)
 
@bot.command(pass_context=True)
async def banUser(msg ,ctx):
    owner = msg.message.author.server.owner.name
    if (msg.message.author.name) == owner:
        user = msg.message.mentions[0]
        try:
            user = msg.message.mentions[0]
            day = 3
            ok = await bot.say("{0}さんを{1}日BANしようとしています。よろしいですか?".format(user, day))
            await bot.add_reaction(ok, '⭕')
            await bot.add_reaction(ok, '❌')
            umsg = await bot.wait_for_reaction(['⭕','❌'],user=msg.message.author, message=ok)
            if str(umsg.reaction.emoji) == "⭕":
                await bot.ban(user, delete_message_days=3)
                await bot.say("{0}さんを{1}日間BANしました。".format(user, day))
            else:
                await bot.say("BANしません。")
        except:
            await bot.say("僕に権限がありません。メンバーをBANに許可を入れてください。(ボットが自動的にBANすることはありません。)または僕より権限が上かも知れません。")
    else:
        await bot.say("このコマンドはサーバーownerしか実行できないように設計されています。")
 
@bot.command(pass_context = True)
async def switchLevelupReaction(msg):#レベルアップのリアクション切替
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content )
    with open("level/reaction.json", 'r') as dr:
        dor = json.load(dr)
        if dor.get(str(msg.message.author.id)) == None:
            dor[str(msg.message.author.id)] = 1
            await bot.say("レベルアップのリアクションをオンにしたよ。(DM含む)")
        elif dor[str(msg.message.author.id)] == 1:
            dor[str(msg.message.author.id)] = 0
            await bot.say("レベルアップのリアクションをオフにしたよ。(DM含む)")
        else:
            dor[str(msg.message.author.id)] = 1
            await bot.say("レベルアップのリアクションをオンにしたよ。(DM含む)")
    with open("level/reaction.json", 'w') as wdr:
        json.dump(dor, wdr)
  
@bot.command(pass_context=True)
async def projectsearch(msg):
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content)
    wd = msg.message.content.replace("tb:projectsearch ", "")
    res = sa.Misc().search_projects(wd, limit=5)
    for pj in res:
        if not pj:
            print("ないんだけど")
        else:
            print(pj)
            await bot.say(("{0} ({1}作) {2}".format(pj.title, pj.author.username, pj.url))+" がヒット!")
  
@bot.command(pass_context=True)
async def projectcomment(msg):
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content)
    wd = msg.message.content.replace("tb:projectcomment ", "")
    proj = sa.Project(wd)
    cmts = list(proj.comments(limit=10))
    for cmt in cmts:
        embed = discord.Embed(title=":speech_balloon:ProjectID:"+wd+"のコメント", description="", color=0xffa500)
        embed.add_field(name="投稿者:", value="{0}さん".format(cmt.author.username), inline=False)
        embed.add_field(name="日時:", value="{0}".format(cmt.created), inline=False)
        embed.add_field(name="内容:", value="{0}".format(cmt.content), inline=False)
        await bot.say(embed=embed)
 
@bot.command(pass_context=True)
async def gamea(msg):
    with open("GAMEPOINT.json", 'r') as fr:
        level = json.load(fr)
        nowl = level[str(msg.message.author.id)]['point']
        if level.get(str(msg.message.author.id)) == None:
            level[str(msg.message.author.id)] = {'point':20}
            await bot.say("情報を登録しました。もう一度コマンドを実行してください。")
        else:
            embed = discord.Embed(title="gamea!|ルール説明", description="やりかた", color=0x90ee90)
            embed.add_field(name="やりかた", value="**カード**(秘密のカード):one: :two: :three: :four: :five: です。\n**ルール**あなたは配られたカードの中からカードを選びます。もしボットより強い数字が出たらあなたの勝ちです。もしあなたが出した数字がボットより弱ければあなたの負けです。")
            embed.add_field(name="状況", value="15秒後にこのメッセージは削除されあたらしいメッセージが送信されます。")
            a = await bot.say(embed=embed)
            sleep(15)
            await bot.delete_message(a)
            ft = ['0⃣','1⃣','2⃣','3⃣','4⃣','5⃣']
            b = random.randint(0, 5)
            c = random.randint(0, 5)
            d = random.randint(0, 5)
            r1 = ft[b]
            r2 = ft[c]
            r3 = ft[d]
            timeout=0
            startt = datetime.datetime.now()
            if timeout==startt:
                embed = discord.Embed(title="タイムアウト!...", description="おーい!", color=0xff0000)
                embed.add_field(name="リアクションが押されませんでした。自動的に停止します。", value="")
            else:
                embed = discord.Embed(title="gamea!|状況", description="ボットより強いカードを出しましょう。", color=0x90ee90)
                embed.add_field(name="もっているカード", value=r1+","+r2+","+r3)
                msg1 = await bot.say(embed=embed)
                await bot.add_reaction(msg1, r1)
                await bot.add_reaction(msg1, r2)
                await bot.add_reaction(msg1, r3)
                bot1 = random.randint(1, 6)
                rea = await bot.wait_for_reaction([r1,r2,r3],user=msg.message.author, message=msg1)
                if str(rea.reaction.emoji) == "0⃣":
                    embed.add_field(name="botが出したカード", value=bot1)
                    await bot.edit_message(msg1,embed=embed)
                    await bot.say("あなたの負けですね...")
                if str(rea.reaction.emoji) == "1⃣":
                    if bot1 == 1:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("引き分けだね!")
                    else:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("あなたの負けですね...")
                if str(rea.reaction.emoji) == "2⃣":
                    if bot1 == 2:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("引き分けだね!")
                    if bot1>2:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("あなたの負けですね...")
                    if bot1<2:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("あなたの勝ちですね!")
                if str(rea.reaction.emoji) == "3⃣":
                    if bot1 == 3:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("引き分けだね!")
                    if bot1>3:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("あなたの負けですね...")
                    if bot1<3:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("あなたの勝ちですね!")
                if str(rea.reaction.emoji) == "4⃣":
                    if bot1 == 4:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("引き分けだね!")
                    if bot1>4:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("あなたの負けですね...")
                    if bot1<4:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("あなたの勝ちですね!")
                if str(rea.reaction.emoji) == "5⃣":
                    if bot1 == 5:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("引き分けだね!")
                    if bot1>5:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("あなたの負けですね...")
                    if bot1<5:
                        embed.add_field(name="botが出したカード", value=bot1)
                        await bot.edit_message(msg1,embed=embed)
                        await bot.say("あなたの勝ちですね!")
 
@bot.command(pass_context=True)
async def weather(msg):
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content)
    # URL,保存するファイルのパスを指定
    url = "https://www.jma.go.jp/jp/yoho/images/000_telop_today.png" # 保存したいファイルのパスを指定
    save_name = "weather.png" # test1.pngという名前で保存される。
    urllib.request.urlretrieve(url, save_name)
    await bot.send_file(msg.message.channel, "weather.png")
    await bot.say("全国の天気です。詳しく:https://www.jma.go.jp/jp/yoho/")
 
@bot.command(pass_context=True)
async def User(msg, mus=None):
    with open("level/level.json", 'r') as fr:
        level = json.load(fr)
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content)
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
    if mus == None:
        if level.get(msg.message.author.id) == None:
            embed.add_field(name="たくが計測したレベル", value="レベルを計測してないよ!")
        else:
            nowl = level[str(msg.message.author.id)]['level']
            exp = level[str(msg.message.author.id)]['exp']
            nextl = nowl * 6 + 2
            tonextexp = nextl - exp
            nextl = str(nextl)
            tonextexp = str(tonextexp)
            embed.add_field(name="たくが計測したレベル", value=str(level[str(msg.message.author.id)]['level'])+"レベル")
    else:
        if level.get(msg.message.mentions[0].id) == None:
            embed.add_field(name="たくが計測したレベル", value="レベルを計測してないよ!")
        else:
            nowl = level[str(msg.message.mentions[0].id)]['level']
            exp = level[str(msg.message.mentions[0].id)]['exp']
            nextl = nowl * 6 + 2
            tonextexp = nextl - exp
            nextl = str(nextl)
            tonextexp = str(tonextexp)
            embed.add_field(name="たくが計測したレベル", value=str(level[str(msg.message.mentions[0].id)]['level'])+"レベル")
    embed.add_field(name="このサーバーに参加した時刻", value=info.joined_at)
    if not info.game == None:
        embed.add_field(name="now playing", value=info.game)
    if not info.nick == None:
        embed.add_field(name="ニックネーム", value=info.nick)
    embed.add_field(name="このサーバーでの最高役職", value=info.top_role)
    await bot.say(embed=embed)
  
@bot.command(pass_context = True)
async def ping(msg):#処理時間を返す
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content )
    startt = time.time()
    mes = await bot.say("計測中...!")
    await bot.edit_message(mes,"結果:**"+str(round(time.time()-startt,3))+"**秒だよ!")
   
@bot.command(pass_context=True)
async def Scratchmall(msg):
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content)
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
async def end(msg):
    if f'{msg.message.author.name}' == 'T-taku':
        print("再起動")
        sleep(180)
 
@bot.command(pass_context=True)
async def update(msg):
        if f'{msg.message.author.name}' == 'T-taku':
            await bot.delete_message(msg.message)
            await bot.say("サーバー作成者の皆さんにお知らせです。:ユーザーをBANできる機能を追加しました。(ボットが自動的にBANすることはありません。)\n今のままでは権限がありませんので設定よりBANの権限を僕に付与してください。(付与を行わない場合できません。)(3日間BANします。)\nこれもサーバー作成者向けの機能です。メッセージの件数による削除ができるようになりました。こちらに関してはメッセージ管理の権限が必要です。\n各実行コマンドは:\nBAN:`tb:banUser [BANするユーザーへのメンション]`\nメッセージ削除`tb:delmsgs [件数(3など)]`\nです。以上たくでした。")
        else:
            await bot.say("そのようなコマンドは存在しないよ!")
bot.remove_command('help')
  
@bot.command(pass_context = True)
async def help(msg,so=None):
    print(f'{msg.message.author.name}({msg.message.server.name})_'+ msg.message.content)
    owner = msg.message.author.server.owner.name
    if (msg.message.author.name) == owner:
        embed = discord.Embed(title="サーバー主のみが利用できるコマンド", description="あなたは"+(msg.message.server.name)+"でサーバー作成者または所有権を持っているので以下のコマンドが利用できます。", color=0xff0000)
        embed.add_field(name="tb:banUser [banするユーザーへのメンション]", value="ユーザーを3日間BANすることが可能です。(たくにBANの権限が必要です。)")
        embed.add_field(name="tb:delmsgs [件数]", value="メッセージを件数指定で削除することが可能です。(たくメッセージ管理の権限が必要です。)")
        embed.add_field(name="tb:delm [メッセージID]", value="メッセージをID指定で削除することが可能です。(たくにメッセージ管理の権限が必要です。)")
        await bot.start_private_message(msg.message.author)
        await bot.send_message(msg.message.author, embed=embed)
    else:
        pass
    embed = discord.Embed(title="何ができるか教えるよ！", description="先頭には\"tb:\"がいるから気を付けてね！", color=0x7cfc00)
    embed.set_thumbnail(url="https://raw.githubusercontent.com/T-taku/Discord-T-takubot/master/T-taku.png")
    embed.add_field(name="NEWS", value="最新ニュースを読もうかな?ってときに:page_facing_up: ", inline=False)
    embed.add_field(name="JPScratchWiki", value="Japanese Scratch-Wikiで新しい記事出来たかな?ってときに:exclamation: ", inline=False)
    embed.add_field(name="weather", value="今日は晴れかな?雨かな?ってときに:white_sun_small_cloud:", inline=False)
    embed.add_field(name="Scratchmall [Username]", value="Scratchでメッセージがきてるかも!ってときに:mailbox_with_mail:", inline=False)
    embed.add_field(name="User [任意でユーザー名へのメンション]", value="このユーザーの情報が知りたい!!ってときに:bust_in_silhouette:", inline=False)
    embed.add_field(name="Wikipedia [検索ワード]", value="分からないことがあって困った!そうだWikipedia!!:mag:", inline=False)
    embed.add_field(name="level [任意でメンション]", value="レベルを確認したいな～ってときに:chart_with_upwards_trend:", inline=False)
    embed.add_field(name="ping", value="ボットがどれくらいの速さで動くのかな?知りたい!ってときに:hourglass_flowing_sand:", inline=False)
    embed.add_field(name="switchLevelupReaction", value="levelのときの通知がうるさい!!止めて!ってときに:no_bell: もしくはまた通知してほしいなーってときに:bell:")
    embed.add_field(name="URLQR [リンク]", value="あーこのリンクのQRコードほしい!だれか作ってほしいな～ってときに:printer:", inline=False)
    embed.add_field(name="projectsearch [検索ワード]", value="Scratchでゲームやろうかな?まとめて探そう!ってときに:mag:", inline=False)
    embed.add_field(name="projectcomment [ProjectID]", value="ScratchのProjectのIDさえわかればコメントを取得できるよ。このプロジェクトの評判ってどうなんだろう?ってときに:speech_balloon:", inline=False)
    embed.add_field(name="gamea", value="ボットに勝てるように頑張ろう!:slot_machine: ", inline=False)
    embed.add_field(name="クレジット表記", value="mii-10さんありがとう! mii-10:mii-10#0739(twitter:mii_10_scratch)")
    embed.add_field(name="作成者", value="T-taku#5089")
    embed.set_footer(text="では!")
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
