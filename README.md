![PriCoSha](https://i.gyazo.com/184f69f915334ca8a29d9fb639080be5.png)
# PriCoSha
A Flask application that allows users to create and share content items among groups of other users.

## How to run
1. Make sure to install needed Python libraries: 
    `pip install flask flask-login flask_uploads pymysql flask-scrypt`
2. Dump database schema into a db (name it `pricosha`) and start your SQL server.
3. Run `python init.py` in command prompt or terminal at the root folder of this project.
4. Should be running at `localhost:5000`!

## Added Security Features
- Use of flask-scrypt to hash+salt passwords, and included salts in db
- Convert to https using SSL/TLS X509 certificate 
- Protection against CSRF and XSS

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
- Feature No. 5 - Add comments

## Screenshots
<img src="static/createGroup.png" width="200px">    <img src="static/friendspage.png" width="200px">    <img src="static/homepage.png" width="200px">
