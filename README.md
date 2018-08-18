# ProfessionalNetworkingWebsite
Professional Networking Website

#run server
sudo /etc/init.d/nginx restart
uwsgi --socket PNsite.sock --wsgi-file PNsite/wsgi.py --chmod-socket=666
