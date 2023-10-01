# coding: utf-8
from flask import Flask, render_template, request, jsonify
from literatureClient import DB
from markupsafe import escape
import random


app = Flask(__name__)
# replace variable is a dictionary of replacement values for certain routes
replace={'review':'📗Аналізи','short':'📔Твори скорочено','audio':'🔉Аудіокниги творів','pres':'🎓Презентації'}

def type_to_ukr(type):
    """
    This function is used to translate the type of literature to Ukrainian
    """
    return type.replace('for','Світова').replace('ukr','Українська')

@app.route('/')
def home():
    """
    This function is used to handle the home page of the website
    """
    # Get the data for the different blocks to be displayed on the home page
    blocks = [[[type,grade,str(type_to_ukr(type)),str(DB(grade,type).get_rnd()['img_src'])] for type in ['for','ukr'] ] for grade in range(5,12)  ]
    # Render the home page template and pass in the data for the blocks
    return render_template('index.html',link_q = random.randint(1,390), blocks = blocks)


@app.route(f'/<type>/<grade>_grade/')
def choose_auth(type,grade):
    """
    This function is used to handle the page that displays a list of authors
    """
    # Escape the grade variable to prevent against potential XSS attacks
    grade = escape(grade.capitalize())
    # Create an instance of the DB class
    DF = DB(grade,type)
    # Get the data for each author
    author_datas = [[author, DF.get_bio(author)['img_src'],DF.get_bio(author)['bio'].replace('\n','<br>'),DF.get_books(author)] for author in DF.authors]
    # Render the authors template and pass in the data for each author
    return render_template('authors_base.html', grade=grade,type = type_to_ukr(type), type_l = type, auth_datas=author_datas)

@app.route(f'/<type>/<grade>_grade/<adding>')
def adding(type,grade,adding):
    """
    This function is used to handle the page that displays a list of books or presentations
    """
    DF = DB(grade,type)
    # Get the data for the specific type of adding
    adding_auth = DF.get_adding(replace[adding])
    auth_datas_simple = [[author, DF.get_bio(author[1:])['img_src']] for author in adding_auth.keys()]
    # Render the adding template and pass in the data for each author
    return render_template('adding_base.html', adding_l = adding, adding = replace[adding],grade=grade,type = type_to_ukr(type), type_l = type, auth_datas_simple=auth_datas_simple)

@app.route(f'/<type>/<grade>_grade/auth_ind=<int:auth_ind>')
def author(type,grade, auth_ind):
    """
    This function is used to handle the page that displays information about a specific author
    """
    DF = DB(grade,type)
    # Get the data for the specified author
    author=DF.authors[int(auth_ind)]
    img_src = DF.get_bio(author)['img_src']
    bio=DF.get_bio(author)['bio']
    books= DF.get_books(author)
    # Render the author template and pass in the data for the author
    return render_template('auth_main.html',auth_ind=auth_ind, author=author,grade=grade,type = type_to_ukr(type), type_l = type,img_src = img_src , bio=bio, books= books)

@app.route(f'/<type>/<grade>_grade/<adding>/auth_ind=<int:auth_ind>')
def adding_auth(type,grade,adding,auth_ind):
    """
    This function is used to handle the page that displays information about a specific book or presentation
    """
    DF = DB(grade,type)
    ADD = DF.get_adding(replace[adding])
    # Get the data for the specified author
    author= list(ADD.keys())[int(auth_ind)]
    img_src = DF.get_bio(author[1:])['img_src']
    auth_data=''
    if adding == 'pres':
        auth_data = ADD[author]
    else:
        for index, book in enumerate(list(ADD[author].keys())):
            auth_data+= f'<a href = "auth_ind={auth_ind}/book_ind={index}">{book}</a>'
    # Render the adding author template and pass in the data for the author
    return render_template('adding_auth_main.html', 
                           adding_l = adding, adding = replace[adding],grade=grade,type = type_to_ukr(type), 
                           type_l = type,img_src = img_src, auth_data = auth_data)
@app.route(f'/<type>/<grade>_grade/auth_ind=<int:auth_ind>/book_ind=<int:book_ind>')
def book(type,grade, auth_ind,book_ind):
    """
    This function is used to handle the page that displays information about a specific book
    """
    DF= DB(grade,type)
    # Get the data for the specified author and book
    author=DF.authors[int(auth_ind)]
    book=DF.get_books(author)[int(book_ind)]
    DF_book = DF.get_content(author,book)
    book_data =[DF_book[key].replace('\n','<br>') for key in DF_book.keys()]
    img_src = DF.get_bio(author)['img_src']
    # Render the book template and pass in the data for the book
    return render_template('book_main.html', grade=grade,type = type_to_ukr(type), type_l = type, auth_ind = auth_ind,book_ind = book_ind, book_data=book_data, book=book, author=author,img_src = img_src)
@app.route(f'/<type>/<grade>_grade/<adding>/auth_ind=<int:auth_ind>/book_ind=<int:book_ind>')
def adding_book(type,grade,adding,auth_ind,book_ind):
    """
    This function is used to handle the page that displays information about a specific short story or audio book
    """
    DF = DB(grade,type)
    ADD = DF.get_adding(replace[adding])
    # Get the data for the specified author and book
    author= list(ADD.keys())[int(auth_ind)]
    img_src = DF.get_bio(author[1:])['img_src']
    auth_data=''
    book = list(ADD[author].keys())[book_ind]
    part = ADD[author][book]
    # Render the adding book template and pass in the data for the book
    return render_template('adding_book_main.html', 
                           adding_l = adding, adding = replace[adding],grade=grade,type = type_to_ukr(type), 
                           type_l = type,img_src = img_src, auth_ind= auth_ind,book_ind = book_ind, part = part, author = author, book = book)

# Run the app when the script is executed
# if __name__ == '__main__':
#     vercel(app)
