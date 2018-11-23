import random
import aiohttp
import time
import asyncio
import json
import discord
from discord.ext import commands
from discord import Game
from random import randint
from discord.ext.commands import Bot

# 100. VE 109. SATIRLARA BAK!
#
# 
#
#-------------------------------------------------------------------

def r(dice : str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    return(result)



def c(*choices : str):
    return(str(random.choice(choices)))
    
#-------------------------------------------------------------------


BOT_PREFIX = ("!")


client = Bot(command_prefix=BOT_PREFIX)

#-------------------------------------------------------------------

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Kodlayan: Смерть#0994"))
    print("Logged in as " + client.user.name)

#-------------------------------------------------------------------

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    await client.process_commands(message)

#-------------------------------------------------------------------

#!hatırlat SANIYE MESAJ#
    
@client.command(pass_context=True)
async def hatırlat(ctx, *, content:str):
    author = ctx.message.author   
    transmis = content.split()
    time = transmis[0]
    konu = transmis[1]
    await client.say(author.mention + ", size bu mesajı " + str(time) + " saniye sonra hatırlatacağım." )
    await asyncio.sleep(int(time))
    await client.send_message(author, "**Hatırlatma:**\n\n" + str(konu))

#-------------------------------------------------------------------

#!kayıt ISIM SINIF#
    
@client.command(pass_context=True)
async def kayıt(ctx, *, content:str):
    server = ctx.message.server
    member = ctx.message.author
    alist = content.split()
    await client.change_nickname(member, alist[0])
    role = discord.utils.get(member.server.roles, name=alist[1])
    await client.add_roles(member, role)


#    await client.replace_roles(member, role)


    
#-------------------------------------------------------------------

#!yardım#
    
@client.command(pass_context=True)
async def yardım(ctx):
    author = ctx.message.author
    await client.send_message(author, "```asciidoc\n= Komutlar = \n\n* !kayıt isim sınıf - İsminizi ve sınıfınızı otomatik olarak atar.\n\n* !hatırlat saniye mesaj - Verilen saniye kadar sonra size bıraktığınız mesajı özelden hatırlatır. 'Özel Mesajlar' devre dışı ise çalışmaz.\n\n* !seç a b c d e - Verilen şıklardan birini seçer (limiti yoktur).\n\n* !söz - Rastgele bir özlü söz söyler. \n\n* !ping - Pong! Şaka bir yana, sunucuyla olan bağlantınızı kontrol etmek için kullanabilirsiniz.\n\n* !temizle sayı - Verilen sayı kadar mesajı siler.\n\n\n[Düzgün çalışmıyorsam lütfen bildirin: Смерть#0994]```")
    await client.delete_message(ctx.message)
    
#-------------------------------------------------------------------

#Misafir ROLU GEREK#
    
@client.event
async def on_member_join(member):
#    role = discord.utils.get(member.server.roles, name="Misafir")
#    await client.add_roles(member, role)
    message = member.mention + ", aramıza hoşgeldin! Aşağıdaki komutu kullanarak kayıt olabilirsin." + "```fix\n!kayıt isim sınıf```"
    smessage = "!yardım komutu ile bütün komutlara ve kullanımlarına ulaşabilirsin.\n\n[Düzgün çalışmıyorsam lütfen bildirin: Смерть#0994]"
    for channel in member.server.channels:
        if channel.name == 'duyuru-i̇stek':   #KANALIN ADINA DIKKAT ET
            await client.send_message(channel, message)
            await client.send_message(member, smessage)

#-------------------------------------------------------------------

#!seç ŞIKLAR BURAYA YAZILIR#
            
@client.command()
async def seç(*choices : str):
    await client.say("Seçimim: " + random.choice(choices))

#-------------------------------------------------------------------

#!ping#
    
@client.command(pass_context=True)
async def ping(ctx):
    author = ctx.message.author
    await client.say("Pong, " + author.mention + "!")
    
#-------------------------------------------------------------------

#!temizle SAYI#
    
@client.command(pass_context=True)
async def temizle(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)+1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(amount + " mesaj silindi.")
    
#-------------------------------------------------------------------

#!söz#

sozler = ["Sonunda, ԁüşmanlarımızın sözlerini değil ԁostlarımızın sessizliğini hatırlayacağız. -Martin Luther King",
          "Ben ışık olmaya, gecelerin susuzluğunu çekmeye ve yalnız olmaya mecburum. -Friedrich Nietzsche",
          "İnsanın ԁostu yoktur, saaԁetin dostu vardır. -Napoléon Bonaparte",
          "Eğer onur kazançlı olsayԁı herkes onurlu olabilirdi. -Thomas More",
          "Mutluluk erԁemin ödülü değil erdemin kenԁisidir. -Baruch Spinoza",
          "Beni korkutan kötülerin baskısı değil iyilerin kayıtsızlığı. -Martin Luther King",
          "Akılsızlar hırsızların en zararlılarıdır. Zamanınızı ve neşenizi çalarlar. -Johann Wolfgang von Goethe",
          "İçinde yaşanılan an, geleceği kemiren geçmiştir. -Henri Bergson",
          "Yaşamak için doğmuşum, yaşamadan ölüyorum. -Jean-Jacques Rousseau",
          "Bilge insanlar konuşurlar çünkü söyleyecek bir şeyleri vardır. Aptal insanlar konuşurlar çünkü bir şey söylemek zorundadırlar. -Platon",
          "Eğitimin pahalı olduğunu düşünüyorsanız, cehaletin bedelini hesaplayın. -Sokrates",
          "Kimilerinin gerçekten özgür olabilmesi için ötekilerin köle olması gerekir. -Aristoteles",
          "Boş bir kafa, şeytanın çalışma odasıdır. -Platon",
          "Bilginin elde edilmesi, bizi iyiye ulaştıracaktır. -Platon",
          "Zor duruma düşecek olsanız dahi dürüstlükten, hakikatten ve doğrudan vazgeçmeyin. Diğer türlüsü sizi daha zor durumda bırakacaktır. -Platon",
          "Kendin pahasına olduktan sonra tüm dünyayı kazansan eline ne geçer? -Sokrates",
          "Felsefe, neleri bilmediğini bilmektir. -Sokrates",
          "Bir şeyleri değiştirmek isteyen insan önce kendisinden başlamalıdır. -Sokrates",
          "Sadece bir iyi vardır, bilgi; ve sadece bir kötü vardır, cehalet. -Sokrates",
          "Unutma, sana ışık tutanlara sırtını dönersen, göreceğin tek şey kendi karanlığındır. -René Descartes",
          "İyi kitaplar okumak, geçmiş yüzyılların en iyi insanlarıyla sohbet etmek gibidir. -René Descartes",
          "Düşünüyorum, o halde varım. -René Descartes",
          "Gençliği yetiştiriniz. Onlara ilim ve irfanın müspet fikirlerini veriniz. Geleceğin aydınlığına onlarla kavuşacaksınız. -Mustafa Kemal Atatürk",
          "Ey kahraman Türk kadını, sen yerde sürünmeye değil, omuzlar üzerinde göklere yükselmeye layıksın. -Mustafa Kemal Atatürk",
          "Medeniyet öyle bir ışıktır ki, ona kayıtsız olanları yakar, mahveder. -Mustafa Kemal Atatürk",
          "İnsanlar dış dünyada olup bitene o kadar kapılmışlardır ki kendi iç dünyalarında neler olduğundan habersizdirler. -Nikola Tesla",
          "Easter egg"
    ]
       
@client.command()
async def söz():
    await client.say(random.choice(sozler))

#-------------------------------------------------------------------

client.run(BOT_TOKEN)




