#!/bin/sh

stamp="$(date '+%A %W %Y %X')"
# print log state line
echo "*******************************************************"
echo "                    $stamp                             "
echo "*******************************************************"
/usr/bin/python3 /home/sean/.local/bin/scdl -l https://soundcloud.com/sean-muyaba -f --download-archive /home/sean/archive --addtofile --no-playlist-folder -c --path /media/sean/GoFlex\ Home/music/inbox/soundcloud/new/
