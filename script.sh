#!/data/data/com.termux/files/usr/bin/bash


cd "$(dirname "$(realpath "$0")")"
tsudo chmod -R 777 /data/data/com.steadfastinnovation.android.projectpapyrus
python main.py
