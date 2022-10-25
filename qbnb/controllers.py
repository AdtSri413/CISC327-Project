from flask import render_template, request, session, redirect
from qbnb.models import User, Listing, Booking, Review
from qbnb.models import \
    register, login, update_user, create_listing, update_listing
from datetime import datetime


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
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


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
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/')
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals

    # the user's listings
    complete_listings = Listing.query.filter_by(owner_id=user.id).all()
    print(complete_listings)
    if len(complete_listings) > 0:
        listings = []
        for i in complete_listings:
            listings.append({"name": i.name, "description": i.description, 
                            "price": f"${i.price}", "edit": "Edit"})
    else:
        listings = [{"name": "No listings yet!", "description": "", 
                    "price": "", "edit": ""}]

    return render_template('index.html', user=user, listings=listings)


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
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


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
        return redirect('/', code=303)


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
            return redirect('/', code=303)


@app.route('/update_user/<string:old_name>', methods=['Get'])
def update_user_get(old_name):
    return render_template('update_user.html',
                           old_name=old_name, message="")


@app.route('/update_user/<string:old_name>', methods=['POST'])
def update_user_post(old_name):
    try:
        new_name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        error_message = ""
    except Exception:
        error_message = "Please ensure all fields are populated correctly"
        return render_template('update_user.html',
                               old_name=old_name,
                               message=error_message)

    # Use backend function to update user
    success = update_user(old_name, new_name, email, password, password2)

    if not success:
        error_message = "Could not update user"
    # if there is any error messages when updating a user
    # at the backend, stay on update_user page
    if error_message:
        return render_template('update_user.html',
                               old_name=old_name, message=error_message)

    else:
        return redirect('/', code=303)