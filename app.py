from Bookstore import app,db,photos
from flask import render_template,redirect,url_for
from Bookstore.forms import AddBook,AddToCart
from Bookstore.models import Book



@app.route('/')
def index():
    
    return render_template('index.html')


@app.route('/book/<id>')
def book(id):
    book = Book.query.filter_by(id=id).first()

    form = AddToCart()

    return render_template('view-book.html', book=book, form=form)

@app.route('/admin')
def admin():
    return render_template('admin/index.html')

@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = AddBook()

    if form.validate_on_submit():
        image_url = photos.url(photos.save(form.image.data))

        new_book = Book(name=form.name.data,price=form.price.data, stock=form.stock.data, description=form.description.data, image=image_url)

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('admin/addBook.html', admin=True, form=form)

    
if __name__ == '__main__':
    app.run(debug=True)
