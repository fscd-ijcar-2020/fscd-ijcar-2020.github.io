#!/usr/bin/python

# dir: /Users/guerrini/Lavoro/Servizi/Organizzazione/FSCD/FSCD-IJCAR-20/web-common.git/scripts/python

def printMarkdownTalk(file, talk, num):
    file.write('<li>\n')
    file.write('{:02d}:{:02d}: '.format(talk['time'][0], talk['time'][1]))
    file.write('<strong>'+', '.join(talk['authors'])+'.</strong>\n')
    file.write('<it>'+format(talk['title']+'.</it>\n'))
    if ('abstract' in talk):
        file.write("""
            &nbsp;&nbsp;&nbsp;
            <a data-toggle="collapse"
                href="#collapseAbstract{num}" role="button"
                style="font-size: var(--text-xsm);"
                aria-expanded="false" aria-controls="collapseAbstract{num}">
                See abstract
            </a>...
            <div class="collapse" id="collapseAbstract{num}">
                <div class="card card-body" style="padding-left:20px">
        """.format(num=num))
        file.write('<br/>\n'.join(talk['abstract']))
        file.write("""
                </div>
            </div>
        """)
    file.write('</li>\n')

def printMarkdownTalks(file, talks):
    num = 0
    file.write('<ul style="list-style-position: outside; list-style: square;">\n')
    for talk in talks:
        num += 1
        printMarkdownTalk(file, talk, num)
    file.write('</ul>\n')

def printMarkdownSession(session, conf=''):
    if (session['type'] != 'talks'):
        return
    if 'track' in session:
        track = session['track']
    else:
        track = ''
    if (conf):
        fname = conf+'-'
    else:
        fname = ''
    fname += 'session{}{}'.format(session['num'], track)
    file = open(fname+'.html', 'w')
    file.write("""---
permalink: /program/sessions/{}
published: true
---

<div class="cd-schedule-modal__event-info">
	<div>
        <p><strong>Session {}{}</strong></p>
        <p>Chair: {}</p>\n
""".format(fname, session['num'], track, (', ').join(session['chairs'])))
    printMarkdownTalks(file, session['talks'])
    file.write("""
    </div>
</div>
""")
    file.close()

def printMarkdownDaySessions(sessions, conf=''):
    for session in sessions:
        printMarkdownSession(session, conf)

def printMarkdownProgSessions(prog, conf=''):
    for day in prog:
        printMarkdownDaySessions(prog[day], conf)

def printMarkdownConfSessions(conf, name='', resetProgram=False):
    if (not ('program' in conf) or not conf['program'] or resetProgram):
        conf['program'] = getConfProgram(conf)
    printMarkdownProgSessions(conf['program'], name)
