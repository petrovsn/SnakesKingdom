sudo cp *.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl restart snakes_kingdom.service
rm -rf /var/www/snakes2/*
cp -r /root/Games/SnakesKingdom/front/dist/* /var/www/snakes2/