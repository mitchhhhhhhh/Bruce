#imports necessary components
from flask import Flask, flash, render_template, g, request, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


#defines the databse as DATABASE
DATABASE = 'game_database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



@app.route('/')
def content():
    cursor = get_db().cursor()
    sql = "SELECT  content.id,content.image, content.Genre,content.name FROM content "
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor = get_db().cursor()
    sql = "SELECT genre.id,genre.genreName FROM genre "
    cursor.execute(sql)
    Genres = cursor.fetchall()
    return render_template("content.html", results=results, Genres=Genres)



@app.route('/Genre/<int:id>')
def genre(id):
    cursor = get_db().cursor()
    sql = "SELECT content.name,content.image, genre.genreName,content.id FROM content JOIN genre ON content.Genre = genre.id WHERE content.Genre = ?"
    cursor.execute(sql,(id,))
    results = cursor.fetchall()
    if len(results) > 0:
        sql = "SELECT genre.id,genre.genreName FROM genre "
        cursor.execute(sql)
        Genres = cursor.fetchall()
        return render_template("Genre.html", results=results,Genre=results[0][2], Genres=Genres)
    else:
        sql = "SELECT genre.id,genre.genreName FROM genre "
        cursor.execute(sql)
        Genres = cursor.fetchall()
        flash('sorry no games have been added to this genre as of now')
        return render_template("Genre.html", Genres=Genres)

@app.route('/Game/<int:id>')
def game(id):
    cursor = get_db().cursor()
    sql = "SELECT content.name, content.image, content.description,content.date FROM content WHERE id = ?"
    cursor.execute(sql,(id,))
    results = cursor.fetchall()
    sql = "SELECT genre.id,genre.genreName FROM genre "
    cursor.execute(sql)
    Genres = cursor.fetchall()
    return render_template("game.html", results=results,Desc=results[0][2],Title=results[0][0],Date=results[0][3],Genres=Genres)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    cursor = get_db().cursor()
    sql = "SELECT genre.id, genre.genreName FROM genre"
    cursor.execute(sql)
    results = cursor.fetchall()
    if request.method == 'POST':   
        t = request.form.get('title_name')
        d = request.form.get('desc_name')
        D = request.form.get('date_name')
        g = request.form.get('genre_name')
        f = request.files['file_name']
        pw = request.form.get('password')
        filename = secure_filename(f.filename)
        f.save('static/images/' + filename)
        if pw == "admin":    
            cursor = get_db().cursor()
            sql = "INSERT INTO content (name,description,date,Genre,image) VALUES (?,?,?,?,?)"
            print(filename)
            print(f)
            print(t,d,D,g,filename)
            data = (t,d,D,g,str(filename))
            cursor.execute(sql,data)
            get_db().commit()
            return redirect (url_for("content"))
        else:
            flash('incorrect password please try again')
            return redirect (url_for("upload_file"))
    cursor = get_db().cursor()
    sql = "SELECT genre.id,genre.genreName FROM genre "
    cursor.execute(sql)
    Genres = cursor.fetchall()
    return render_template ("uploadForm.html", results=results, Genres=Genres)


@app.route('/uploadGenre', methods=['GET','POST'])
def upload_Genre():
    if request.method == 'POST':  
        pww = request.form.get('password')
        Genre = request.form.get('genre') 
        if pww == "admin":
            cursor = get_db().cursor()
            sql = "INSERT INTO genre (genreName) VALUES (?)"
            cursor.execute(sql,(Genre,))
            get_db().commit()
            return redirect (url_for("content"))
        else:
            flash('incorrect password please try again')
            return redirect (url_for("upload_Genre"))
    cursor = get_db().cursor()
    sql = "SELECT genre.id,genre.genreName FROM genre "
    cursor.execute(sql)
    Genres = cursor.fetchall()
    return render_template ("uploadGenreForm.html", Genres=Genres)


@app.route('/CDG' , methods=['GET','POST'])
def choose_delete_game():
    cursor = get_db().cursor()
    sql = "SELECT  content.id,content.image, content.Genre,content.name FROM content "
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor = get_db().cursor()
    sql = "SELECT genre.id,genre.genreName FROM genre "
    cursor.execute(sql)
    Genres = cursor.fetchall()
    return render_template("ChooseGameDelete.html", results=results, Genres=Genres)

@app.route('/Delete/<int:id>', methods=['GET','POST'])
def delete(id): 
    cursor = get_db().cursor()
    sql = "SELECT  content.id,content.image, content.Genre,content.name FROM content WHERE id =?"
    cursor.execute(sql,(id,))
    results = cursor.fetchall()
    cursor = get_db().cursor()
    sql = "SELECT genre.id,genre.genreName FROM genre "
    cursor.execute(sql)
    Genres = cursor.fetchall()
    if request.method == 'POST':  
        password = request.form.get('password')
        if password == "admin": #;)
            cursor = get_db().cursor()
            sql = "DELETE FROM content WHERE id =?"
            cursor.execute(sql,(id,))
            get_db().commit()
            return redirect (url_for("content"))
        else:
            flash('incorrect password please try again')
            return redirect(url_for('delete', results=results,name=results[0][3],id = id, Genres=Genres))
    
    return render_template("delete.html", results=results,name=results[0][3],id = id, Genres=Genres)

    



if __name__ == "__main__":
    app.run(debug=True)