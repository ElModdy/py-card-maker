# Card Maker
# Description

It's a python script that converts new [Squid](https://play.google.com/store/apps/details?id=com.steadfastinnovation.android.projectpapyrus) notes into [Anki](https://apps.ankiweb.net/) cards.\
To do this you need to have an rooted Android smartphone and give sudo permissions to the script which will then be able to read the memory area reserved by Android for Squid app and write to the [Ankidroid](https://play.google.com/store/apps/details?id=com.ichi2.anki) database.\
The loading of the cards is delegated to [card-proxy](https://github.com/ElModdy/card-proxy) which must therefore be installed.\
The script looks inside the notes for a yellow stroke which it will use as a delimiter between the front and back of the card as shown below.

![ANKI_VS_SQUID](https://user-images.githubusercontent.com/18534491/231198131-e7aa7993-b363-4b8b-8c2f-abad9626cf2e.jpg)

## Installation guide
```
pkg update
pkg upgrade
pkg install build-essential libjpeg-turbo nodejs git python pango
pip install cairocffi protobuf pypdf tinydb sqlite3
LDFLAGS=" -lm" pip install pillow
```

## Setup Termux Widget
```
cd ~/.shortcuts
mkdir tasks
cd tasks
ln -s ../../py-card-maker/script.sh make_cards
```
