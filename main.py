import discord
from random import choice
import os
import datetime
import bdbf
import datetime
import database
import json
import asyncio
import requests

token = os.environ.get('TOKEN', None)




client = bdbf.Client(commandPrefix = "-", embedFooter = {"text": "Powered by wertousek","icon_url":"https://cdn.discordapp.com/avatars/436131686640648195/d72e4885e1d21bca46bd245bb00c4687.png"})
guild = client.get_guild(825802518805086278)

with open ("sprostySlovnik.json","r") as sprostySlovnik:
    sprostaSlova = json.loads(sprostySlovnik.read())

class GetOutOfLoop(Exception):
    pass

@client.event # event decorator/wrapper
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    
    try:
        if message.channel.guild.id not in (436132782725660672,):
            if "guild" in dir(message.channel):
                msgLog = [datetime.datetime.utcnow().isoformat(), str(message.author), str(message.author.id),str(message.channel.guild), str(message.channel.guild.id), str(message.channel), str(message.channel.id), message.content, str(message.id)]
            else:
                msgLog = [datetime.datetime.utcnow().isoformat(), str(message.author), str(message.author.id),"", "", str(message.channel), str(message.channel.id), message.content, str(message.id)]

            try:
                database.messageLog.append_row(msgLog)
            except:
                pass
    except:
        pass
    
    if message.channel.id in [717434872733368531,717456125259153488,773470209503526932,774214326277505044,775706385190617089,800459924164968529,765588311829381141,784788638566711316,798501918972313601,798833045867331584,798856483008806912,798856778728079401,789127499639816212,788087884933890098,775065672782577714,775768221151526974,717440779903172640,717440779903172640]:
        return {"command":False}
    """await spamProtection(message, choice([f"{message.author.mention} nespamuj!",f"{message.author.mention} Mohli bys ps??t trochu m??n??. nikoho to tu nezaj??m??, jak spamuje??",f"{message.author.mention}u?? nic nepi??! bol?? m?? z toho hlava!"]), 5)"""

    """if "kedy" in message.content.lower() and "aktualizacia" in message.content.lower():
        await message.channel.send("Nau?? sa p??sa?? diakritiku ty bezcitn?? hovado")

    for i in [["kdy","bude","aktualizace"],["kdy","vyjde","aktualizace"],["kdy","update"],["jak","je","na","tom","aktualizace"]]:
        b = 0
        for j in i:
            if j in message.content.lower():
                b += 1
        if b == len(i):
            await message.channel.send(choice(["Kdo v??","Nikdo nev??","Bude a?? bude","N??kdy vyjde, neboj"]))

    for i in [["kedy","vyjde","aktualiz??cia"],["kedy","bude","aktualiz??cia"],["kedy","update"],["kedy","updatu"]]:
        b = 0
        for j in i:
            if j in message.content.lower():
                b += 1
        if b == len(i):
            await message.channel.send(choice(["Ani boh nevie","Neboj bude","Zist???? a?? vyjde"]))"""

    if type(message.channel) == discord.DMChannel:
        if message.author.id == 436131686640648195:
            try:
                msgTextSplit = message.content.split(" ",1)
                channel = await client.fetch_channel(int(msgTextSplit[0]))
                await channel.send(msgTextSplit[1])
            except Exception as e:
                await message.channel.send(e)
                raise e

    #print(sprostaSlova)
    b = False
    for slovo in message.content.lower().split(" "):
        for sSlovo in sprostaSlova["sprostaSlova"]:
            if sSlovo in slovo:
                try:
                    for nSslovo in sprostaSlova["neSprostaSlova"]:
                        if nSslovo in slovo:
                            b = False
                            print(slovo, nSslovo, sSlovo)
                            raise GetOutOfLoop
                    b = True
                except GetOutOfLoop:
                    pass
    if b and "Soukupe ml??" not in message.content:
        await message.channel.send(choice([f"{message.author.mention} Zklidni slovn??k kamar??de",f"Hej! {message.author.mention} Tohle slovo bys m??l co nejd????ve odstranit ze sv??ho slovn??ku!",f"Hej! Hej! Hej! {message.author.mention} Nikdo tady na ty tvoje spros????rny neni zv??davej!" ]),delete_after=20)

    if message.author.id != 436131686640648195 and message.channel.guild.id == 436132782725660672 and message.content == "!rank":
                await asyncio.sleep(1)
                await message.channel.send("Amat??r")
                
    if str(message.channel.id) not in database.commandStates.col_values(1):
        database.commandStates.append_row([str(message.channel.id), "off"])
        
    channelIndexInCommandStates = database.commandStates.col_values(1).index(str(message.channel.id))
    
    if database.commandStates.col_values(2)[channelIndexInCommandStates] == "off" and not message.author.guild_permissions.administrator:
        return {"command": False}
        
@client.command("randomKlub")
async def randomKlub(message):
    """nap????e n??hodn?? klub z aktualizace Jaro20 do hry [CSM](https://www.csmweb.net/)"""
    with open("teams20.txt","r") as teams:
        team = choice(teams.read().split("\n"))
    await message.channel.send(team)
    
