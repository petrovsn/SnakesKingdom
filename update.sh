sudo systemctl stop snakes_kingdom.service
git stash
git pull
sudo systemctl restart snakes_kingdom.service
rm -rf /var/www/snakes2/*
cp -r /root/Games/SnakesKingdom/front/dist/* /var/www/snakes2/