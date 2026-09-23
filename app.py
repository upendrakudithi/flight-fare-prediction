from flask import Flask, render_template, request, redirect, url_for, flash, session
import numpy as np 
import pandas as pd
import pickle
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, date
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Load the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Load the DataFrame for dropdown values
with open('Clean_Dataset.csv', 'r', encoding='utf-8', errors='replace') as f:
    df = pd.read_csv(f)

# Create users.xlsx if it doesn't exist
if not os.path.exists('users.xlsx'):
    pd.DataFrame(columns=['name', 'email', 'password', 'created_at']).to_excel('users.xlsx', index=False)

dropdown_values = {
    'airline': df['airline'].unique().tolist(),
    'flight': df['flight'].unique().tolist(),
    'source_city': df['source_city'].unique().tolist(),
    'departure_time': df['departure_time'].unique().tolist(),
    'stops': df['stops'].unique().tolist(),
    'arrival_time': df['arrival_time'].unique().tolist(),
    'destination_city': df['destination_city'].unique().tolist(),
    'class': df['class'].unique().tolist()
}

# API endpoint to get flights for a given airline
@app.route('/get_flights_for_airline')
def get_flights_for_airline():
    airline = request.args.get('airline')
    if not airline:
        return jsonify({'flights': []})
    flights = df[df['airline'] == airline]['flight'].unique().tolist()
    return jsonify({'flights': flights})

@app.route('/get_cities_for_airline')
def get_cities_for_airline():
    airline = request.args.get('airline')
    # Define city groups
    national_cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai']
    international_cities = ['New York', 'Detroit', 'London', 'Manchester']
    all_cities = national_cities + international_cities
    
    if airline == 'American':
        allowed = ['New York', 'Detroit', 'Delhi', 'Mumbai', 'Hyderabad']
    elif airline == 'British Airways':
        allowed = ['London', 'Manchester', 'Delhi', 'Mumbai', 'Hyderabad']
    elif airline in ['SpiceJet', 'Vistara']:
        allowed = national_cities
    elif airline in ['Air India', 'Indigo']:
        allowed = all_cities
    else:
        allowed = all_cities
    return jsonify({'cities': allowed})

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict')
def predict():
    if not session.get('logged_in'):
        flash('Please login to access the prediction feature', 'error')
        return redirect(url_for('login'))
    return render_template('index.html', 
                         dropdown_values=dropdown_values,
                         today=date.today().isoformat())

@app.route('/predict', methods=['POST'])
def predict_price():
    if not session.get('logged_in'):
        flash('Please login to access the prediction feature', 'error')
        return redirect(url_for('login'))

    # Get data from the form
    airline = request.form['airline']
    flight = request.form['flight']
    source_city = request.form['source_city']
    departure_time = request.form['departure_time']
    stops = request.form['stops']
    arrival_time = request.form['arrival_time']
    destination_city = request.form['destination_city']
    travel_class = request.form['class']
    duration = float(request.form['duration'])
    days_left = int(request.form['days_left'])

    # Prepare input data for prediction
    input_data = pd.DataFrame([{
        'airline': airline,
        'flight': flight,
        'source_city': source_city,
        'departure_time': departure_time,
        'stops': stops,
        'arrival_time': arrival_time,
        'destination_city': destination_city,
        'class': travel_class,
        'duration': duration,
        'days_left': days_left
    }])

    # Apply one-hot encoding
    input_data = pd.get_dummies(input_data, drop_first=True)
    input_data = input_data.reindex(columns=rf.feature_names_in_, fill_value=0)

    # Predict the price
    prediction = rf.predict(input_data)[0]

    return render_template('index.html', 
                         prediction=f"predicted_price: {prediction:.2f}",
                         dropdown_values=dropdown_values,
                         today=date.today().isoformat())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        users_df = pd.read_excel('users.xlsx')
        user = users_df[users_df['email'] == email]
        
        if not user.empty and check_password_hash(user.iloc[0]['password'], password):
            session['logged_in'] = True
            session['user_email'] = email
            session['user_name'] = user.iloc[0]['name']
            flash('Successfully logged in!', 'success')
            return redirect(url_for('predict'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        users_df = pd.read_excel('users.xlsx')
        
        if email in users_df['email'].values:
            flash('Email already registered', 'error')
            return render_template('signup.html')
        
        # Add new user
        new_user = pd.DataFrame({
            'name': [name],
            'email': [email],
            'password': [generate_password_hash(password)],
            'created_at': [datetime.now()]
        })
        
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_excel('users.xlsx', index=False)
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
