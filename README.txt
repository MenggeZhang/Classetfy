HOW TO RUN PROPJECT

I. LOCALLY
1. Make sure change RF_MODEL_PATH in constants.py to a local path.
2. python3 run.py
3. Go to browser.

II. ON (NGINX-ENABLED) SERVER
1. Transfer the classetfy/ folder to server using scp or rsync
2. Make sure change RF_MODEL_PATH in constants.py to a path of the project on server.
3. Make sure Nginx is installed and create the following file "application" with content:

(base) ubuntu@ip-172-31-7-29:~$ cat /etc/nginx/sites-available/application
server {
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /static {
        alias /home/ubuntu/application/flaskexample/static;
    }
}

4. Symlink as 
sudo ln -s /etc/nginx/sites-available/application /etc/nginx/sites-enabled/application

5. Start Nginx
sudo /etc/init.d/nginx start

6. Open a tmux session and run gunicorn (having the classefy/ at the same level)

gunicorn classetfy:app

7. Website is up and running!

III. Install conda environment by running:

conda env create -f environment.yml