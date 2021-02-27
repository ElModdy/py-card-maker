#!/data/data/com.termux/files/usr/bin/bash


tsudo chmod -R 777 /data/data/com.steadfastinnovation.android.projectpapyrus
tsudo cp /data/data/com.steadfastinnovation.android.projectpapyrus/databases/papyrus.db ./ 

echo "kadha"
python main.py
echo "kshfkkkk"
