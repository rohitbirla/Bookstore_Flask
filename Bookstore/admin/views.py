from flask import Blueprint,render_template,redirect,url_for
from Bookstore import db
from Bookstore.models import Book
from Bookstore.admin.forms import AddBook



admin_blueprint = Blueprint('admin',__name__,template_folder='templates/admin')

@admin_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    form = AddBook()
    return render_template('admin/addBook.html',admin=True,form=form)