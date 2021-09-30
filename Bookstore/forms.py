from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,TextAreaField,SubmitField,HiddenField
from flask_wtf.file  import FileField,FileAllowed
from flask_uploads import IMAGES

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