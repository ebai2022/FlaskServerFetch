from flask import Flask, request, jsonify
from collections import defaultdict, deque
from datetime import datetime

app = Flask(__name__)

transactions = deque()
balances = defaultdict(int)


@app.route('/add', methods=['POST'])
def add_points():
    data = request.get_json()
    payer = data['payer']
    points = data['points']
    timestamp = datetime.fromisoformat(data['timestamp'].replace("Z", "+00:00"))
    transaction = {'payer': payer, 'points': points, 'timestamp': timestamp}
    # if the transaction is the latest, append it
    if not transactions or transactions[-1]['timestamp'] <= timestamp:
        transactions.append(transaction)
    # otherwise, insert in order of timestamp
    else:
        for i, transaction in enumerate(transactions):
            if transaction['timestamp'] > timestamp:
                transactions.insert(i, transaction)
                break
    balances[payer] += points
    return '', 200


@app.route('/spend', methods=['POST'])
def spend_points():
    data = request.get_json()
    points_requested = data['points']
    if sum(balances.values()) < points_requested:
        return 'You do not have enough points', 400
    spent_points = defaultdict(int)
    while points_requested > 0:
        transaction = transactions.popleft()
        payer = transaction['payer']
        points = transaction['points']
        points_requested -= points
        if points_requested < 0:
            spent_points[payer] -= points + points_requested
            balances[payer] -= points + points_requested
        else:
            spent_points[payer] -= points
            balances[payer] -= points
        # add the transaction back if there are still points left
        if points_requested < 0:
            transaction['points'] = -points_requested
            transactions.appendleft(transaction)
    return jsonify(spent_points), 200


@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify(balances), 200


if __name__ == '__main__':
    app.run(port=8000)
