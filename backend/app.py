"""Calculator API. Run with `python backend/app.py`; listens on http://localhost:5000."""

import math
import operator

from flask import Flask, jsonify, request

app = Flask(__name__)

OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def is_number(value):
    # bool is a subclass of int, and NaN/Infinity pass Python's JSON parser.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return not isinstance(value, float) or math.isfinite(value)


def error(message):
    return jsonify({"error": message}), 400


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/calculate")
def calculate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error("Invalid input")

    a, b, op = data.get("a"), data.get("b"), data.get("op")
    if not isinstance(op, str) or op not in OPERATIONS:
        return error("Unknown operation")
    if not is_number(a) or not is_number(b):
        return error("Invalid input")

    try:
        result = OPERATIONS[op](a, b)
    except ZeroDivisionError:
        return error("Cannot divide by zero")
    except OverflowError:
        return error("Invalid input")

    if not is_number(result):
        return error("Invalid input")
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
