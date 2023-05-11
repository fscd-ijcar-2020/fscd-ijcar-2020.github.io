#!/usr/bin/python

# dir: /Users/guerrini/Lavoro/Servizi/Organizzazione/FSCD/FSCD-IJCAR-20/web-common.git/scripts/python

import sys

from YamlProgramLib import printYamlConfProgram

from MarkdownProgramLib import printMarkdownConfSessions

exec(open('conf-data.py').read())

if (len(sys.argv) == 1 or not (sys.argv[1] in conferences.keys())):
    print ('Usage: python scrap-program.py <conf-name>')
    print('Available conferences:')
    for conf in conferences.keys():
        print('-', conf)
else:
    # sys.stdout = open(sys.argv[1]+'.yaml', 'w')
    printYamlConfProgram(conferences[sys.argv[1]])
    printMarkdownConfSessions(conferences[sys.argv[1]], sys.argv[1])
