import jwt

from flask import Flask, Response, request
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from my_api.server import generate_server

def generate_authenticated_server(app_name: str = "auth_hpi_api", cors: bool = True, public_key: str = None, issuer: str = None):
  app: Flask = generate_server(app_name, cors)

  try:
    # Add PEM headers because otherwise things get escaped and will fail to parse
    wrapped_public_key = str.encode('-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----')
    pem_public_key = load_pem_public_key(wrapped_public_key)
  except:
    pass

  @app.before_request
  def before_request():
    return check_authentication(pem_public_key, issuer)

  return app

def validate_claim(jwt_claim, desired_claim):
  # Don't include wildcard (*)
  jwt_claim = jwt_claim.split(':')[:-1]
  desired_parts = desired_claim.split(':')

  has_sufficient_claim = False
  for claim_part in jwt_claim:
    desired_part = desired_parts.pop(0)

    # Every part of the claim is required to match, up to the wildcard
    has_sufficient_claim = claim_part == desired_part

  return has_sufficient_claim

def check_authentication(public_key, issuer):
  # Only enable authentication if the parameter is defined
  if public_key:
    auth_header = request.headers.get('Authorization')
    if auth_header:
      # Grab the token, ignore the auth type
      auth_token = auth_header.split(' ')[1]
    else:
      auth_token = ''

    endpoint = ':'.join(request.base_url.split('/')[3:])

    try:
      decoded_token = jwt.decode(auth_token, public_key, algorithms=["PS256"], options={
        'verify_iat': True,
        'verify_exp': True,
        'verify_iss': True,
        }, issuer=issuer)
    except Exception as e:
      return { "error": "JWT decoded failed due to " + str(e) }

    claims = decoded_token['claims']

    claim_approved = False
    for claim in claims:
      # Has admin wildcard
      if claim == '*':
        claim_approved = True
      # Has a wildcard
      elif '*' in claim:
        claim_approved = validate_claim(claim, endpoint)
      # Exact match
      elif claim == endpoint:
        claim_approved = True

      # Don't validate more claims if we have a match
      if claim_approved:
        break

    if not claim_approved:
      return { "error": "JWT claim is invalid for " + endpoint }
