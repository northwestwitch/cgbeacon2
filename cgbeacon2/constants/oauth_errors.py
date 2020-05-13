MISSING_PUBLIC_KEY = dict(
    errorCode=403,
    errorMessage="Could not retrieve OAuth2 public key from Elixir"
)

MISSING_TOKEN_CLAIMS=dict(
    errorCode=403,
    errorMessage="Auth token is not valid: missing claims"
)

INVALID_TOKEN_CLAIMS=dict(
    errorCode=403,
    errorMessage="Auth token error: Invalid claims"
)

EXPIRED_TOKEN_SIGNATURE=dict(
    errorCode=403,
    errorMessage="Auth token contains an expired signature"
)

INVALID_TOKEN_AUTH = dict(
    errorCode=403,
    errorMessage="Invalid auth token error"
)
