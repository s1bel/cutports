# cutports

Excludes ports from ports range

2 versions:
1) cutports.py - for local python execution
2) main.py, config.py, bigholecutterbot.service - version adapted for telegram bot 

## Add packages to use telebot library:
pip install pyTelegramBotAPI


## Install as service for Debian 12:

edit and save /lib/systemd/system/bigholecutterbot.service

systemctl daemon-reload

systemctl enable bigholecutterbot

systemctl start bigholecutterbot

systemctl status bigholecutterbot
