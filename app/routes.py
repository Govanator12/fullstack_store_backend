from app import app, db
from flask import request, jsonify
from datetime import datetime


@app.route('/')
def index():
    return ''

@app.route('/api/products/add', methods=['GET', 'POST'])
def addProduct():
    try:
        # get headers first
        title = request.headers.get('title')
        imageURL = request.headers.get('imageURL')
        price = float(request.headers.get('price'))
        desc = request.headers.get('desc')
        amount = int(request.headers.get('amount'))

        if not title and not price and not imageURL and not desc and not amount:
            return jsonify({ 'error #301': 'Invalid params' })

        if not isinstance(price, float) and not isinstance(amount, int):
            return jsonify({ 'error #302': ' Price should be a decimal and amount should be a whole number' })

        # create a product
        product = Product(title=title, imageURL=imageURL, price=price, desc=desc, amount=amount)

        # add to stage and commit to db
        db.session.add(product)
        db.session.commit()

        return jsonify({ 'success': 'product created' })
    except:
        return jsonify({ 'error #303': 'something went wrong' })

@app.route('/api/products/remove', methods=['GET', 'POST'])
def removeProduct():
    try:
        product_id = request.headers.get('product_id')

        product = Event.query.filter_by(id=product_id).first()

        if not product:
            return jsonify({ 'error#306': 'Product does not exist.'})

        db.session.delete(product)
        db.session.commit()

        return jsonify({ 'success': f'Product {product_id} deleted.'})

    except:
        return jsonify({ 'error#307': 'Could not delete product.' })

@app.route('/api/retrieve', methods=['GET', 'POST'])
def retrieve():
    try:
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')

        if day and month and year:
            results = Event.query.filter_by(day=day, month=month, year=year).all()
        elif not day and month and year:
            results = Event.query.filter_by(month=month, year=year).all()
        elif not day and not month and year:
            results = Event.query.filter_by(year=year).all()
        else:
            return jsonify({ 'error#304': 'Required params not included' })

        if not results:
            return jsonify({ 'success': 'No events scheduled with those dates.' })

        # remember that results is a list of db.Model objects
        parties = []

        for event in results:
            party = {
                'id': event.id,
                'title': event.title,
                'day': event.day,
                'month': event.month,
                'year': event.year,
                'notes': event.notes
            }

            parties.append(party)

        return jsonify(parties)

    except:
        return jsonify({ 'error#305': 'something went wrong' })


@app.route('/api/purchases/add', methods=['GET', 'POST'])
def addPurchase():
    try:
        # get headers first
        total = request.headers.get('total')


        if not total:
            return jsonify({ 'error #301': 'Params for total required' })

        if not isinstance(total, float):
            return jsonify({ 'error #302': ' Total should be a decimal' })

        # create an purchase
        purchase = Purchase(total=total, date_purchased=datetime.now().date())

        # add to stage and commit to db
        db.session.add(purchase)
        db.session.commit()

        return jsonify({ 'success': 'purchase created' })
    except:
        return jsonify({ 'error #303': 'something went wrong' })

@app.route('/api/pruchases/remove', methods=['GET', 'POST'])
def removePurchase():
    try:
        product_id = request.headers.get('product_id')

        product = Event.query.filter_by(id=product_id).first()

        if not product:
            return jsonify({ 'error#306': 'Product does not exist.'})

        db.session.delete(product)
        db.session.commit()

        return jsonify({ 'success': f'Product {product_id} deleted.'})

    except:
        return jsonify({ 'error#307': 'Could not delete product.' })
