from flask import *
from markupsafe import escape
import datetime
from literatureClient import DB
app = Flask(__name__)


@app.route('/')
def hello(): 
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())


@app.route(f'/<type>/<grade>_grade/')
def capitalize(type,grade):
    grade = escape(grade.capitalize())
    DF = DB(grade,type)
    author_datas = [[author, DF.get_bio(author)['img_src'],DF.get_bio(author)['bio'].replace('\n','<br>'),DF.get_books(author)]
                    for author in DF.authors]
    return render_template('authors_base.html', auth_datas=author_datas, grade=grade)


@app.route(f'/<type>/<grade>_grade/auth_ind=<int:auth_ind>')
def capitalize_(type,grade, auth_ind):
    DF = DB(grade,type)
    author=DF.authors[int(auth_ind)]
    return render_template('auth_main.html',auth_ind=auth_ind, author=author,img_src = DF.get_bio(author)['img_src'] , bio=DF.get_bio(author)['bio'].replace('\n','<br>'), books= DF.get_books(author))

@app.route(f'/<type>/<grade>_grade/auth_ind=<int:auth_ind>/book_ind=<int:book_ind>')
def capitalifzegh(type,grade, auth_ind,book_ind):
    DF= DB(grade,type)
    author=DF.authors[int(auth_ind)]
    book=DF.get_books(author)[int(book_ind)]
    DF_book = DF.get_content(author,book)
    return render_template('book_main.html',auth_ind=auth_ind,book_ind=book_ind, book_data=[DF_book[key].replace('\n','<br>') for key in DF_book.keys()], book=book, author=author,img_src = DF.get_bio(author)['img_src'])

app.run(host='0.0.0.0', port=81)