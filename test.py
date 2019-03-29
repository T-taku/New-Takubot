@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    await bot.invoke(ctx)
    try:
        if not message.guild.id == 540801874765414410:#とあるサーバーでの無効化のため
            if not ctx.command and message.author.bot == False:
                with open("level/level.json", 'r') as fr:
                    levelA = json.load(fr)
                    if levelA.get(str(message.author.id)) == None:
                        levelA[str(message.author.id)] = {'exp':1,'level':0}
                    else:
                        levelA[str(message.author.id)]['exp'] = levelA[str(message.author.id)]['exp'] + 1
                        if levelA[str(message.author.id)]['exp'] == levelA[str(message.author.id)]['level'] * 6 + 2:
                            levelA[str(message.author.id)]['level'] = levelA[str(message.author.id)]['level'] + 1
                            levelA[str(message.author.id)]['exp'] = 0
                            try:
                                with open("level/reaction.json", 'r') as dr:
                                    dor = json.load(dr)
                                if dor[str(message.author.id)] == 1:
                                    await message.add_reaction('🎉')
                                    with open("level/ch.json", 'r') as dr:
                                        dor = json.load(dr)
                                        if dor.get(str(message.author.id)) == None:
                                            await ctx.author.create_dm()
                                            await ctx.author.dm_channel.send('あなたのレベルが'+str(levelA[str(message.author.id)]['level'])+'に上がったよ！🎉')
                                        elif dor[str(message.author.id)]==1:
                                            await ctx.author.create_dm()
                                            await ctx.author.dm_channel.send('あなたのレベルが'+str(levelA[str(message.author.id)]['level'])+'に上がったよ！🎉')
                                        else:
                                            await ctx.message.channel.send('{0}さんのレベルが{1}に上がったよ！🎉'.format(message.author.mention,(levelA[str(message.author.id)]['level'])))
                                else:
                                    pass
                            except:
                                #エラーで書き込まれなくならないようにするため
                                with open("level/reaction.json", 'r') as dr:
                                    dor = json.load(dr)
                                    if dor.get(str(message.author.id)) == None:
                                        dor[str(message.author.id)] = 1
                                        with open("level/reaction.json", 'w') as wdr:
                                            json.dump(dor,wdr)
                with open("level/level.json", 'w') as fs:
                    json.dump(levelA,fs)
    except:
        if message.author.bot == False:#あまり役に立ってない
            pass