@client.command("randomKlub18")
async def randomKlub18(message):
    """nap????e n??hodn?? klub z aktualizace Podzim18 do hry [CSM](https://www.csmweb.net/)"""
    with open("teams.txt","r") as teams:
        team = choice(teams.read().split("\n"))
    await message.channel.send(team)
    
@client.command("randomklub")
async def randomKlub(message):
    """randomklub"""
    with open("teams20.txt","r") as teams:
        team = choice(teams.read().split("\n"))
    await message.channel.send(team)
    
@client.command("randomklub18")
async def randomKlub18(message):
    """randomklub18"""
    with open("teams.txt","r") as teams:
        team = choice(teams.read().split("\n"))
    await message.channel.send(team)

@client.command("trh")
async def trh(message):
    """nap????e, po kter??ch kolech se aktualizuje trh"""
    await message.channel.send("Trh se aktualizuje po odehr??n?? t??chto kol:\nDom??c??: 3, 8, 13, 18, 23, 28, 33, 38, 43\nSv??tov??: 5, 10, 15, 20, 25, 30, 35, 40, 45")
    
@client.command("prodej")
async def prodej(message, *attributes):
    """**Pou??it??**: `-prodej <cena hr????e>` nap????e, za kolik procent ceny hr???? prod??vat"""
    if len(attributes) == 0:
        await message.channel.send("Hr????e se doporu??uje prod??vat za 80 a?? 90% jeho ceny")
    else:
        attributes = attributes[0]
        await message.channel.send(f"Hr????e prodej za {int(int(attributes)*0.85)}???, {int(int(attributes)*0.8)}??? a?? {int(int(attributes)*0.9)}???")
            
@client.command("nejslabsi")
async def nejslabsi(message):
    """nap????e tabulku nejslab????ch t??m?? z ka??d?? ligy"""
    await message.channel.send("Hled???? nejslab???? kluby? tak snad tohle pom????e https://media.discordapp.net/attachments/695395367092486144/721144888862703666/Nejvetsi_lemplove.PNG (tabulku vytvo??il FluffyHero)")
   
@client.command("kodyJaro20")
async def kodyJaro20(message):
    """Po??le odkaz na tabulku k??d?? t??m?? pro sc??n????e"""
    await message.channel.send("D??l???? sc??n???? a nev???? k??d t??mu? Nevad??, tady m???? tabulku (hlavn?? se nezapome?? o sc??n???? pak pod??lit :slight_smile:) http://bit.ly/KodyJaro20")

@client.command("hostovani")
async def hostovani(message, *attributes):
    """**Pou??it??**: `-hostovani <cena hr????e> <po??et kol v sezon??> <po??et kol na hostov??n??>` nap?? `-hostovani 300000 30 16`\n Nap????e, kolik pen??z si ????ct za hostov??n??"""
    try:
        attributes = attributes[0]
        attributes = [i for i in map(int,attributes.split(" "))]
        await message.channel.send(f"Hr????e pos??lej na hostov??n?? za {int(attributes[0]/3/attributes[1]*attributes[2])} ???.")
    except:
        await message.channel.send("Tento p????kaz se pou????v?? zp??sobem `-hostovani <cena hr????e> <po??et kol v sezon??> <po??et kol na hostov??n??>` nap?? `-hostovani 300000 30 16` pop????pad?? to sam?? akor??t m??sto hostov??n?? napsat host")

@client.command("host")
async def host(message, *attributes):
    """host"""
    try:
        attributes = attributes[0]
        attributes = [i for i in map(int,attributes.split(" "))]
        await message.channel.send(f"Hr????e pos??lej na hostov??n?? za {int(attributes[0]/3/attributes[1]*attributes[2])} ???.")
    except:
        await message.channel.send("Tento p????kaz se pou????v?? zp??sobem `-hostovani <cena hr????e> <po??et kol v sezon??> <po??et kol na hostov??n??>` nap?? `-hostovani 300000 30 16` pop????pad?? to sam?? akor??t m??sto hostov??n?? napsat host")

@client.command("search")
async def search(msg, *args):
    """Searches the web"""
    print(args)
    if args == ():
        return
    r = requests.get(f"https://api.duckduckgo.com/?q={args[0]}&format=json&kl=cz-cs").json()
    print(msg.content)
    await msg.channel.send("Ty to nev????? No tak j?? ti pom????u", embed=client.embed(r["Heading"], description=r["AbstractText"], fields=[]))
    
@client.command("command")
async def commandToggeling(msg, *args):
    """P??ep??n??n?? command??"""
    if str(msg.channel.id) not in database.commandStates.col_values(1):
        database.commandStates.append_row([str(msg.channel.id), "off"])
        
    channelIndexInCommandStates = database.commandStates.col_values(1).index(str(msg.channel.id))
    args = args[0]
    if args == None:
        await msg.channel.send(f"Commandy jsou aktu??ln?? ***{database.commandStates.col_values(2)[channelIndexInCommandStates]}***")
    elif args == "on":
        database.commandStates.update_cell(channelIndexInCommandStates,2, "on")
        await msg.channel.send("Commandy zapnuty")
    elif args == "off":
        database.commandStates.update_cell(channelIndexInCommandStates,2, "off")
        await msg.channel.send("Commandy vypnuty")
    else:
        await msg.channel.send(f"Nezn??m?? stav {args}, pou??ij *off*, nebo *on*")
        
client.run(token)
