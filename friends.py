from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import getfriends

@app.route('/friends')
def friends():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    # gotta update this data every time someone successfully adds a user
    friends = getfriends.getFriend()
    session['users'][session['username']]['friends'] = friends

    gname_list = []
    for group in session['users'][session['username']]['groups']:
        gname_list.append(group['group_name'])

    gname_list = session['users'][session['username']]['groups']

    # get all the groups the person is the owner of
    query = 'SELECT group_name FROM `friendgroup` WHERE username = %s'
    groups = getData(query, session['username'])
    allGroups = []
    for group in groups:
        allGroups.append(group['group_name'])
    return render_template('friends.html', data=friends, gname_list=gname_list, groups=allGroups)

@app.route('/delete-<user>-from-<group>')
def deleteFriends(user, group):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    command = "DELETE FROM member \
                WHERE group_name = %s AND username="+ "'" + user + "'"
    execute(command, (group))
    return redirect(url_for('friends'))

@app.route('/addFriends')
def addFriends():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    cursor = conn.cursor()
    groupQuery = 'SELECT * FROM `friendgroup` WHERE username = %s'
    cursor.execute(groupQuery, session['username'])
    group = cursor.fetchall()
    cursor.close()

    return render_template('addFriends.html', data=group)

@app.route('/addingFriends', methods=['GET', 'POST'])
def addingFriends():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    groupQuery = 'SELECT group_name FROM `friendgroup` WHERE username = %s'
    group = getData(groupQuery, session['username'])

    #checks if user owns any groups, else error
    countGroupQuery = 'SELECT COUNT(*) FROM friendgroup WHERE username = %s'
    countGroupData = getData(countGroupQuery, session['username'])

    if (countGroupData[0]['COUNT(*)'] < 1):       
        error = "Did not select a friendgroup first, or incorrect name."
        return render_template("addFriends.html", data=group, error=error)

    if (len(group) == 0):
        error = "Please include a group name or a user's name"
        return render_template('addFriends.html', error=error, data=group)

    # creating variables from the form
    formGroup = request.form['group']
    fullname = request.form['name']
    first_name = ""
    last_name = ""

    # checks if username field is filled
    # username field is filled only if there
    # are two people with the same first and last name
    username = request.form.get('username', None)

    # if user entered a proper first name and last name
    if len(fullname.split()) == 2:
        first_name = fullname.split()[0]
        last_name = fullname.split()[1]
    else:
        error = "Please enter a first name and a last name."
        return render_template('addFriends.html', error=error, data=group)

    # if the username parameter is not filled, check for the username
    # with the person's first and last name
    if (username is None):

        # finding username with the entered first and last name
        cursor = conn.cursor()
        query = "SELECT username \
                    FROM person \
                    WHERE first_name = %s \
                    AND last_name = %s"
        cursor.execute(query, (first_name, last_name))
        userData = cursor.fetchall()
        cursor.close()

        # if there are multiple users with the same first and last name
        if (len(userData) > 1):
            error = "Please include a username."
            return render_template('addFriends.html', error=error, data=group)
        # if the user cannot be found, send an error message
        elif (len(userData) < 1):
            error = "User not found."
            return render_template('addFriends.html', error=error, data=group)       

        isOwner = False
        cursor = conn.cursor()
        query = "SELECT username \
                    FROM friendgroup \
                    WHERE username = %s "
        cursor.execute(query, (userData[0]['username']))
        ownerData = cursor.fetchall()
        cursor.close()

        for data in ownerData:
            if data['username'] == userData[0]['username']:
                isOwner = True
        
        isMember = False
        cursor = conn.cursor()
        query = "SELECT username \
                    FROM member \
                    WHERE username = %s "
        cursor.execute(query, (userData[0]['username']))
        memberData = cursor.fetchall()
        cursor.close()

        for data in memberData:
            if data['username'] == userData[0]['username']:
                isMember = True
                
        #if user already in the group or is group owner, send error message
        if (isOwner):
            error = "Already the group owner or a group member."
            return render_template('addFriends.html', error=error, data=group)
        elif (isMember):
            error = "Already a group member or the group owner."
            return render_template('addFriends.html', error=error, data=group)
        else:
            query = "INSERT INTO member (username, group_name, username_creator) VALUES (%s, %s, %s)"
            cursor = conn.cursor()
            cursor.execute(query, (userData[0]['username'], formGroup, session['username']))
            conn.commit()
            cursor.close()
            return redirect(url_for('friends'))
    else:
        cursor = conn.cursor()
        query = "SELECT username \
                FROM person \
                WHERE username = %s"
        cursor.execute(query, (username))
        data = cursor.fetchone()
        cursor.close()


        # if the username is collected
        if (data):
            data=group
            for mem in group:
                if (mem['group_name'] == formGroup):
                    error = "This person is already in the group!"
                    return render_template('addFriends.html', error=error,data=group)

            query = "INSERT INTO member (username, group_name, username_creator) VALUES (%s, %s, %s)"
            cursor = conn.cursor()
            cursor.execute(query, (data['username'], formGroup, session['username']))
            conn.commit()
            cursor.close()
            return redirect(url_for('friends'))
        else:
            error = "Username was not found. Please enter a valid one."
            return render_template('addFriends.html', error=error,data=group)
    return render_template('addFriends.html')    

@app.route('/createFriend', methods=['GET', 'POST'])
def createFriend():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    return render_template('createFriend.html')

@app.route('/creatingFriends', methods=['GET', 'POST'])
def creatingFriends():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    # get all the info from the form
    groupName = request.form['name']
    description = request.form["description"]
    data = request.form

    #check if group name too long
    if len(groupName) > 50:
        error = "Group name too long. 50 characters max."
        return render_template('createFriend.html', error=error)
        
    # check if group name exists
    query = "SELECT COUNT(group_name) FROM friendgroup WHERE group_name = %s"
    allGroups = getData(query, groupName)

    if (allGroups[0]['COUNT(group_name)'] == 1):
        error = "The group name already exists. Please enter another one."
        return render_template('createFriend.html', error=error)
    else:
        cursor = conn.cursor()
        command = "INSERT INTO friendgroup (group_name, username, description) VALUES (%s, %s, %s)"
        cursor.execute(command, (groupName, session['username'], description))
        conn.commit()
        cursor.close()


        # create a query for each member
        cursor = conn.cursor()
        stuff = []
        exclude = ["name", "description"]
        for member in data:
            if (member not in exclude):

                query = "INSERT INTO member (username, group_name, username_creator) VALUES (%s, %s, %s)"
                cursor.execute(query, (member, groupName, session['username']))
                conn.commit()
        cursor.close()
    return redirect(url_for('friends'))

def getData(query, param):
    cursor = conn.cursor()
    cursor.execute(query, (param))
    data = cursor.fetchall()
    cursor.close()
    return data

def execute(query, param):
    cursor = conn.cursor()
    cursor.execute(query, (param))
    conn.commit()
    cursor.close()
    return
