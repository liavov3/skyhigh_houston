from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Routes
@app.route('/')
def index():
    """Home Page"""
    return render_template('home.html')

@app.route('/gallery/<category>')
def gallery(category):
    """Gallery Page for different product categories."""
    categories = {
        'shirts': ['shirt1.png', 'shirt2.png', 'shirt3.png'],
        'sweatshirts': ['sweatshirt1.png', 'sweatshirt2.png'],
        'new': ['new1.png', 'new2.png']
    }

    if category not in categories:
        flash("Category not found!", "error")
        return redirect(url_for('index'))
    
    return render_template('gallery.html', category=category, items=categories[category])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact Page to send emails."""
    if request.method == 'POST':
        email = request.form.get('email')
        message = request.form.get('message')

        if not email or not message:
            flash("Please provide all required details.", "error")
            return redirect(url_for('contact'))

        # Send email
        try:
            msg = Message("Customer Inquiry", sender=email, recipients=[app.config['MAIL_USERNAME']])
            msg.body = message
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

        return redirect(url_for('index'))
    
    return render_template('contact.html')

@app.route('/add_to_bag', methods=['POST'])
def add_to_bag():
    """Add an item to the shopping bag."""
    data = request.get_json()
    item_name = data.get('item_name')
    item_price = float(data.get('item_price'))

    # Image path based on item name (adjust this logic as needed)
    item_image = f"images/{item_name.lower()}.png"

    # Initialize the shopping bag in the session if not present
    if 'shopping_bag' not in session:
        session['shopping_bag'] = []

    # Add the item to the shopping bag
    session['shopping_bag'].append({'name': item_name, 'price': item_price, 'image': item_image})
    session.modified = True  # Mark session as modified

    return jsonify(success=True)

@app.route('/remove_from_bag', methods=['POST'])
def remove_from_bag():
    """Remove an item from the shopping bag."""
    data = request.get_json()
    item_name = data.get('item_name')

    print(f"Item to remove: {item_name}")  # Debugging

    # Access the shopping bag from the session
    shopping_bag = session.get('shopping_bag', [])

    # Find the first matching item to remove
    for item in shopping_bag:
        if item['name'].lower() == item_name.lower():  # Case-insensitive match
            shopping_bag.remove(item)
            break

    # Save the updated shopping bag back to the session
    session['shopping_bag'] = shopping_bag
    session.modified = True

    print(f"Updated shopping bag: {shopping_bag}")  # Debugging

    return jsonify(success=True)

@app.route('/view_bag')
def view_bag():
    shopping_bag = session.get('shopping_bag', [])
    total = sum(item['price'] for item in shopping_bag)
    return render_template('bag.html', shopping_bag=shopping_bag, total=total)


# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 Page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
