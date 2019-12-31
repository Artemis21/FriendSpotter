from datetime import datetime
import json
import discord


class Record:
    @classmethod
    def load(cls, data, bot):
        time = datetime.fromisoformat(data['time'])
        guild = bot.get_guild(data['guild'])
        author = bot.get_user(data['author'])
        mentions = [bot.get_user(i) for i in data['mentions']]
        return cls(time, guild, author, mentions)

    @classmethod
    def new(cls, message):
        time = datetime.now()
        guild = message.guild
        author = message.author
        mentions = [i for i in message.mentions if type(i) == discord.Member]
        return cls(time, guild, author, mentions)

    def __init__(self, time, guild, author, mentions):
        self.time = time
        self.guild = guild
        self.author = author
        self.mentions = mentions

    def dump(self):
        return {
            'time': self.time.isoformat(),
            'guild': self.guild.id,
            'author': self.author.id,
            'mentions': [i.id for i in self.mentions]
        }


class Records:
    @classmethod
    def load(cls, bot):
        try:
            with open('data/records.json') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        records = data.get('records', [])
        cls.records = []
        for record in records:
            cls.records.append(Record.load(record, bot))
        cls.testing = bot.test

    @classmethod
    def save(cls):
        records = [i.dump() for i in cls.records]
        data = {'records': records}
        with open('data/records.json', 'w') as f:
            if cls.bot.test:
                json.dump(data, f, indent=4)
            else:
                json.dump(data, f, separators=(',', ':'))

    @classmethod
    def fetch(cls, guild=None, start=None, end=None):
        ret = []
        for record in cls.records:
            if guild and record.guild != guild:
                continue
            if start and record.time < start:
                continue
            if end and record.time > end:
                continue
            ret.append(record)
        return ret

    @classmethod
    def log(cls, message):
        if message.author.bot:
            return
        if not message.guild:
            return
        cls.records.append(Record.new(message))
