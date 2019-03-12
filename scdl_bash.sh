#!/bin/sh

stamp="$(date '+%A %W %Y %X')"
# print log state line
echo "*******************************************************"
echo "                    $stamp                             "
echo "*******************************************************"

echo "*******************************************************"
echo "               Running scdl                             "
echo "*******************************************************"
/usr/bin/python3 /usr/local/bin/scdl -l https://soundcloud.com/sean-muyaba -f --download-archive /home/sean/Documents/usetools/archive --addtofile --no-playlist-folder -c --path /home/sean/Music/music/inbox >> /home/sean/Music/music/inbox/scdl.log
echo "*******************************************************"
echo "            Sorting new music                          "
echo "*******************************************************"
/usr/bin/python3 /home/sean/Documents/usetools/organise.py 
echo "*******************************************************"
echo "            Sorting music library                      "
echo "*******************************************************"
/usr/bin/python3 /home/sean/Documents/usetools/organise.py --unorganised "/home/sean/Music/music/tech & house"
echo "*******************************************************"
echo "            SYNCING MUSIC TO SERVER                    "
echo "*******************************************************"
#/usr/bin/rsync -avzh --delete --existing /home/sean/Music/ /media/sean/GoFlex\ Home/music/
echo "*******************************************************"
echo "            SYNCING SERVER TO MUSIC                   "
echo "*******************************************************"
#/usr/bin/rsync -avzh --delete /media/sean/GoFlex\ Home/music/ /home/sean/Music



