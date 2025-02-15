# cutports

2 versions:
1) cutports.py - for local python execution
2) main.py, config.py - version adapted for telegram bot 

Add packages to use telebot:
pip install pyTelegramBotAPI

install as service for Debian 12:
edit and save /lib/systemd/system/bigholecutterbot.service
systemctl daemon-reload
systemctl enable bigholecutterbot
systemctl start bigholecutterbot
systemctl status bigholecutterbot
