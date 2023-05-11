#!/usr/bin/python

# dir: /Users/guerrini/Lavoro/Servizi/Organizzazione/FSCD/FSCD-IJCAR-20/web-common.git/scripts/python

import sys

import re

from lxml import html
import requests

def dayProgURL(url, date):
    return (url+'20'+'{:02}'.format(date[0])
                +'-'+'{:02}'.format(date[1])
                +'-'+'{:02}'.format(date[2])+'.html')

def getSessionData(session, strip_title=True):
    data = {}
    ls = session.find_class('coffeebreak')
    if (ls != []):
        data['type'] = 'break'
    else:
        ls = session.find_class('heading')
        if (ls == []):
            raise NameError("Missing heading")
        if (session.find_class('talks') != []):
            data['type'] = 'talks'
        # elif (session.find_class('session_desc')):
        #     data['type'] = 'generic'
        # else:
        #     raise NameError("unknown session type")
        else:
            data['type'] = 'generic'
    interval = ls[0].find_class('interval')[0].text
    lsint = interval.split('-')
    data['start'] = tuple(map(int, lsint[0].split(':')))
    data['end'] = tuple(map(int, lsint[1].split(':')))
    data['title'] = ls[0].find_class('title')[0].text
    if (strip_title):
        r = re.match('Session\s+(\d+)(\w)*:\W*(.*)', data['title'])
        if r:
            data['num'] = r.group(1)
            if (r.group(2)): data['track'] = r.group(2)
            data['title'] = r.group(3)
    return data

def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

def getSessionTalks(session, get_abstracts=True):
    talks = []
    for talk in session.find_class('talk'):
        data = {
                'time': tuple(map(int, talk.find_class('time')[0].text.split(':'))),
                'title': talk.find_class('title')[0].text,
                # 'abstract': html.tostring(talk.find_class('abstract')[0])
                # 'abstract': talk.find_class('abstract')[0].xpath('p/text()')
                }
        if (get_abstracts):
            abstractdiv = talk.find_class('abstract')
            if (abstractdiv != []):
                data['abstract'] = abstractdiv[0].xpath('p/text()')
        # authors = []
        # for person in talk.find_class('authors')[0].find_class('person'):
        #     authors.append(person.text)
        # data['authors'] = authors
        data['authors'] = talk.xpath('*//div[@class="authors"]//a[@class="person"]/text()')
        talks.append(data)
    return talks

def getSessionChairs(session):
    chairs = []
    for person in session.find_class('chair_names')[0].find_class('person'):
        chairs.append(person.text)
    return chairs

def getSessionDesc(session):
    # descdiv = session.find_class('session_desc')
    descdiv = session.xpath('//div[@class="session_desc"]')
    if (descdiv != []):
        return descdiv[0].xpath('p/text()')

def getSessions(root, get_abstracts=True):
    sessions = []
    for session in root.xpath('//div[@class="session"]|//div[@class="session notalk"]'):
        sessionDict = getSessionData(session)
        if (sessionDict['type'] == 'talks'):
            sessionDict['chairs'] = getSessionChairs(session)
            sessionDict['talks'] = getSessionTalks(session, get_abstracts)
        elif (sessionDict['type'] == 'generic'):
            sessionDict['desc'] = getSessionDesc(session)
        sessions.append(sessionDict)
    return sessions

def getProgram(progurl, dates, get_abstracts=True):
    days = {}
    for date in dates:
        dayurl = dayProgURL(progurl, date)
        page = requests.get(dayurl)
        root = html.fromstring(page.content)
        days[date] = getSessions(root, get_abstracts)
    return days

def getConfProgram(conf, get_abstracts=True):
    return getProgram(conf['progurl'], conf['dates'], get_abstracts)

def loadConfProgram(conf, get_abstracts=True):
    conf['program'] = getConfProgram(conf, get_abstracts)
