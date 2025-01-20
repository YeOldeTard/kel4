from flask import Flask, request, jsonify, render_template
from mysql import connector

app = Flask(__name__)

db = connector.connect(
    host  = "5ckpn.h.filess.io",
    database  = "Kelompok4_factorfog",
    port      = "3307",
    user  = "Kelompok4_factorfog",
    password  = "49f1dbc6ebd72d53ebd275db886ef42cfbb555f0"
)

if db.is_connected():
    print('Open connection successful')

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

    cur = db.cursor()
    cur.execute(
        "INSERT INTO pesanan (name, contact, details) VALUES (%s, %s, %s)",
        (name, contact, details)
    )
    db.commit()
    cur.close()

    return jsonify({'status': 'success', 'message': 'Pesanan berhasil disimpan'})

@app.route('/orders', methods=['GET'])
def get_orders():
    cur = db.cursor()
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
