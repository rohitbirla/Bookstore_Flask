from flask import Flask,redirect,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField,TextAreaField,HiddenField
from flask_uploads import UploadSet, configure_uploads
from flask_wtf.file import FileField, FileAllowed


app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trendy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Book(db.Model):
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer) #in cents
    stock = db.Column(db.Integer)
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))


class AddBook(FlaskForm):
    name = StringField('Name')
    price = IntegerField('Price')
    stock = IntegerField('Stock')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(IMAGES, 'Only images are accepted.')])
    submit = SubmitField('Save')

class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')
    id = HiddenField('ID')

@app.route('/')
def index():
    books=Book.query.all()
    
    return render_template('index.html',books=books)


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
    app.run()


