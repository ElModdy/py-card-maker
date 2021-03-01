# Card Maker

## Installation guide
```
pkg update
pkg upgrade
pkg install build-essential libjpeg-turbo nodejs git python pango
pip install cairocffi protobuf pypdf tinydb sqlite3
LDFLAGS=" -lm" pip install pillow
```

## Termux Widget
```
cd ~/.shortcuts
mkdir tasks
cd tasks
ln -s ../../py-card-maker/script.sh make_cards
```
