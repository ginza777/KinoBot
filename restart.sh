
git pull


sudo nginx -t
sudo systemctl daemon-reload




sudo systemctl restart bot_beat.service
sudo systemctl status bot_beat.service


sudo systemctl restart bot_worker.service
sudo systemctl status bot_worker.service


sudo systemctl restart bot
sudo systemctl status bot