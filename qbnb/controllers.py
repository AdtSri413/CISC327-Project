from flask import render_template, request, session, redirect, url_for
from qbnb.models import User, Listing, Booking, Review
from qbnb.models import \
    register, login, update_user, create_listing, update_listing, book_listing
from datetime import datetime
from decimal import Decimal

from qbnb import app


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login', code=303)

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/')
def redirect_to_login():
    return redirect('/login', code=303)


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between a user's browser and the end server. 
        Typically it is packed and stored in the browser cookies. 
        They will be past along between every request the browser made 
        to this services. Here we store the user object into the 
        session, so we can tell if the client has already login 
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/home', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/home')
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals
    # the user's listings
    complete_listings = Listing.query.filter_by(owner_id=user.id).all()
    if len(complete_listings) > 0:
        listings = []
        for i in complete_listings:
            listings.append({"name": i.name, "description": i.description,
                            "price": f"${i.price}", "edit": "Edit"})
    else:
        listings = [{"name": "No listings yet!", "description": "",
                    "price": "", "edit": ""}]

    complete_bookings = Booking.query.filter_by(user_id=user.id).all()
    if len(complete_bookings) > 0:
        bookings = []
        for i in complete_bookings:
            listing = Listing.query.filter_by(id=i.listing_id).first()
            bookings.append({
                            "name": listing.name,
                            "description": listing.description,
                            "start": i.start,
                            "end": i.end})
    else:
        bookings = [{"name": "No Bookings yet", "description": "",
                     "start": "", "end": ""}]

    return render_template(
        'index.html', user=user, listings=listings, bookings=bookings
    )


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = register(name, email, password)
        if not success:
            error_message = "Registration failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        user = login(email, password)
        if user:
            session['logged_in'] = user.email
            return redirect('/home', code=303)
        else:
            render_template('register.html', message="login failed")


@app.route(
    "/make_booking/<int:id>"
    "/<string:username>/<float:balance>/<int:insufficientBalance>"
)
def make_booking(id, username, balance, insufficientBalance):
    # Routing to page which lists all available bookings

    complete_listings = Listing.query.filter(Listing.owner_id != id).all()
    if len(complete_listings) > 0:
        listings = []
        for i in complete_listings:
            listings.append({"name": i.name, "description": i.description,
                            "price": f"${i.price}", "book": "Book"})
    else:
        listings = [{"name": "No available booking!", "description": "",
                    "price": "", "edit": ""}]

    if (insufficientBalance):
        #Booking price > User balance
        insBalMsg = "You have insufficient balance to book this listing"
    else:
        #Booking price < User balance
        insBalMsg = ""
    return render_template(
        'make_booking.html', id=id, username=username,
        listings=listings, balance=balance, insBalMsg=insBalMsg
    )


@app.route(
    "/book/<string:username>/<string:title>/"
    "<string:price>/<float:balance>/<int:id>",
    methods=['Get']
)
def book_get(username, title, price, balance, id):
    #Checks if user has sufficient balance for booking
    price_dec = Decimal(price.strip('$'))
    if (price_dec > balance):
        #Insufficient balance
        return redirect(url_for(
            'make_booking', 
            id=id, username=username,
            balance=balance, insufficientBalance=1)
        )
    else:
        #Sufficient balance, redirect to make booking
        return render_template(
            'booking_page.html', username=username, title=title
        )


@app.route('/book/<string:username>/<string:title>', methods=['Post'])
def book_post(username, title):
    #Creates booking with selected start and end date
    format = '%Y-%m-%d'
    start = datetime.strptime(request.form.get('start'), format)
    end = datetime.strptime(request.form.get('end'), format)
    success = book_listing(title, start, end, username)

    if (success):
        return redirect('/home', code=303)
    else:
        message = "Unable to make booking at specified dates"
        return render_template(
            'booking_page.html',
            username=username, title=title, message=message
        )


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/login', code=303)


@app.route('/update_listing/<string:old_name>', methods=['Get'])
def update_listing_get(old_name):
    # print(session)
    return render_template('update_listing.html',
                           old_name=old_name, message="")


# Find a way to past Updatelisting into the main page
@app.route('/update_listing/<string:old_name>', methods=['Post'])
def update_listing_post(old_name):
    try:
        email = session['logged_in']
        new_name = request.form.get('name')
        price = int(request.form.get('price'))
        description = request.form.get('description')
        error_message = ""
    except Exception:
        error_message = "Please ensure all fields are populated correctly"
        return render_template('update_listing.html',
                               old_name=old_name,
                               message=error_message)

    # Use backend function to update listing
    success = update_listing(old_name, new_name, description, price, email)

    if not success:
        error_message = "Could not update listing"
    # if there is any error messages when updating a listing
    # at the backend, stay on update_listing page
    if error_message:
        return render_template('update_listing.html',
                               old_name=old_name, message=error_message)
    else:
        return redirect('/home')


@app.route('/create_listing')
def create_listing_get():
    if 'logged_in' in session:
        return render_template('create_listing.html',
                               user=session['logged_in'], message="")


@app.route('/create_listing', methods=['POST'])
def create_listing_post():
    if 'logged_in' in session:
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        error_message = None

        # use backend api to create the listing
        success = create_listing(title, description, int(price),
                                 datetime.now(), session["logged_in"])
        if not success:
            error_message = "Could not create listing."
        # if there is any error messages when creating a new listing
        # at the backend, stay on create_listing page
        if error_message:
            return render_template('create_listing.html',
                                   message=error_message)
        else:
            return redirect('/home', code=303)


@app.route('/update_user/<string:old_name>', methods=['Get'])
def update_user_get(old_name):
    return render_template('update_user.html',
                           old_name=old_name, message="")


@app.route('/update_user/<string:old_name>', methods=['POST'])
def update_user_post(old_name):
    try:
        username = request.form.get('name')
        email = request.form.get('email')
        billing_address = request.form.get('billing_address')
        postal_code = request.form.get('postal_code')
        error_message = ""
    except Exception:
        error_message = "Please ensure all fields are populated correctly"
        return render_template('update_user.html',
                               old_name=old_name,
                               message=error_message)

    # Use backend function to update user
    user = User.query.filter_by(username=old_name).first()
    success = update_user(user.id, username, email, billing_address,
                          postal_code)

    if not success:
        error_message = "Could not update user"
    # if there is any error messages when updating a user
    # at the backend, stay on update_user page
    if error_message:
        return render_template('update_user.html',
                               old_name=old_name, message=error_message)

    else:
        user = User.query.filter_by(id=user.id).first()
        session['logged_in'] = user.email
        return redirect('/home', code=303)
