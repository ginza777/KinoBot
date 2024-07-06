
git pull


sudo nginx -t
sudo systemctl daemon-reload




sudo systemctl start bot_beat.service
sudo systemctl enable bot_worker.service
sudo systemctl restart bot_beat.service
sudo systemctl status bot_beat.service


sudo systemctl start bot_worker.service
sudo systemctl enable bot_worker.service
sudo systemctl restart bot_worker.service
sudo systemctl status bot_worker.service


sudo systemctl start bot
sudo systemctl enable bot
sudo systemctl restart bot
sudo systemctl status bot