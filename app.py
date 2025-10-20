from flask import *
import psycopg2

app = Flask(__name__)
app.secret_key = "AW_r%@jN*HU4AW_r%@jN*HU4AW_r%@jN*HU4"
print(__name__)

# Database connection function
def get_connection():
    return psycopg2.connect(
        host='db',        # 👈 use the Docker Compose service name, not localhost
        user='postgres',
        password='root',
        database='jumia',
        port=5432
    )



@app.route('/')
def home():
    # Establish a database connection
    connection = get_connection()
    cursorSmartphone = connection.cursor()
    cursorClothes = connection.cursor()

    sqlSmartphone = "SELECT * FROM products WHERE product_category = 'Smartphone'"
    sqlClothes = "SELECT * FROM products WHERE product_category = 'Clothes'"

    cursorSmartphone.execute(sqlSmartphone)
    cursorClothes.execute(sqlClothes)

    smartphones = cursorSmartphone.fetchall()
    clothes = cursorClothes.fetchall()

    # Close cursors and connection
    cursorSmartphone.close()
    cursorClothes.close()
    connection.close()

    return render_template('home.html', smartphones=smartphones, clothes=clothes)


@app.route('/single/<product_id>')
def single(product_id):
    connection = get_connection()
    cursor1 = connection.cursor()

    sql1 = "SELECT * FROM products WHERE product_id = %s"
    cursor1.execute(sql1, (product_id,))
    product = cursor1.fetchone()

    category = product[4]  # adjust if category column index changes

    sql2 = "SELECT * FROM products WHERE product_category = %s LIMIT 4"
    cursor2 = connection.cursor()
    cursor2.execute(sql2, (category,))
    similar = cursor2.fetchall()

    cursor1.close()
    cursor2.close()
    connection.close()

    return render_template('single.html', product=product, similar=similar)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if len(password1) < 8:
            return render_template('signup.html', error='Password must be more than 8 characters')
        elif password1 != password2:
            return render_template('signup.html', error='Passwords do not match')
        else:
            connection = get_connection()
            cursor = connection.cursor()

            sql = '''INSERT INTO users(username, password, phone, email)
                     VALUES (%s, %s, %s, %s)'''
            cursor.execute(sql, (username, password1, phone, email))
            connection.commit()

            cursor.close()
            connection.close()

            return render_template('signup.html', success='Registered Successfully')
    else:
        return render_template('signup.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_connection()
        cursor = connection.cursor()

        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))

        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if not user:
            return render_template('signin.html', error='Invalid Credentials')
        else:
            session['key'] = username
            return redirect('/')
    else:
        return render_template('signin.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/signin')


# MPESA Integration
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/mpesa', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])

        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        data = r.json()
        access_token = "Bearer " + data['access_token']

        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"

        data_str = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data_str.encode())
        password = encoded.decode('utf-8')

        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)

        return '<h3>Please complete payment on your phone. We will deliver shortly.</h3>' \
               '<a href="/" class="btn btn-dark btn-sm">Back to Products</a>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
