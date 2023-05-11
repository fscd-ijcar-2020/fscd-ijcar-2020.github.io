#!/usr/bin/python

# dir: /Users/guerrini/Lavoro/Servizi/Organizzazione/FSCD/FSCD-IJCAR-20/web-common.git/scripts/python

from ScrapProgramLib import getConfProgram
from PanelsLib import printDayPanels

exec(open('conf-data.py').read())

for conf in conferences.values():
    if (not ('program' in conf) or not conf['program'] or resetProgram):
        conf['program'] = getConfProgram(conf)
    for day in conf['program']:
        printDayPanels(conf, day)
