from flask import Flask, render_template, request, redirect, url_for

#import db functions

from db import get_products, add_product, get_product_by_id, update_product, \
               get_locations, add_location, get_location_by_id, update_location, \
               add_movement, get_movements, get_balance_report, get_stock_at_location


app = Flask(__name__)

# ---HOME PAGE (List All Products) ---
@app.route("/")
def home():
    products = get_products()
    return render_template("inventory.html", products=products)

# --- ADD PRODUCT ---
@app.route("/add_product", methods=["POST"])
def add_product_route():
    product_name = request.form['product_name']
    add_product(product_name)
    return redirect(url_for('home'))

# --- EDIT PRODUCT PAGE ---
@app.route("/edit_product/<int:id>")
def edit_product_route(id):
    product = get_product_by_id(id)
    return render_template("edit.html", product=product)

# --- UPDATE PRODUCT ---
@app.route("/update_product/<int:id>", methods=["POST"])
def update_product_route(id):
    new_name = request.form['product_name']
    update_product(id, new_name)
    return redirect(url_for('home'))




# --- LOCATIONS ROUTES ---

@app.route("/locations")
def locations():
    locations = get_locations()
    return render_template("locations.html", locations=locations)

@app.route("/add_location", methods=["POST"])
def add_location_route():
    location_name = request.form['location_name']
    add_location(location_name)
    return redirect(url_for('locations'))

@app.route("/edit_location/<int:id>")
def edit_location_route(id):
    location = get_location_by_id(id)
    return render_template("edit_location.html", location=location)

@app.route("/update_location/<int:id>", methods=["POST"])
def update_location_route(id):
    new_name = request.form['location_name']
    update_location(id, new_name)
    return redirect(url_for('locations'))



# --- MOVEMENT ROUTES ---

@app.route("/movements")
def movements():
    # Products & Locations for dropdown
    products = get_products()
    locations = get_locations()
    # Movements for history
    movements = get_movements()
    return render_template("movements.html", products=products, locations=locations, movements=movements)

# app.py

@app.route("/add_movement", methods=["POST"])
def add_movement_route():
    product_id = int(request.form['product_id'])
    qty = int(request.form['qty'])
    from_loc = request.form['from_location']
    to_loc = request.form['to_location']
    
    # Empty String handling

    if from_loc == "": from_loc = None
    if to_loc == "": to_loc = None

    # --- STOCK CHECKING ---
    if from_loc:

        # ask db for current stock
        current_stock = get_stock_at_location(product_id, int(from_loc))
        
        # Check if source has enough stock
        if from_loc:
            current_stock = get_stock_at_location(from_loc, product_id)
            
            if current_stock < qty:
                # get product names from database
                p_data = get_product_by_id(product_id)
                p_name = p_data['product_name']

                # 2. Error Message for not available stock
                error = f"❌ '{p_name}' ( Available Stock : {current_stock}, Asked: {qty} )"
                
                # return movements, products, locations
                products = get_products()
                locations = get_locations()
                movements = get_movements()
                return render_template('movements.html', products=products, locations=locations, movements=movements, error=error)
    # --- STOCK CHECKING END ---

    # else part. if stock is there, save
    add_movement(product_id, qty, from_loc, to_loc)
    return redirect(url_for('movements'))


    # --- REPORT ROUTE ---
@app.route("/report")
def report():
    report_data = get_balance_report()
    return render_template("report.html", report=report_data)


if __name__ == "__main__":
    app.run(debug=True)
