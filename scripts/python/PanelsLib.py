#!/usr/bin/python

# dir: /Users/guerrini/Lavoro/Servizi/Organizzazione/FSCD/FSCD-IJCAR-20/web-common.git/scripts/python

import csv

def getSessionPanel(sess):
    time = "{:02d}:{:02d}".format(sess['start'][0],sess['start'][1])
    if 'num' in sess:
        num = sess['num']
    else:
        num = ''
    if ('track' in sess):
        track = sess['track']
    else:
        track = ''
    rows = []
    if 'chairs' in sess:
        for chair in sess['chairs']:
            rows.append([time, num, track, 'chair', chair])
    if 'talks' in sess:
        for talk in sess['talks']:
            if 'authors' in talk:
                for author in talk['authors']:
                    rows.append([time, num, track, 'author', author])
    return rows

def getDayPanels(day):
    rows = []
    for session in day:
        rows.extend(getSessionPanel(session))
    return rows

def printDayPanels(conf, date):
    filename = "{:02d}-{:02d}-{:02d}-{}.csv".format(date[0],date[1],date[2], conf['title'])
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in getDayPanels(conf['program'][date]):
            writer.writerow(row)
    return filename

