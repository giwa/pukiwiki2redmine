from flask import Flask, render_template, request, redirect, url_for
from puki2redmine import Puki2Redmine


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/convert", methods=['POST', 'GET'])
def convert():
    if request.method != 'POST':
        return redirect(url_for('index'))
    pukitext = request.form['pukitext']
    p2r = Puki2Redmine(pukitext.splitlines())
    redminetext = "\n".join(p2r.convert())

    return render_template('index.html', redminetext=redminetext,
                           pukitext=pukitext)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
