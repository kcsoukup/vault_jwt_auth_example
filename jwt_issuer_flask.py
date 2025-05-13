r"""
___  ____  _____   ____  _____ ____ _ __ _____
\  \/ (__)/  ___)_/    \/  _  )    | |  | ____)
 \    |  |  |(_  _) () |     (  () | |  |___  \
  \   |__|____   |\____|__|\  \____|____|      )
   \_/        `--'          `--'         \____/
        P  R  o  G  R  A  M  M  i  N  G
<========================================[KCS]=>
  Developer: Ken C. Soukup
  Project  : Tiny JWT Token Issuer (Flask)
  Purpose  : A very small Flask app that issues JWT Tokens with Asymmetric keys
<=================================[04/15/2025]=>
"""
__project__ = 'Tiny JWT Token Issuer'
__version__ = '1.0'
__author__ = 'Ken C. Soukup'
__company__ = 'Vigorous Programming'
__minted__ = '2025'

from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timezone, timedelta

# Variables
app = Flask(__name__)


@app.route('/get_token', methods=['POST'])
def get_token():
    # Need to add User Authentication (flask login) to request token

    # Force=True replaces the need for the -H 'Content-Type: application/json' header
    data = request.get_json(force=True)
    if data:
        print(f'[+] Received data: {data}')

    # Read in private key, must match id string! (no extension)
    with open(f"./keys/{data['id']}", 'rb') as f:
        private_key = f.read()

    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': data['id'],
        'aud': data['aud']
    }

    # Encode the JWT using the private key and RS256 algorithm
    token = jwt.encode(payload, private_key, algorithm='RS256')
    return jsonify({'token': token})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
