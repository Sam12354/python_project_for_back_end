import jwt  # This is the PyJWT library to work with JSON Web Tokens
from jwt import PyJWTError  # This handles errors from JWT operations


class JWT:
    @staticmethod
    def sign(payload, secret, algorithm='HS256'):
        """
        Create (sign) a JWT token.

        - payload: The data you want to encode into the token (like user info)
        - secret: A secret key (only your server knows this) to sign the token securely
        - algorithm: The encryption algorithm, HS256 is most common

        Returns a token string that can be sent to clients.
        """
        token = jwt.encode(payload, secret, algorithm=algorithm)
        # PyJWT can return either bytes or a string depending on version
        # We make sure to return a string (decoding if needed)
        return token if isinstance(token, str) else token.decode('utf-8')

    @staticmethod
    def verify(token, secret, algorithms=['HS256']):
        """
        Verify a JWT token to check if it's valid and not tampered with.

        - token: The JWT token string received from a client
        - secret: The secret key to verify the signature
        - algorithms: List of acceptable algorithms for verification

        Returns the decoded payload (data inside the token) if valid.

        Raises ValueError if token is invalid or expired.
        """
        try:
            decoded = jwt.decode(token, secret, algorithms=algorithms)
            return decoded
        except PyJWTError as e:
            # Any error means the token is invalid (e.g. expired, tampered)
            raise ValueError(f'Invalid token: {str(e)}')

    @staticmethod
    def decode(token):
        """
        Decode the token **without** verifying its signature.

        - token: The JWT token string

        Use this only if you want to read the data without confirming it's secure.
        Not recommended for security checks!

        Returns the decoded payload (data inside the token).
        """
        return jwt.decode(token, options={"verify_signature": False})
