"Demo Flask application"
import json
import os
import subprocess
import urllib.request

from flask import Flask, render_template, render_template_string, url_for, redirect, flash, g
from flask_wtf import FlaskForm
#from flask_wtf.file import FileField
from wtforms import StringField, HiddenField, validators, DecimalField
from flask_cors import CORS
#import boto3
import config
#import config
#import util

"""if "DYNAMO_MODE" in os.environ:
    import database_dynamo as database
else:
    import database
"""
if config.DATABSE_TYPE == "SQLITE":
    import database_sqlite as database
else:
    import database_dynamodb as database

application = Flask(__name__)
application.secret_key = "something-random"
CORS(application)


### FlaskForm set up
class productForm(FlaskForm):
    """flask_wtf form class"""
    product_id = HiddenField()
    designation = StringField(u'Designation', [validators.InputRequired()])
    price = DecimalField(u'Price', [validators.InputRequired()])
    quantity = DecimalField(u'Quantity', [validators.InputRequired()])
    category = StringField(u'Category', [validators.InputRequired()])


@application.route("/")
@application.route("/products")
def home():
    "Home screen"
    products = database.list_products()
    if config.DATABSE_TYPE == "SQLITE":
        condition = len(products) == 0
    else:
        condition = products == 0

    if condition:
        print("empty catalogue")
        return render_template_string("""        
        {% extends "html/index.html" %}
        {% block head %}
        Products Catalogue - Home
        {% endblock %}
        {% block body %}
        <a class="btn btn-primary float-right" href="{{ url_for('add') }}">New product</a>
        <p></p>
        <h4>Empty Catalogue</h4>
        {% endblock %}
        """)
    else:
        return render_template_string("""        
        {% extends "html/index.html" %}
        {% block head %}
        Products Catalogue - Home
        {% endblock %}

        {% block body %}
            <a class="btn btn-primary float-right" href="{{ url_for('add') }}">New product</a>
        <br>
        <br>
            
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Designation</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Category</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for product in products %}
                        <tr>
                            <td>{{product.designation}}</td>
                            <td>${{product.price}}</td>
                            <td>{{product.quantity}}</td>
                            <td>{{product.category}}</td>
                            <td>
                            <a class="btn btn-success" href="{{ url_for('edit', product_id=product.id) }}">Edit</a>
                            <a class="btn btn-danger" href="{{ url_for('delete', product_id=product.id) }}">Delete</a>
                            <a class="btn btn-warning" href="{{ url_for('view', product_id=product.id) }}">View</a>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
            
        {% endblock %}
        """, products = products)

@application.route("/products/add")
def add():
    "Add an product"
    form = productForm()
    title = 'Add new product'
    return render_template("html/view-edit.html", title = title, form=form)

@application.route("/products/<product_id>/edit")
def edit(product_id):
    "Edit an product"
    product = database.load_product(product_id)
    
    form = productForm()
    form.product_id.data = product.id
    form.designation.data = product.designation
    form.price.data = product.price
    form.quantity.data = product.quantity
    form.category.data = product.category
    title ="Edit product"
    return render_template("html/view-edit.html", title = title,form=form)

@application.route("/save", methods=['POST'])
def save():
    "Save an product"
    form = productForm()
    
    if form.validate_on_submit():
        if form.product_id.data:
            database.update_product(
                form.product_id.data,
                form.designation.data,
                form.price.data,
                form.quantity.data,
                form.category.data)
        
        else:
            database.add_product(
                form.designation.data,
                form.price.data,
                form.quantity.data,
                form.category.data)
        flash("Saved!")
        return redirect(url_for("home"))
    else:
        return "Form failed validate"

@application.route("/products/<product_id>")
def view(product_id):
    "View an product"
    
    product = database.load_product(product_id)
    form = productForm()

    return render_template_string("""
        {% extends "html/index.html" %}
        {% block head %}
            {{product.designation}}

            <div class="row float-right">
            <div class="control-group">
                <div class="controls">
                    <a class="btn btn-success float-right" href="{{ url_for("edit", product_id=product.id) }}">Edit</a>
                </div>
            </div>
            &nbsp;
            <div class="control-group">
                <div class="controls">
                    <a class="btn btn-primary float-right" href="{{ url_for('home') }}">Home</a>
                </div>
            </div>
        </div>



        {% endblock %}
        {% block body %}
    <form>
        <div class="col-md-8">
            <div class="form-group row">
                <label class="col-sm-2">{{form.designation.label}}</label>
                <div class="col-sm-10">
                    {{product.designation}}
                </div>
            </div>
            <div class="form-group row">
                <label class="col-sm-2">{{form.price.label}}</label>
                <div class="col-sm-10">
                    {{product.price}}
                </div>
            </div>
            <div class="form-group row">
                <label class="col-sm-2">{{form.quantity.label}}</label>
                <div class="col-sm-10">
                    {{product.quantity}}
                </div>
            </div>
            <div class="form-group row">
                <label class="col-sm-2">{{form.category.label}}</label>
                <div class="col-sm-10">
                    {{product.category}}
                </div>
            </div>
        </div>
    </form>
        {% endblock %}
    """, form=form, product=product)

@application.route("/products/<product_id>/delete")
def delete(product_id):
    "delete product route"
    database.delete_product(product_id)
    flash("Deleted!")
    return redirect(url_for("home"))


if __name__ == "__main__":
    database.create_table_products()
    application.run(debug=True)
