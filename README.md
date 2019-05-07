![PriCoSha](https://i.gyazo.com/184f69f915334ca8a29d9fb639080be5.png)
# PriCoSha 2.0
A Flask application that allows users to create and share content items among groups of other users, enhanced with cryptographic methods to increase security measures. 

## How to run
1. Make sure to install needed Python libraries: 
    `pip install flask flask_uploads pymysql flask-scrypt flask_kvsession pycryptodome`. You also need to install redis separately on your computer, which can be done via `brew install redis` (Mac), through [downloadable zip files for Windows](https://github.com/dmajkic/redis/downloads), or [Ubuntu](https://tosbourn.com/install-latest-version-redis-ubuntu/).
2. Obtain a self-signed certificate & key (`localhost.crt`, `localhost.key`) 
3. Dump database schema into a db (name it `pricosha`) and start your SQL server and redis server via `redis-server` (for Windows just click the `redis-server` executable).
4. Run `python init.py` in command prompt or terminal at the root folder of this project.
5. Should be running at `https://localhost:5000`!

## Added Security Features
- Use of flask-scrypt to hash+salt passwords, and included salts in db
- Convert to https using SSL/TLS X509 certificate
- Use redis & flask-kvsession to store session cookies & delete to prevent session replay attacks

## Available Features
- Login
- View content items and information
- Manage tags
- Post a content item
- Tag a content item
- Add friend
- Feature No. 1 - Create/delete/defriend friend group
- Feature No. 2 - Update/delete content items
- Feature No. 3 - Like/Dislike feature for content item
- Feature No. 4 - Profile page for users

## Screenshots
<img src="static/createGroup.png" width="200px">    <img src="static/friendspage.png" width="200px">
