import os
import time
import random
from flask import Flask, jsonify

app = Flask(__name__)

pendingTime = int(os.environ.get("pendingTime", "10"))
startTime = time.time()

@app.route("/status", methods=["GET"])
def getStatus():
	try:
		timeElapsed = int(time.time() - startTime)
		print(f"\ntime elapsed: {timeElapsed} seconds")

		if timeElapsed < pendingTime:
			return jsonify({"result": "pending", "timeElapsed": timeElapsed}), 200
		else:
			return jsonify({"result": "completed", "timeElapsed": timeElapsed}), 200

	except Exception as e:
		print(f"Error in /status: {e}")
		return jsonify({"result": "error"}), 500
	
if __name__ == "__main__":
	app.run(debug=True)

  