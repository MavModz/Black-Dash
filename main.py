from flask import Flask, jsonify, render_template, request, redirect, session, json
import mysql.connector
import os
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="black_db")
cursor = conn.cursor()

# Read JSON data from the file
with open('F:\Python\Black-Dash\jsondata.json', encoding='utf-8') as file:
    json_data = json.load(file)

# Iterate over the JSON data and generate INSERT statements
for item in json_data:
    # Extract the necessary fields from the JSON object
    end_year = item.get('end_year')
    intensity = item.get('intensity')
    sector = item.get('sector')
    topic = item.get('topic')
    insight = item.get('insight')
    url = item.get('url')
    region = item.get('region')
    start_year = item.get('start_year')
    impact = item.get('impact')
    added = item.get('added')
    published = item.get('published')
    country = item.get('country')
    relevance = item.get('relevance')
    pestle = item.get('pestle')
    source = item.get('source')
    title = item.get('title')
    likelihood = item.get('likelihood')
    # ...

    # Generate the SQL statement
    sql = "INSERT INTO user_data (end_year, intensity, sector, topic, insight, url, region, start_year, impact, added, published, country, relevance, pestle, source, title, likelihood) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s)"
    values = (end_year, intensity, sector, topic, insight, url, region, start_year,
              impact, added, published, country, relevance, pestle, source, title, likelihood)

    # Execute the SQL statement
    cursor.execute(sql, values)

# Commit the changes to the database
conn.commit()


# Route for HomePage
@app.route('/')
def home():
    return render_template('index.html')

# Route for Register


@app.route('/register')
def register():
    return render_template('register.html')

# Route For Login

@app.route('/login')
def login():
    if 'user_id' not in session:
        return render_template('login.html')
    else:
        return redirect('/dashboard')

# Logout A User

@app.route('/logout')
def logout():
    # Pop out user_id and user_type from session
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect('/')

# Route for dashboard

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Check user type in session
        if 'user_type' in session and session['user_type'] == 'Admin':
            return render_template('admin_dashboard.html')
        else:
            return render_template('dashboard.html')
    else:
        return redirect('/login')

# VALIDATE AND LOGIN USER

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    # Perform email validation using regular expression
    email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.match(email_regex, email):
        return jsonify({'status': 'failure', 'message': 'Please enter a valid email address!'})

    # Perform registration logic and check if email and password match in database
    cursor.execute(""" SELECT * FROM `users` where `email` LIKE '{}' AND BINARY `password` LIKE '{}' """
                   .format(email, password))
    users = cursor.fetchall()
    if len(users) > 0:
        session['user_id'] = users[0][0]
        # Store user_type in session
        session['user_type'] = users[0][1]
        if users[0][1] == 'admin':
            # Return success status and message
            return jsonify({'status': 'success', 'message': 'Login successful!', 'redirect': '/admin'})
        else:
            # Return success status and message
            return jsonify({'status': 'success', 'message': 'Login successful!', 'redirect': '/dashboard'})
    else:
        # Return failure status and message
        return jsonify({'status': 'failure', 'message': 'Email or password is incorrect!'})

# REGISTER A USER

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    cursor.execute("SELECT `email` FROM `users`")
    users = cursor.fetchall()
    print(users)
    print(email)

    if any(user[0] == email for user in users):
        print('Email already exists!')
        return "fail"
    else:
        cursor.execute("""INSERT INTO `users` (`user_id`, `name`, `email`, `password`) VALUES (NULL, '{}', '{}', '{}')""".format(
            name, email, password))
        conn.commit()
        print('Registration successful!')
        return "success"

# FETCH USER NAME

@app.route('/get_user_name')
def get_user_name():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor.execute("SELECT name FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            name = row[0]
            return jsonify({'success': True, 'name': name})
        else:
            return jsonify({'success': False, 'message': 'User not found'})
    else:
        return jsonify({'success': False, 'message': 'User not logged in'})

# Fetch Users from Database


@app.route('/user_details', methods=['GET'])
def user_details():
    # Fetch only the latest 6 rows from the database
    cursor.execute("SELECT * FROM users ORDER BY user_id DESC LIMIT 6")
    rows = cursor.fetchall()
    print(rows)
    users = []
    for row in rows:
        user = {
            'user_id': row[0],
            'user_name': row[1],
            'email': row[2],
            'password': row[3],
        }
        users.append(user)
    return jsonify(users=users)

# Reset Password

@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    password = request.form.get('password')

    email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.match(email_regex, email):
        return jsonify({'status': 'failure', 'message': 'Please enter a valid email address!'})

    # Update password in the database
    cursor.execute(
        "UPDATE users SET password = %s WHERE email = %s", (password, email))
    conn.commit()

    # Check if the update was successful
    if cursor.rowcount > 0:
        return jsonify({'status': 'success', 'message': 'Password updated successfully!'})
    else:
        return jsonify({'status': 'failure', 'message': 'Failed to update password. User not found or invalid email!'})


@app.route('/reset')
def reset():
    return render_template('reset_password.html')

# API for chart data
@app.route('/api/chart_data', methods=['GET'])
def api_chart_data():
    # Fetch data from the database
    cursor.execute(
        "SELECT sector, topic, country, intensity, likelihood, relevance, end_year, region, COUNT(*) as count FROM user_data GROUP BY sector, topic, country, intensity, likelihood, relevance, end_year, region"
    )
    rows = cursor.fetchall()

    sectors = []
    topics = []
    countries = []
    intensities = []
    likelihoods = []
    relevances = []
    end_years = []
    regions = []
    counts = []

    for row in rows:
        sector = row[0]
        topic = row[1]
        country = row[2]
        intensity = row[3]
        likelihood = row[4]
        relevance = row[5]
        end_year = row[6]
        region = row[7]
        count = row[8]

        sectors.append(sector)
        topics.append(topic)
        countries.append(country)
        intensities.append(intensity)
        likelihoods.append(likelihood)
        relevances.append(relevance)
        end_years.append(end_year)
        regions.append(region)
        counts.append(count)

    chart_data = {
        'sectors': sectors,
        'topics': topics,
        'countries': countries,
        'intensities': intensities,
        'likelihoods': likelihoods,
        'relevances': relevances,
        'end_years': end_years,
        'regions': regions,
        'counts': counts
    }

    return jsonify(chart_data)


@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)