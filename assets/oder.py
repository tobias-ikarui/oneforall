import mysql.connector
import sys
import json
import time
import os
from zipfile import ZipFile
import subprocess

dbco = mysql.connector.connect(
    host='localhost',
    user='takefydev',
    passwd="murphy7777",
    database='botperso'
)
db = dbco.cursor()

userId = str(sys.argv[1])


# userId = '443812465772462090'


def getToken():
    token = '0'
    db.execute("SELECT botToken FROM client WHERE discordId = '{}'".format(userId))
    myresult = db.fetchone()
    for x in myresult:
        token = x
    return token


def getDiscordName():
    discordName = '0'
    db.execute("SELECT discordName FROM client WHERE discordId = '{}'".format(userId))
    myresult = db.fetchone()
    for x in myresult:
        discordName = x
    return discordName


def createBot():
    token = getToken()
    path = 'D:\\Github\\DiscordBot\\' + userId
    print(path)
    discordName = getDiscordName()
    os.mkdir(path)
    with ZipFile('D:/Github/DiscordBot/BotPerso.zip', 'r') as zipObj:
        zipObj.extractall(path)

    createDatase = mysql.connector.connect(
        host='localhost',
        user='takefydev',
        passwd="murphy7777"
    )
    createDb = createDatase.cursor()

    createDb.execute("CREATE DATABASE {}".format(discordName))
    con = mysql.connector.connect(
        host='localhost',
        user='takefydev',
        passwd="murphy7777",
        database=discordName
    )
    dbcon = con.cursor()
    dbcon.execute("CREATE TABLE guilds(guildId VARCHAR(100) NOT NULL PRIMARY KEY,guildOwnerId VARCHAR(100) NOT NULL)")
    dbcon.execute("""CREATE TABLE guildConfig(
        guildId VARCHAR(100) NOT NULL PRIMARY KEY,
        prefix VARCHAR(10) DEFAULT '!',
        muteChannelId VARCHAR(100),
        muteRoleId VARCHAR(100) DEFAULT NULL,
        setup BOOLEAN DEFAULT FALSE,
        embedColors VARCHAR(10) DEFAULT '#36393F',
        whitelisted TEXT DEFAULT (''),
        memberRole VARCHAR(100) DEFAULT NULL,
        antiraidLogs VARCHAR(100) DEFAULT NULL,
        inviteChannel VARCHAR(100) DEFAULT NULL,
        inviteMessage TEXT DEFAULT ('Bienvenue ${invited}, ${inviter} à ${count} invites.'),
        soutienMsg TEXT DEFAULT(''),
        soutienOn BOOLEAN DEFAULT FALSE,
        soutienId VARCHAR(100) DEFAULT NULL,
        inviteOn BOOLEAN DEFAULT FALSE,
        owner TEXT DEFAULT (''))
        
        """)
    dbcon.execute("""
        CREATE TABLE antiraid(
        guildId VARCHAR(100) NOT NULL PRIMARY KEY,
        webhookCreate BOOLEAN DEFAULT FALSE,
        roleCreate BOOLEAN DEFAULT FALSE,
        roleUpdate BOOLEAN DEFAULT FALSE,
        roleDelete BOOLEAN DEFAULT FALSE,
        channelCreate BOOLEAN DEFAULT FALSE,
        channelUpdate BOOLEAN DEFAULT FALSE,
        channelDelete BOOLEAN DEFAULT FALSE,
        spam BOOLEAN DEFAULT FALSE,
        ban BOOLEAN DEFAULT FALSE,
        bot BOOLEAN DEFAULT FALSE,
        roleAdd BOOLEAN DEFAULT FALSE)
    """)
    dbcon.execute("""
        CREATE TABLE antiraidWlBp(
        guildId VARCHAR(100) NOT NULL PRIMARY KEY,
        webhookCreate BOOLEAN DEFAULT TRUE,
        roleCreate BOOLEAN DEFAULT TRUE,
        roleUpdate BOOLEAN DEFAULT TRUE,
        roleDelete BOOLEAN DEFAULT TRUE,
        channelCreate BOOLEAN DEFAULT TRUE,
        channelUpdate BOOLEAN DEFAULT TRUE,
        channelDelete BOOLEAN DEFAULT TRUE,
        spam BOOLEAN DEFAULT TRUE,
        ban BOOLEAN DEFAULT TRUE,
        bot BOOLEAN DEFAULT TRUE,
        roleAdd BOOLEAN DEFAULT TRUE)
    """)
    dbcon.execute("""
    CREATE TABLE antiraidconfig(
        guildId VARCHAR(100) NOT NULL PRIMARY KEY,
        webhookCreate VARCHAR(100) DEFAULT 'unrank',
        roleCreate VARCHAR(100) DEFAULT 'unrank',
        roleUpdate VARCHAR(100) DEFAULT 'unrank',
        roleDelete VARCHAR(100) DEFAULT 'unrank',
        channelCreate VARCHAR(100) DEFAULT 'unrank',
        channelUpdate VARCHAR(100) DEFAULT 'unrank',
        channelDelete VARCHAR(100) DEFAULT 'unrank',
        spam VARCHAR(100) DEFAULT 'mute',
        ban VARCHAR(100) DEFAULT 'ban',
        bot VARCHAR(100) DEFAULT 'kick',
        roleAdd VARCHAR(100) DEFAULT 'unrank')
    """)

    with open(path + "/.env", "w") as f:
        f.write(
            "TOKEN={}\nOWNER={}\nDB_USER=takefydev\nDB_PASS=murphy7777\nDB_NAME={}".format(token, userId, discordName))

    data = {}
    data['apps'] = []
    data['apps'].append({
        "name": discordName,
        'script': path + '\\index.js'
    })
    with open(path + "\\pm2.json", 'w') as w:
        json.dump(data, w)


def main():
    createBot()
    pass


if __name__ == '__main__':
    main()
