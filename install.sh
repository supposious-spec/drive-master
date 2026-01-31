#!/usr/bin/env bash

echo "Drive Master tool install ho raha hai..."

# Dependencies
if ! command -v python3 &> /dev/null; then
    echo "Python3 install kar rahe hain..."
    sudo apt update && sudo apt install -y python3 python3-pip
fi

if ! python3 -c "import click" &> /dev/null 2>&1; then
    echo "Click install kar rahe hain..."
    pip3 install click
fi

# Tool install GitHub se
pip3 install git+https://github.com/supposious-spec/drive-master.git

echo "Done! Ab 'drive-master' run karo menu ke liye ya 'drive-master coding' direct mount ke liye."
echo "Agar command nahi chal raha: export PATH=\"$HOME/.local/bin:$PATH\" aur source ~/.bashrc"