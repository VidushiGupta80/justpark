from flask import Flask, jsonify
from time import time

app = Flask(__name__)

@app.route('/ispaid/<string:ticketNumber>', methods=['GET'])
def isPaid(ticketNumber):
    ticketPaid = True if time()%10 < 5 else False
    return jsonify({'status': 200, 'isPaid': ticketPaid})

if __name__ == '__main__':
    app.run(debug=True)