"""The routes.py file you provided contains the route definitions and view functions for the luxury watches application. 
Let's go through each section of the code to understand its functionality:

The Produce blueprint is created using Blueprint('Produce', __name__). 
This blueprint is used to group related routes and views related to produce management together.

The produce() function is associated with the /produce route and handles both GET and POST requests. 
On a GET request, it renders the pages/produce.html template, passing in the form for filtering produce, 
a list of produce items, and a title. On a POST request, it retrieves produce items based on the filter criteria 
submitted in the form and updates the title accordingly.

The add_produce() function is associated with the /add-produce route and requires the user to be logged in
 (@login_required). It handles both GET and POST requests. On a GET request, it renders the pages/add-produce.html template, passing in the form for adding produce. On a POST request, it validates the form and inserts the new produce into the database using the insert_produce() function. It also inserts a corresponding sell record for the produce using the insert_sell() function.

The your_produce() function is associated with the /your-produce route and requires the user to be logged in 
(@login_required). It handles both GET and POST requests. On a GET request, it retrieves all produce items 
for the current user (farmer) from the database using the get_all_produce_by_farmer() function. 
On a POST request, it retrieves produce items based on the filter criteria submitted in the form and
 filters them by the current user (farmer).

The buy_produce() function is associated with the /produce/buy/<pk> route and requires the user to be logged in
 (@login_required). It handles both GET and POST requests. On a GET request, it retrieves the details of a specific 
 produce item based on its primary key (pk) using the get_produce_by_pk() function. On a POST request, it validates 
 the form and inserts a new produce order into the database using the insert_produce_order() function. 
 It also updates the corresponding sell record to mark the produce as unavailable for purchase using the update_sell() function.

The restock_produce() function is associated with the /produce/restock/<pk> route and requires the user to be logged in (@login_required).
 It handles both GET and POST requests. On a GET request, it retrieves the details of a specific produce item based on its primary key
   (pk) using the get_produce_by_pk() function. On a POST request, it validates the form and updates the corresponding sell record 
   to mark the produce as available for purchase using the update_sell() function.

The your_orders() function is associated with the /produce/your-orders route. It retrieves all produce orders for the 
current user (customer) from the database using the get_orders_by_customer_pk() function and renders the pages/your-orders.html template,
 passing in the orders.

Overall, the routes.py file defines the routes and view functions related to producing management, including filtering produce,
 adding produce, viewing user's own produce, buying produce, restocking produce, and viewing user's own orders. 
The functions handle form validation, database operations, and rendering the appropriate templates.
"""
from flask import render_template, request, Blueprint
from flask_login import login_required, current_user

from FineWatches.forms import FilterProduceForm, AddProduceForm, BuyProduceForm, RestockProduceForm
from FineWatches.models import Watch as WatchModel, WatchOrder
from FineWatches.queries import insert_watch, get_watch_by_pk, Sell, \
    insert_sell, get_all_produce_by_farmer, get_produce_by_filters, insert_produce_order, update_sell, \
    get_orders_by_customer_pk

Produce = Blueprint('Produce', __name__)


@Produce.route("/produce", methods=['GET', 'POST'])
def produce():
    form = FilterProduceForm()
    title = 'Our produce!'
    produce = []
    if request.method == 'POST':
        produce = get_produce_by_filters(category=request.form.get('category'),
                                         item=request.form.get('item'),
                                         variety=request.form.get('variety'),
                                         farmer_name=request.form.get('sold_by'),
                                         price=request.form.get('price'))
        title = f'Our {request.form.get("category")}!'
    return render_template('pages/produce.html', produce=produce, form=form, title=title)


@Produce.route("/add-produce", methods=['GET', 'POST'])
@login_required
def add_produce():
    form = AddProduceForm(data=dict(farmer_pk=current_user.pk))
    if request.method == 'POST':
        if form.validate_on_submit():
            produce_data = dict(
                category=form.category.data,
                item=form.item.data,
                variety=form.variety.data,
                unit=form.unit.data,
                price=form.price.data
            )
            produce = ProduceModel(produce_data)
            new_produce_pk = insert_produce(produce)
            sell = Sell(dict(farmer_pk=current_user.pk, produce_pk=new_produce_pk, available=True))
            insert_sell(sell)
    return render_template('pages/add-produce.html', form=form)


@Produce.route("/your-produce", methods=['GET', 'POST'])
@login_required
def your_produce():
    form = FilterProduceForm()
    produce = []
    if request.method == 'GET':
        produce = get_all_produce_by_farmer(current_user.pk)
    if request.method == 'POST':
        produce = get_produce_by_filters(category=request.form.get('category'),
                                         item=request.form.get('item'),
                                         variety=request.form.get('variety'),
                                         farmer_pk=current_user.pk)
    return render_template('pages/your-produce.html', form=form, produce=produce)


@Produce.route('/produce/buy/<pk>', methods=['GET', 'POST'])
@login_required
def buy_produce(pk):
    form = BuyProduceForm()
    produce = get_produce_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            order = ProduceOrder(dict(produce_pk=produce.pk,
                                      farmer_pk=produce.farmer_pk,
                                      customer_pk=current_user.pk))
            insert_produce_order(order)
            update_sell(available=False,
                        produce_pk=produce.pk,
                        farmer_pk=produce.farmer_pk)
    return render_template('pages/buy-produce.html', form=form, produce=produce)


@Produce.route('/produce/restock/<pk>', methods=['GET', 'POST'])
@login_required
def restock_produce(pk):
    form = RestockProduceForm()
    produce = get_produce_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            update_sell(available=True,
                        produce_pk=produce.pk,
                        farmer_pk=produce.farmer_pk)
    return render_template('pages/restock-produce.html', form=form, produce=produce)


@Produce.route('/produce/your-orders')
def your_orders():
    orders = get_orders_by_customer_pk(current_user.pk)
    return render_template('pages/your-orders.html', orders=orders)