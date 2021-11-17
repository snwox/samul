from flask import Flask,app,render_template
import os
from module import dbModule

if os.getenv("env") == "Dev":
    from config import Dev as CONF
else:
    from config import Production as CONF
app=Flask(__name__)
app.config.from_object(CONF)

db=dbModule.Database()
print(db)
@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)