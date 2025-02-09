from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '5ckpn.h.filess.io'
app.config['MYSQL_USER'] = 'Kelompok4_factorfog'
app.config['MYSQL_PASSWORD'] = '49f1dbc6ebd72d53ebd275db886ef42cfbb555f0'
app.config['MYSQL_DB'] = 'Kelompok4_factorfog'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.json
    name = data.get('name')
    contact = data.get('contact')
    details = data.get('details')

    if not (name and contact and details):
        return jsonify({'status': 'error', 'message': 'Semua field harus diisi'}), 400

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO pesanan (name, contact, details) VALUES (%s, %s, %s)",
        (name, contact, details)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({'status': 'success', 'message': 'Pesanan berhasil disimpan'})

@app.route('/orders', methods=['GET'])
def get_orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pesanan")
    data = cur.fetchall()
    cur.close()

    orders = []
    for row in data:
        orders.append({
            'id': row[0],
            'name': row[1],
            'contact': row[2],
            'details': row[3]
        })

    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)
