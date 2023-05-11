#!/bin/bash

SFTP_HOST="access811863574.webspace-data.io"
SFTP_PASSWORD="Ru4free#Coffee?"
SFTP_USER="u99620396"
SOURCE="../_site/"
TARGET="ijcar-fscd-2020/"

lftp -e "set sftp:auto-confirm yes ; open sftp://$SFTP_HOST ; user $SFTP_USER $SFTP_PASSWORD; mirror --exclude-glob .git* --exclude .git/ --reverse --verbose --delete $SOURCE $TARGET; bye"
