# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a JWT Authentication testing project that provides two implementations for generating JWT tokens using RSA asymmetric keys:

1. **Flask Web Service** (`jwt_issuer_flask.py`) - HTTP API for token generation
2. **CLI Tool** (`jwt_issuer_cli.py`) - Command-line token generation with automatic key creation

The project is designed for educational purposes to demonstrate JWT authentication with HashiCorp Vault using RS256 algorithm.

## Development Commands

### Setup
```bash
# Install dependencies
python -m pip install -r requirements.txt

# Create RSA key pairs manually (if needed)
cd keys
openssl genrsa -out <username> 2048
openssl rsa -in <username> -outform PEM -pubout -out <username>.pem
```

### Running Applications

**Flask Web Service:**
```bash
python jwt_issuer_flask.py
# Runs on http://127.0.0.1:5000
```

**CLI Token Generator:**
```bash
python jwt_issuer_cli.py <username>
# Generates keys automatically if they don't exist
```

### Testing JWT Token Generation

**Using Flask API:**
```bash
# Get token via HTTP POST
curl -X POST http://127.0.0.1:5000/get_token -d '{"id": "username", "aud": "damage_inc"}' | jq -r .token

# Store token in variable for Vault authentication
JWT_TOKEN=$(curl -s -X POST http://127.0.0.1:5000/get_token -d '{"id": "username", "aud": "damage_inc"}' | jq -r .token)
```

**Using CLI:**
```bash
# Generate token directly
python jwt_issuer_cli.py username

# Store CLI output in variable
JWT_TOKEN=$(python jwt_issuer_cli.py username)
```

## Architecture

### Key Components

- **Flask Application** (`jwt_issuer_flask.py`): Simple web service with single `/get_token` endpoint
- **CLI Generator** (`jwt_issuer_cli.py`): Standalone token generator with automatic key management
- **Keys Directory Structure**: RSA private/public key pairs stored in `keys/` directory

### Key File Naming Conventions

**Flask Implementation:**
- Private key: `keys/<username>` (no extension)
- Public key: `keys/<username>.pem`

**CLI Implementation:**
- Private key: `keys/<username>.priv`
- Public key: `keys/<username>.pem`

### JWT Token Structure

Both implementations generate tokens with:
- Algorithm: RS256
- Expiration: 1 hour from issue time
- Claims: `sub` (subject/username), `aud` (audience), `exp`, `iat`
- Default audience: "damage_inc"

### Dependencies

- `Flask`: Web framework for HTTP API
- `PyJWT`: JWT token encoding/decoding
- `cryptography`: RSA key operations (CLI only)
- `rsa`: RSA operations (Flask only)

## Integration Notes

This project is designed to work with HashiCorp Vault's JWT authentication method. The generated tokens authenticate users against Vault using the public keys configured in the JWT auth method.