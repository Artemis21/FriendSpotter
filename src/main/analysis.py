from datetime import timedelta, datetime
from models.records import Records
from models.points import AllPoints


def timeline(records):
    current = min([i.time for i in records])
    end = max([i.time for i in records])
    records = records
    tline = []
    while current < end:
        minute = []
        newrecords = []
        for record in records:
            if record.time < current:
                minute.append(record.author)
            else:
                newrecords.append(record)
        records = newrecords
        tline.append(minute)
        current += timedelta(minutes=1)
    return tline


def strplist(lst):
    fromstart = []
    started = False
    for itm in lst:
        if started:
            fromstart.append(itm)
        elif itm:
            started = True
            fromstart.append(itm)
    return fromstart


def analyse_close(records, points):
    tline = timeline(records)
    last = [[]] * 60
    for time in tline:
        last = last[1:]
        last.append(time)
        stripped = strplist(last)
        usrs = set(i for j in stripped for i in j)
        if 0 < len(stripped) <= 5 and stripped[-1] and len(usrs) == 2:
            points.add(*usrs, 1)


def analyse_convos(records, points):
    last = []
    for record in records:
        if len(records) == 5:
            last = last[1:]
        last.append(record.author)
        usrs = set(last)
        if len(usrs) == 2:
            points.add(*usrs, 2)


def analyse_mentions(records, points):
    for record in records:
        for other in record.mentions:
            if other != record.author:
                points.add(record.author, other, 4)


def analyse(guild=None, start=None, end=None):
    records = Records.fetch(guild, start, end)
    points = AllPoints.new(
        guild, (start or Records.start), (end or datetime.now())
    )
    print('records got')
    analyse_mentions(records, points)
    print('mentions analysed')
    # analyse_close(records, points)
    print('temporal proximity analysed')
    analyse_convos(records, points)
    print('temporal density analysed')
    return points
