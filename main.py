""" main server """
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pymysql
app = Flask(__name__)

@app.route('/upload')
def render_file():
    return render_template('upload.html')

@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        result = request.form

        f = request.files['file']
        t = result.get('title')
        u = result.get('user')
        o = secure_filename(u + '/'+f.filename)
        f.save('imgs' + '/' + o)
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='user', charset='utf8')
        try:
            cursor = db.cursor()
            sql = "INSERT INTO main (title, username, score, link) VALUES ('%s', '%s', 1, '%s')" % (t, u, o)
            print(sql)
            cursor.execute(sql)
            db.commit()
        finally:
            db.close()
        return 'http://3.134.96.11:5000/fileLoad?name=' + o + '    에 저장되었습니다.'
    elif request.method == 'GET':
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='user', charset='utf8')
        try:
            cursor = db.cursor()
            sql = "SELECT * FROM main ORDER BY score ASC"
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            return str(result)
        finally:
            db.close()


@app.route('/fileLoad')
def get_image():
    filename = request.args.get('name')
    return send_file('imgs/' + filename, mimetype='image/png')

@app.route('/fileUp', methods = ['GET', 'POST'])
def update_score():
    if request.method == 'POST':
        filename = request.args.get('name')

        try:
            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='user', charset='utf8')
            cursor = db.cursor()
            sql = "UPDATE main SET score = score + 1 WHERE link = '%s'" % filename
            print(sql)
            cursor.execute(sql)
            db.commit()
            return 'SUCCESS!'
        finally:
            db.close()
    else:
        return 'YOU NEED POST'
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
