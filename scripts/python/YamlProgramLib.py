#!/usr/bin/python

# dir: /Users/guerrini/Lavoro/Servizi/Organizzazione/FSCD/FSCD-IJCAR-20/web-common.git/scripts/python

from ScrapProgramLib import getConfProgram

def printYamlList(list, indent=0):
    for el in list:
        print(indent*' '+'- {}'.format(el))

def printYamlTalk(talk, indent=0, listitem=False):
    if (listitem):
        print(indent*' '+'- ', end='')
        indent += 2
        indent1 = 0
    else:
        indent1 = indent
    print(indent1*' '+'time: "{:02d}:{:02d}"'.format(talk['time'][0], talk['time'][1]))
    print(indent*' '+'title: "{}"'.format(talk['title']))
    print(indent*' '+'authors:')
    printYamlList(talk['authors'], indent)

def printYamlTalks(talks, indent=0):
    for talk in talks:
        printYamlTalk(talk, indent, True)

def printYamlSession(session, indent=0, listitem=False):
    if (listitem):
        print(indent*' '+'- ', end='')
        indent += 2
        indent1 = 0
    else:
        indent1 = indent
    print(indent1*' '+'type: {}'.format(session['type']))
    if ('num' in session):
        print(indent*' '+'num: {}'.format(session['num']))
    if ('track' in session):
        print(indent*' '+'track: {}'.format(session['track']))
    print(indent*' '+'title: "{}"'.format(session['title']))
    for key in ['start', 'end']:
        print(indent*' '+'{}: "{:02d}:{:02d}"'.format(key, session[key][0], session[key][1]))
    if (session['type'] == 'talks'):
        print(indent*' '+'chairs:')
        printYamlList(session['chairs'], indent)
        print(indent*' '+'talks:')
        printYamlTalks(session['talks'], indent)

def printYamlSessions(sessions, indent=0):
    for session in sessions:
        printYamlSession(session, indent, True)

def printYamlProgram(prog, indent=0):
    for day in prog:
        print(indent*' '+'- date:', '{:02d}/{:02d}/{:02d}'.format(day[2], day[1], day[0]))
        print(indent*' '+'  sessions:')
        printYamlSessions(prog[day], indent+2)

def printYamlConfProgram(conf, indent=0, listitem=False, resetProgram=False):
    if (listitem):
        print(indent*' '+'- ', end='')
        indent += 2
        indent1 = 0
    else:
        indent1 = indent
    print(indent1*' '+'title: "{}"'.format(conf['title']))
    print(indent*' '+'name: "{}"'.format(conf['name']))
    print(indent*' '+'url: "{}"'.format(conf['url']))
    print(indent*' '+'progurl: "{}"'.format(conf['progurl']))
    if (not ('program' in conf) or not conf['program'] or resetProgram):
        conf['program'] = getConfProgram(conf)
    print(indent*' '+'program:')
    printYamlProgram(conf['program'], indent)
