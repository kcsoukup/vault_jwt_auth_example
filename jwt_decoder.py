r"""
___  ____  _____   ____  _____ ____ _ __ _____
\  \/ (__)/  ___)_/    \/  _  )    | |  | ____)
 \    |  |  |(_  _) () |     (  () | |  |___  \
  \   |__|____   |\____|__|\  \____|____|      )
   \_/        `--'          `--'         \____/
        P  R  o  G  R  A  M  M  i  N  G
<========================================[KCS]=>
  Developer: Ken C. Soukup
  Project  : Tiny JWT Token Decoder
  Purpose  : Decode a JWT and optionally verify its signature against a public key
<=================================[10/02/2026]=>
"""
__project__ = 'Tiny JWT Token Decoder'
__version__ = '1.0'
__author__ = 'Ken C. Soukup'
__company__ = 'Vigorous Programming'
__minted__ = '2026'

import os
import sys
import json
import jwt
from datetime import datetime, timezone

# Global Constants
BASENAME = os.path.basename(__file__)
KEY_PATH = os.path.join(os.getcwd(), 'keys')
AUDIENCE = 'damage_inc'
TIME_CLAIMS = ('exp', 'iat', 'nbf')


def main() -> None:
    """ Main program where all of the primary calls are made. """
    # Slurp in parameters
    if len(sys.argv) < 2:
        print('[-] ERROR! : Missing Parameter: token.')
        print(f'[-] Usage  : {BASENAME} <token> [username]')
        print(f'[-] Example: {BASENAME} "$JWT_TOKEN" triskull   (username verifies the signature)')
        return
    token = sys.argv[1].strip()
    username = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        header = jwt.get_unverified_header(token)
        payload = jwt.decode(token, options={'verify_signature': False})
    except jwt.exceptions.DecodeError as err:
        print(f'[-] ERROR! : Not a valid JWT: {err}')
        return

    print('[+] Header:')
    print(json.dumps(header, indent=2))
    print('[+] Payload:')
    print(json.dumps(payload, indent=2))

    print('[+] Times:')
    for claim in TIME_CLAIMS:
        if claim in payload:
            print(f'    {claim}: {datetime.fromtimestamp(payload[claim], timezone.utc):%Y-%m-%d %H:%M:%S} UTC')

    if username:
        verify_signature(token, username)
    else:
        print('[!] Signature NOT verified (decoding is only base64). Pass a username to verify.')


def verify_signature(token: str, username: str) -> None:
    """ Verify the token signature, expiration, and audience against keys/<username>.pem """
    pem_file = os.path.join(KEY_PATH, f'{username}.pem')
    if not os.path.exists(pem_file):
        print(f'[-] ERROR! : Public key not found: {pem_file}')
        return

    with open(pem_file, 'rb') as f:
        public_key = f.read()

    try:
        jwt.decode(token, public_key, algorithms=['RS256'], audience=AUDIENCE)
        print(f'[+] Signature VALID for {username} (audience "{AUDIENCE}")')
    except jwt.exceptions.ExpiredSignatureError:
        print('[-] Signature OK, but the token has EXPIRED.')
    except jwt.exceptions.InvalidTokenError as err:
        print(f'[-] Verification FAILED: {err}')


if __name__ == '__main__':
    main()
