gnome-terminal --title 'subscriber-fuel' --geometry=76x18+1010+0 -- /bin/bash -c 'python sensor_sub1.py;exec bash'\
& gnome-terminal --title 'subscriber-tire' --geometry=76x18+0+540 -- /bin/bash -c 'python sensor_sub2.py;exec bash'\
& gnome-terminal --title 'subscriber-engine' --geometry=76x18+1010+540 -- /bin/bash -c 'python sensor_sub3.py;exec bash'\
& gnome-terminal --title 'publisher' --geometry=76x18+0+0 -- /bin/bash -c 'python sensor_pub.py;exec bash'