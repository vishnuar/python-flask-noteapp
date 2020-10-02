from flask import Flask, render_template,request, redirect, session, flash
from flask_bootstrap import Bootstrap
import requests
from flask_mysqldb import MySQL

app = Flask(__name__)
Bootstrap(app)

app.config['MYSQL_HOST'] = 'vishnuar.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'vishnuar'
app.config['MYSQL_PASSWORD'] = 'qatest123$$1'
app.config['MYSQL_DB'] = 'vishnuar$todo'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'secret'

@app.route('/noteapp')
def basenote():
    if session:
        userid = session['id']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM mytodo WHERE user_id = %s",[int(userid)])
        if resultValue > 0:
            blogs = cur.fetchall()
            cur.close()
            return render_template('index.html', blogs=blogs)
        cur.close()
        return render_template('index.html', blogs=None)
    else:
        return redirect('/login')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register.html')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(first_name, last_name, username, email, password) "\
        "VALUES(%s,%s,%s,%s,%s)",(userDetails['first_name'], userDetails['last_name'], \
        userDetails['username'], userDetails['email'], userDetails['password']))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM user WHERE username = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['firstName'] = user['first_name']
                session['lastName'] = user['last_name']
                session['id'] = user['user_id']
                flash('Welcome ' + session['firstName'] +'! You have been successfully logged in', 'success')
            else:
                cur.close()
                flash('Password does not match', 'danger')
                return render_template('login.html')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login.html')
        cur.close()
        return redirect('/noteapp')
    return render_template('login.html')

@app.route('/notes/<int:id>/')
def blogs(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM mytodo WHERE todo_id = {}".format(id))
    if resultValue > 0:
        blog = cur.fetchone()
        return render_template('note.html', blog=blog)
    return 'Note not found'

# Write a new note
@app.route('/write-note/',methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        blogpost = request.form
        title = blogpost['title']
        body = blogpost['body']
        userid = session['id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mytodo(user_id, title, body) VALUES(%s, %s, %s)", (int(userid), title, body))
        mysql.connection.commit()
        cur.close()
        flash("Successfully posted a new note", 'success')
        return redirect('/noteapp')
    return render_template('write_note.html')

# View my notes
@app.route('/my-notes/')
def view_blogs():
    userid = session['id']
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM mytodo WHERE user_id = %s",[int(userid)])
    if result_value > 0:
        my_blogs = cur.fetchall()
        return render_template('my_notes.html',my_blogs=my_blogs)
    else:
        return render_template('my_notes.html',my_blogs=None)

# Edit blog
@app.route('/edit-note/<int:id>/', methods=['GET', 'POST'])
def edit_blog(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        title = request.form['title']
        body = request.form['body']
        cur.execute("UPDATE mytodo SET title = %s, body = %s where todo_id = %s",(title, body, id))
        mysql.connection.commit()
        cur.close()
        flash('Note updated successfully', 'success')
        return redirect('/notes/{}'.format(id))
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM mytodo WHERE todo_id = {}".format(id))
    if result_value > 0:
        blog = cur.fetchone()
        blog_form = {}
        blog_form['title'] = blog['title']
        blog_form['body'] = blog['body']
        return render_template('edit_note.html', blog_form=blog_form)

@app.route('/delete-note/<int:id>/')
def delete_blog(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM mytodo WHERE todo_id = {}".format(id))
    mysql.connection.commit()
    flash("Your note has been deleted", 'success')
    return redirect('/my-notes')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/logout/')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=False)