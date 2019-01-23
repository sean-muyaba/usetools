#!/bin/sh

stamp="$(date '+%A %W %Y %X')"
# print log state line
echo "*******************************************************"
echo "                    $stamp                             "
echo "*******************************************************"

echo "*******************************************************"
echo "               Running scdl                             "
echo "*******************************************************"
/usr/bin/python3 /home/sean/.local/bin/scdl -l https://soundcloud.com/sean-muyaba -f --download-archive /home/sean/archive --addtofile --no-playlist-folder -c --path /media/sean/GoFlex\ Home/music/inbox/soundcloud/new/ >> /home/sean/logs/scdl.log
echo "*******************************************************"
echo "                                             "
echo "*******************************************************"
/usr/bin/python3 /home/sean/usetools/organise.py 
echo "*******************************************************"
echo "            SYNCING MUSIC TO SERVER                    "
echo "*******************************************************"
#/usr/bin/rsync -avzh --delete --existing /home/sean/Music/ /media/sean/GoFlex\ Home/music/
echo "*******************************************************"
echo "            SYNCING SERVER TO MUSIC                   "
echo "*******************************************************"
/usr/bin/rsync -avzh --delete /media/sean/GoFlex\ Home/music/ /home/sean/Music



