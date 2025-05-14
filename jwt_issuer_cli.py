r"""
___  ____  _____   ____  _____ ____ _ __ _____
\  \/ (__)/  ___)_/    \/  _  )    | |  | ____)
 \    |  |  |(_  _) () |     (  () | |  |___  \
  \   |__|____   |\____|__|\  \____|____|      )
   \_/        `--'          `--'         \____/
        P  R  o  G  R  A  M  M  i  N  G
<========================================[KCS]=>
  Developer: Ken C. Soukup
  Project  : Tiny JWT Token Issuer
  Purpose  : A very small Flask app that issues JWT Tokens with Asymmetric keys
<=================================[05/12/2025]=>
"""
__project__ = 'Tiny JWT Token Issuer (CLI)'
__version__ = '1.0'
__author__ = 'Ken C. Soukup'
__company__ = 'Vigorous Programming'
__minted__ = '2025'

import os
import sys
import jwt
import time
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Global Constants
BASENAME = os.path.basename(__file__)
KEY_PATH = os.path.join(os.getcwd(), 'keys')
AUDIENCE = 'damage_inc'
ECHO = False


def main() -> None:
    """ Main program where all of the primary calls are made. """
    if ECHO:
        print (f'\n {__project__} v{__version__}')
        print (f' {__company__}')
        print (f' Crafted by {__author__} ({__minted__})\n')
    start_time = time.time()

    # Slurp in parameters
    if len(sys.argv) < 2:
        print('[-] ERROR! : Missing Parameter: username.')
        print(f'[-] Usage  : {BASENAME} <username>.')
        print(f'[-] Example: {BASENAME} triskull.')
        return
    username = sys.argv[1]

    if ECHO:
        print( '[+] -=- Runtime Environment -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print(f'[+] Script Name       : {BASENAME}')
        print(f'[+] User Name         : {username}')
        print(f'[+] Keys Path         : {KEY_PATH}')
        print()
        print(f'[+] Checking for "{username}" keys...')

    if not os.path.exists(os.path.join(KEY_PATH, f'{username}.priv')) or not os.path.exists(os.path.join(KEY_PATH, f'{username}.pem')):
        if ECHO:
            print(f'[-] WARNING! Could not locate {username} to create JWT token.')
            print(f'[+] Generating new keys for {username}...')
        generate_rsa_key_pair(username, KEY_PATH)

    if ECHO:
        print(f'[+] Generate JWT Token for Authentication...')
    with open(os.path.join(KEY_PATH, f'{username}.priv'), 'rb') as material:
        private_key = material.read()
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(hours=1),
            'iat': datetime.now(timezone.utc),
            'sub': username,
            'aud': AUDIENCE
        }

        # Encode the JWT using the private key and RS256 algorithm
        token = jwt.encode(payload, private_key, algorithm='RS256')
        if ECHO:
            print(f'[+] Token: {token}')
        else:
            print(token)

    # Close Script
    if ECHO:
        print()
        print(elapsed_time(start_time))
        print('Mission Complete!!\n')


def elapsed_time(start_time: float) -> str:
    """ Return elapsed time from provided start time """
    script_run_time = time.time() - start_time
    return ('Elapsed Time : {0:02d} hrs. {1:02d} mins. {2:02d} secs. {3:06d} ms.'.format(
        int(script_run_time / 3600), (int(script_run_time / 60) % 60),
        int(script_run_time % 60), int((script_run_time * 1000000) % 1000000)))


def generate_rsa_key_pair(key_name: str, key_path: str) -> None:
    """Generates an RSA private and public key pair and saves them to files."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    full_path = os.path.join(key_path, f'{key_name}.priv')
    with open(full_path, 'wb') as f:
        f.write(private_pem)
    print(f"[+] Private key saved to: {full_path}")

    full_path = os.path.join(key_path, f'{key_name}.pem')
    with open(full_path, 'wb') as f:
        f.write(public_pem)
    print(f"[+] Public key saved to: {full_path}")


if __name__ == '__main__':
    main()
