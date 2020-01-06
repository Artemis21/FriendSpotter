from datetime import datetime
import json


class Points:
    @classmethod
    def load(cls, raw, bot):
        points = raw['points']
        start = datetime.fromisoformat(raw['start'])
        end = datetime.fromisoformat(raw['end'])
        if raw['guild']:
            guild = bot.get_guild(raw['guild'])
            if not guild:
                return None
        else:
            guild = None
        data = {}
        for a_id, b_id, value in points:
            a = bot.get_user(a_id)
            b = bot.get_user(b_id)
            data[(a_id, b_id)] = [a, b, value]
        return cls(data, guild, start, end)

    @classmethod
    def new(cls, guild, start, end):
        return cls({}, guild, start, end)

    def __init__(self, data, guild, start, end):
        self.data = data
        self.start = start
        self.end = end
        self.guild = guild

    def dump(self):
        data = [[a, b, self.data[a, b][2]] for a, b in self.data]
        start = self.start.isoformat()
        end = self.end.isoformat()
        guild = getattr(self.guild, 'id', None)
        return {'points': data, 'start': start, 'end': end, 'guild': guild}

    def add(self, a, b, value=1):
        a_id = a.id
        b_id = b.id
        for key in self.data:
            if a_id in key and b_id in key:
                self.data[key][2] += value
                return
        self.data[(a_id, b_id)] = [a, b, value]


class AllPoints:
    @classmethod
    def load(cls, bot):
        try:
            with open('data/points.json') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        all_points = data.get('points', [])
        cls.all_points = []
        for raw_points in all_points:
            points = Points.load(raw_points, bot)
            if not points:
                continue
            cls.all_points.append(points)
        cls.testing = bot.test

    @classmethod
    def save(cls):
        all_points = []
        for points in cls.all_points:
            all_points.append(points.dump())
        data = {'points': all_points}
        with open('data/points.json', 'w') as f:
            if cls.testing:
                json.dump(data, f, indent=4)
            else:
                json.dump(data, f, separators=(',', ':'))

    @classmethod
    def new(cls, guild, start, end):
        p = Points.new(guild, start, end)
        cls.all_points.append(p)
        return p

    @classmethod
    def fetch(cls, time=None):
        time = time or datetime.now()
        for points in reversed(cls.all_points):
            if points.time < time:
                return points
        return cls.all_points[0]

    @classmethod
    def in_range(cls, guild=None, start=None, end=None):
        ret = []
        for points in cls.all_points:
            if start and points.start < start:
                continue
            if end and points.end > end:
                continue
            if guild != points.guild:
                continue
            ret.append(points)
        return ret
