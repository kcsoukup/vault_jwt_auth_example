### JWT Authentication Method -- General Usage Example  
This is a very basic example of creating a JWT token and using it to authenticate with HashiCorp Vault.  
Purely educational only!  
  
#### Links  
https://jwt.io/ -- Use the debugger to review token contents  
  
#### Whats needed?  
HashiCorp Vault 1.1x.x  
Python 3.x.x  
jq (CLI JSON processor)  
Clone of this repository  
  
#### Tiny JWT Token Issuer  
Configure Flask App to generate JWT Tokens using asymmetric keys  
  
**Required directory structure with example keys**  
```
├── jwt_issuer_flask.py
├── requirements.txt
└── keys
    ├── username
    ├── username.pem
    ├── example-kan_soki
    └── example-kan_soki.pem
```
  
**Install Required Python Modules**  
`python -m pip install -r requirements.txt`  
  
**Create Asymmetric Keys in 'keys' directory**  
`cd keys` or add keys/ before the key references  
Change "username" to something else...  
```
openssl genrsa -out <username> 2048
openssl rsa -in <username> -outform PEM -pubout -out <username>.pem
```
... one-liner ...  
```
echo <username> | bash -c 'read -r name && openssl genrsa -out "${name}" 2048 && openssl rsa -in "${name}" -pubout -outform PEM -out "${name}.pem"'
```
  
**Start Flask App**  
`python jwt_issuer_flask.py`  
  
#### Configure JWT Authentication Method in Vault  
Login into the Vault console (sorry no CLI calls... lazy today...)  
Drill into Access and Authentication Methods  
  
Enable the JWT Authentication Method and apply the following values to the configuration  
- Default Role:  jwt_role  
- JWT supported algorithms:  RS256  
- JWT validation public keys:  Add the key materials for the username.pem (public) key(s).  
- Save  
  
Create the jwt_role  
- Go back to the Main Menu, click Tools and then API Explorer  
- Type `jwt` in the search field  
- Click POST /auth/jwt/role/{name}, then Try it out and add the following values  
    - String:  jwt_role  
    - Request body: (Change the bound_audience to match the aud value provided when requesting a JWT token and align the token policy with secrets)  
```
{
  "bound_audiences": ["damage_inc"],
  "role_type": "jwt",
  "token_policies": [
    "default","secrets-readonly"
  ],
  "user_claim": "sub"
}
```
  
#### Using Curl to get JWT token and Authentication with Vault  
```
# Get JWT Token
curl -X POST http://127.0.0.1:5000/get_token -d '{"id": "kan_soki", "aud": "damage_inc"}' | jq -r .token
curl -X POST http://127.0.0.1:5000/get_token -d '{"id": "mando", "aud": "damage_inc"}' | jq -r .token
```
  
**Stuff JWT token into variable, pass to Vault JWT Login API call**  
`JWT_TOKEN=$(curl -s -X POST http://127.0.0.1:5000/get_token -d '{"id": "kan_soki", "aud": "damage_inc"}' | jq -r .token)`  
`curl -s -X POST https://cluster.damage.inc:8200/v1/auth/jwt/login -d '{"role": "jwt_role", "jwt": "'$JWT_TOKEN'"}' | jq .`  
  
Output  
```
{
  "request_id": "98e21f34-6690-ff22-12ed-d75fc22fdb0e",
  "lease_id": "",
  "renewable": false,
  "lease_duration": 0,
  "data": null,
  "wrap_info": null,
  "warnings": null,
  "auth": {
    "client_token": "hvb.AAAAAQLYaLDWnZID1GipgMv8SUY...",
    "accessor": "",
    "policies": [
      "default",
      "secrets-readonly"
    ],
    "token_policies": [
      "default",
      "secrets-readonly"
    ],
    "metadata": {
      "role": "jwt_role"
    },
    "lease_duration": 3600,
    "renewable": false,
    "entity_id": "7e987faa-6c02-d595-6db5-80fe6623aa21",
    "token_type": "batch",
    "orphan": true,
    "mfa_requirement": null,
    "num_uses": 0
  },
  "mount_type": ""
}
```

...
