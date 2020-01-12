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
        mentions = [i for i in mentions if i]
        if (not guild) or (not author):
            return None
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
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        records = data.get('records', [])
        cls.records = []
        for record in records:
            r = Record.load(record, bot)
            if r:
                cls.records.append(r)
        cls.testing = bot.test
        cls.start = min([i.time for i in cls.records] or [datetime.now()])

    @classmethod
    def save(cls):
        records = [i.dump() for i in cls.records]
        data = {'records': records}
        with open('data/records.json', 'w') as f:
            if cls.testing:
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
        if not message.guild:
            return
        cls.records.append(Record.new(message))
