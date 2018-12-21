from flask import Flask, render_template
from config import *
import pymysql
app = Flask(__name__)
import config #将config文件与flask关联起来

def connectdb():
    db = pymysql.connect(host=HOST,user=USER,passwd=PASSWORD,db=DATABASE,port=PORT,charset=CHARSET)
    cursor = db.cursor()
    return (db, cursor)

def closedb(db, cursor):
    db.close()
    cursor.close()

@app.route('/')
def index():
    (db, cursor) = connectdb()
    cursor.execute("select * from news")
    items = cursor.fetchall()
    closedb(db, cursor)
    return render_template('yituo.html',title='智慧农业',items=items)

@app.route('/moreinfo')
def more_info():
    return '敬请期待'

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run()
