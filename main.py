from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
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
        return o + '의 이름으로 저장되었습니다.'

@app.route('/fileLoad')
def get_image():
    filename = request.args.get('name')
    return send_file('imgs/' + filename, mimetype='image/png')
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')