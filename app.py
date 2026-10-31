from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-demo-secret-key')

# Demo-only in-memory storage. Complaints reset when the server restarts.
complaints = []

HIGH_WORDS = ['emergency', 'urgent', 'danger', 'fire', 'accident', 'injury', 'burst', 'flood', 'electric shock', 'gas leak', 'violence', 'life threatening', 'severe leak']
MEDIUM_WORDS = ['broken', 'not working', 'street light', 'garbage', 'water supply', 'pothole', 'noise', 'repair', 'blocked', 'delay', 'drain']

def classify_priority(text):
    text = text.lower()
    if any(word in text for word in HIGH_WORDS):
        return 'HIGH', 'Needs urgent attention based on detected keywords.'
    if any(word in text for word in MEDIUM_WORDS):
        return 'MEDIUM', 'Should be reviewed and addressed soon.'
    return 'LOW', 'Routine issue; review when resources are available.'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        # Demo credentials only. Replace with a proper user database for real use.
        if username == 'admin' and password == 'admin123':
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Invalid username or password. Try the demo credentials shown below.', 'error')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        location = request.form.get('location', '').strip()
        description = request.form.get('description', '').strip()
        if not all([name, category, location, description]):
            flash('Please complete all fields before submitting.', 'error')
        else:
            priority, reason = classify_priority(description + ' ' + category)
            complaint = {
                'id': len(complaints) + 1,
                'name': name,
                'category': category,
                'location': location,
                'description': description,
                'priority': priority,
                'reason': reason,
                'created_at': datetime.now().strftime('%d %b %Y, %I:%M %p')
            }
            complaints.insert(0, complaint)
            return render_template('result.html', complaint=complaint)
    return render_template('dashboard.html', complaints=complaints)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
