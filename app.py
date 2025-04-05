from flask import Flask, jsonify
from bot_logic import TradingBot

app = Flask(__name__)

bot = TradingBot()

@app.route('/api/market_signal', methods=['GET'])
def get_market_signal():
    signal = bot.get_market_signal()
    return jsonify(signal)

if __name__ == '__main__':
    app.run(debug=True)
