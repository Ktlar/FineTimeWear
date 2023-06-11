from flask import render_template, request, Blueprint
from flask_login import login_required, current_user

from FineWatches.forms import FilterWatchForm, AddWatchForm, BuyWatchForm, RestockWatchForm
from FineWatches.models import Watches as WatchModel, WatchOrder
from FineWatches.queries import insert_watch, get_watches_by_pk, Sell, \
    insert_sell, get_all_watches_by_brandrep, get_watches_by_filters, insert_watch_order, update_sell, \
    get_orders_by_customer_pk

Watch = Blueprint('Watch', __name__)


@Watch.route("/collection.html", methods=['GET', 'POST'])
def watch():
    form = FilterWatchForm()
    title = 'Our watch!'
    watch = []
    if request.method == 'POST':
        watch = get_watches_by_filters(brand=request.form.get('brand'),
                                         model=request.form.get('model'),
                                         brandrep_name=request.form.get('brandrep_name'),
                                         brandrep_pk=request.form.get('brandrep_pk'),
                                         price=request.form.get('price'))
        title = f'Our {request.form.get("category")}!'
    return render_template('collection.html', watch=watch, form=form, title=title)


@Watch.route("/add_watch", methods=['GET', 'POST'])
@login_required
def add_produce():
    form = AddWatchForm(data=dict(brandrep_pk=current_user.pk))
    if request.method == 'POST':
        if form.validate_on_submit():
            watch_data = dict(
                brand=form.brand.data,
                model=form.model.data,
                price=form.price.data
            )
            watch = WatchModel(watch_data)
            new_watch_pk = insert_watch(watch)
            sell = Sell(dict(brandrep_pk=current_user.pk, watch_pk=new_watch_pk, available=True))
            insert_sell(sell)
    return render_template('add_watch.html', form=form)


@Watch.route("/your-watch", methods=['GET', 'POST'])
@login_required
def your_watch():
    form = FilterWatchForm()
    watch = []
    if request.method == 'GET':
        watch = get_all_watches_by_brandrep(current_user.pk)
    if request.method == 'POST':
        watch = get_watches_by_filters(brand=request.form.get('brand'),
                                         model=request.form.get('model'),
                                         brandrep_pk=current_user.pk)
    return render_template('pages/your-watch.html', form=form, watch=watch)


@Watch.route('/buy_watch.html', methods=['GET', 'POST'])
@login_required
def buy_watch(pk):
    form = BuyWatchForm()
    watch = get_watches_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            order = WatchOrder(dict(watch_pk=watch.pk,
                                      brandrep_pk=watch.brandrep_pk,
                                      customer_pk=current_user.pk))
            insert_watch_order(order)
            update_sell(available=False,
                        watch_pk=watch.pk,
                        brandrep_pk=watch.brandrep_pk)
    return render_template('buy_watch.html', form=form, watch=watch)


@Watch.route('/watch/restock/<pk>', methods=['GET', 'POST'])
@login_required
def restock_watch(pk):
    form = RestockWatchForm()
    watch = get_watches_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            update_sell(available=True,
                        watch_pk=watch.pk,
                        brandrep_pk=watch.brandrep_pk)
    return render_template('pages/restock-watch.html', form=form, watch=watch)


@Watch.route('/watch/your-orders')
def your_orders():
    orders = get_orders_by_customer_pk(current_user.pk)
    return render_template('pages/your-orders.html', orders=orders)