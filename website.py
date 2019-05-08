from flask import Flask, render_template, request, redirect
import os
from os import walk
import shelve
import shutil


app = Flask(__name__, static_url_path='/static', static_folder='./templates/static')


@app.route('/')
def home():
    mypath = "/Users/haroonkhazi/desktop/eecs377/final_project/videos/"
    imagepath = "/Users/haroonkhazi/desktop/eecs377/final_project/templates/static/"
    files = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        files.extend(filenames)
        break
    db = shelve.open('images.db')
    for f in files:
        if f in db:
            continue
        else:
            shutil.copy2(os.path.join(mypath, f), imagepath)
            db[f]=1
    db.close()
    files =[]
    for (dirpath, dirnames, filenames) in walk(imagepath):
        files.extend(filenames)
        break
    files = [f for f in files if "picture" in f]
    files.sort()
    return render_template('home.html', files=files)

@app.route('/done')
def done():
    imagepath = "/Users/haroonkhazi/desktop/eecs377/final_project/templates/static/"
    files = []
    for (dirpath, dirnames, filenames) in walk(imagepath):
        files.extend(filenames)
        break
    files = [f for f in files if "video" in f]
    files.sort()
    print(files)
    return render_template('video.html', files=files)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
