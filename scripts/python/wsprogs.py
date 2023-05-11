import yaml

def numberSessions(conf):
    n = 0
    for day in conf['program']:
        if 'sessions' in day:
            for session in day['sessions']:
                n += 1
                session['num'] = n
    return n

def printMarkdownTalk(file, talk, num):
    file.write('<li>\n')
    if (type(talk['time']) == str):
        # print('str:', talk['time'])
        file.write('{}: '.format(talk['time']))
    else:
        print('couple:', talk['time'])
        file.write('{:02d}:{:02d}: '.format(int(talk['time'][0]), int(talk['time'][1])))
    if 'authors' in talk:
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

def printMarkdownSession(session, conf='', dir='.'):
    if (session['type'] != 'talks' or not 'talks' in session):
        return
    if 'track' in session:
        track = session['track']
    else:
        track = ''
    if (conf):
        fname = '{}-session{}{}'.format(conf, session['num'], track)
    else:
        fname = 'session{}{}'.format(session['num'], track)
    fullname = '{}/{}.html'.format(dir, fname)
    file = open(fullname, 'w')
    file.write("""---
permalink: /wsprogram/sessions/{}
published: true
---

<div class="cd-schedule-modal__event-info">
	<div>
""".format(fname))
    if 'chairs' in session:
        file.write("<p>Chair: {}</p>\n".format(', '.join(session['chairs'])))
    if 'talks' in session:
        printMarkdownTalks(file, session['talks'])
    file.write("""
    </div>
</div>
""")
    file.close()

def printMarkdownDaySessions(sessions, conf='', dir='.'):
    for session in sessions:
        printMarkdownSession(session, conf, dir)

def printMarkdownProgSessions(prog, conf='', dir='.'):
    for day in prog:
        if ('sessions' in day):
            printMarkdownDaySessions(day['sessions'], conf, dir)

##

workshops = [
        {
            'file': 'linearityTLLA',
            'acronym': 'Linearity & TLLA',
            'form': 'Linearity & TLLA (Joint Workshop on Linearity and Trends in Linear Logic and Applications, June 29-30)'
        },
        {
            'file': 'unif',
            'acronym': 'UNIF',
            'form': 'UNIF (Workshop on Unification, June 29)'
        },
        {
            'file': 'wpte',
            'acronym': 'WPTE',
            'form': 'WPTE (Workshop on Rewriting Techniques for Program Transformations and Evaluation, June 29)'
        },
        {
            'file': 'pg',
            'acronym': 'Proof Ground',
            'form': 'Proof Ground (June 29)'
        },
        {
            'file': 'lfmtp',
            'acronym': 'LFMTP',
            'form': 'LFMTP (Logical Frameworks and Meta-Languages: Theory and Practice, June 29-30)'
        },
        {
            'file': 'wil',
            'acronym': 'WiL',
            'form': 'WiL (Women in Logic, June 30)'
        },
        {
            'file': 'iwc',
            'acronym': 'IWC',
            'form': 'IWC (International Workshop on Confluence, June 30)'
        },
        {
            'file': 'ifip',
            'acronym': 'IFIP WG 1.6',
            'form': 'IFIP WG 1.6 (June 30)'
        },
        {
            'file': 'isabelle',
            'acronym': 'Isabelle Workshop',
            'form': 'Isabelle Workshop (June 30)'
        },
        {
            'file': 'paar',
            'acronym': 'PAAR',
            'form': 'PAAR (Practical Aspects of Automated Reasoning, June 30)'
        },
        {
            'file': 'hott-uf',
            'acronym': 'HoTT/UF',
            'form': 'HoTT/UF (Homotopy Type Theory/Univalent Foundations, July 5-6)'
        },
        {
            'file': 'geocat',
            'acronym': 'GeoCat',
            'form': 'GeoCat (Geometric and Categorical Structures for Computation and Deduction, July 5-6)'
        },
        {
            'file': 'coq',
            'acronym': 'The Coq Workshop',
            'form': 'The Coq Workshop (July 5-6)'
        },
        {
            'file': 'smt',
            'acronym': 'SMT',
            'form': 'SMT (Satisfiability Modulo Theories, July 5-6)'
        },
        {
            'file': 'termgraph',
            'acronym':
            'TERMGRAPH',
            'form': 'TERMGRAPH (July 5)'
        }
    ]

# #####
scriptdir = "/Users/guerrini/Lavoro/Servizi/Organizzazione/FSCD/FSCD-IJCAR-20/web-common.git/scripts/python"

# yaml relative path
yamldir = "../../_data/conference/programs"

# session file relative path
sessdir = "../../_2018_pages/wsprogram/sessions"

import os

for ws in workshops:
    confname = ws['file']
    # print(os.path.exists(fname+'.yml'))
    fname = '{}/{}/{}'.format(scriptdir, yamldir, confname)
    if not os.path.exists(fname+'.yml'):
        continue
    yamlFile = open(fname+'.yml', 'r')
    conf = yaml.load(yamlFile, Loader=yaml.BaseLoader)
    # to number sessions
    # numberSessions(conf)
    # newYamlFile = open(fname+'.new.yml', 'w')
    # newyaml = yaml.dump(conf)
    # newYamlFile.write(newyaml)
    newYamlFile.close()
    abssessdir = '{}/{}'.format(scriptdir, sessdir)
    printMarkdownProgSessions(conf['program'], confname, abssessdir)