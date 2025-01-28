from flask import Flask, request, jsonify
# from pydantic import BaseModel
from typing import List
import main
import transactions
import numpy as np

# app = FastAPI()
app = Flask(__name__)

# class Transaction(BaseModel):
#     date: str
#     amount: float
#     name: str

# @app.get("/")
@app.route("/", methods=['GET'])
def read_root():
    return jsonify({"Hello": "World"})

@app.route("/calculate_budget", methods=['POST'])
def calculate_budget():
    transactions = request.json
    if not transactions:
        return jsonify({"error": "No transactions provided"}), 400
        
    try:
        data, monthly_net = main.create_datasets(transactions)
        smart_budget, total_save = main.calculate_smart_budget(data)
        if np.isnan(smart_budget):
            return jsonify({'message': "Smart budget unavailable"})
        print(smart_budget, total_save, monthly_net)
        
        # Convert monthly_net to JSON-serializable format
        monthly_net_dict = monthly_net.to_dict()
        
        return jsonify({
            "smart_budget": smart_budget,
            "total_save": total_save,
            "total_saved": monthly_net_dict
        })
    
    except Exception as e:
        return jsonify({'message_error': str(e)}), 500


if __name__ == "__main__":
    app.run(host="134.122.123.99", port=5000)
    # app.run(host="0.0.0.0", port=5000)












