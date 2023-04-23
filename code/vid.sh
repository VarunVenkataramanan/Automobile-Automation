gnome-terminal --title 'subscriber' --geometry=76x18+1010+0 -- /bin/bash -c 'python vid_sub.py;exec bash'\
& gnome-terminal --title 'publisher' --geometry=76x18+0+0 -- /bin/bash -c 'python vid_pub.py;exec bash'
