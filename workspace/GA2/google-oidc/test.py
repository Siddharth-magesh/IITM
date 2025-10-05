# decode_token.py
import json, time

# Paste your id_token below (keep it quoted)
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE3ZjBmMGYxNGU5Y2FmYTlhYjUxODAxNTBhZTcxNGM5ZmQxYjVjMjYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI1ODg5MDQwNTA0MjMtMzI2bW1zYjNxbGQ4cTAxa2xjMXUxZzFvb3NqY2lydDUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI1ODg5MDQwNTA0MjMtMzI2bW1zYjNxbGQ4cTAxa2xjMXUxZzFvb3NqY2lydDUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTYyNTA1MTQ2NTA2OTA3Mjg2MDIiLCJoZCI6ImRzLnN0dWR5LmlpdG0uYWMuaW4iLCJlbWFpbCI6IjIyZjMwMDI1NzlAZHMuc3R1ZHkuaWl0bS5hYy5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoidlpkSEVHU1FodUhsclpZNUZaUU5ZdyIsIm5vbmNlIjoiZEdCUDRieDUwUFl6T3QySmJRQ04iLCJuYW1lIjoiU0lEREhBUlRIIE0iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSmI1QU5VM1laU2s3MHBIdXJFbXlnSHAtdGRfZS0xd0NwM1JSZXQyam9rRkh1SGdnPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IlNJRERIQVJUSCIsImZhbWlseV9uYW1lIjoiTSIsImlhdCI6MTc1OTY0NDEzOCwiZXhwIjoxNzU5NjQ3NzM4fQ.iyciiHcwmO8guWcSj9ciyywpK47Tzdl1G7U-fwrR5GmD96JSywwJLKdARUpr57JH3GNTxV551i3XoCvV8FiolDSV7SKTNNdAobxLYQ1_JF1CLQW0Gi4g9CwFKSkYimGpjF6K04NEmr41Xp2hvxE8M2RazM81DFGv0CY6SD936gj5dRqmu6CaSLCkIIIOHlP4bCnZ8ZrPsHIbbZeldl9-rT-YVgklhhficWmzAUa4Gq5wN2FZtCVESCzNLsrTFbpP7IPlSHMzSG69S1AJDkiHkrsPl00In1d6gu-QWlGoE_aOl86dCefMHLtrugQlXMOmiPzDD7MM4YtazHw9k2p8SQ"

def decode_without_signature(tok: str):
	# Try PyJWT first
	try:
		import jwt as _pyjwt
		if hasattr(_pyjwt, 'decode'):
			return _pyjwt.decode(tok, options={"verify_signature": False})
	except Exception:
		pass

	# Fallback to python-jose
	try:
		from jose import jwt as _jose_jwt

		# python-jose provides get_unverified_claims for reading
		if hasattr(_jose_jwt, 'get_unverified_claims'):
			return _jose_jwt.get_unverified_claims(tok)
		# or try decode with verify=False
		return _jose_jwt.decode(tok, verify=False)
	except Exception:
		pass

	raise SystemExit("Install PyJWT (pip install pyjwt) or python-jose (pip install python-jose) to decode tokens")


claims = decode_without_signature(token)
print(json.dumps(claims, indent=2))
print("aud:", claims.get("aud"))
print("iss:", claims.get("iss"))
print("email:", claims.get("email"))
print("email_verified:", claims.get("email_verified"))
print("exp:", claims.get("exp"), " (unix)", "valid_now:", claims.get("exp") > time.time())