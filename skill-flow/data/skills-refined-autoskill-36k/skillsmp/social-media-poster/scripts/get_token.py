#!/usr/bin/env python3
"""
LinkedIn OAuth2 Token Helper
Helps you get an access token for the LinkedIn API.
"""

import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = "openid profile email w_member_social"

class CallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from LinkedIn."""

    def do_GET(self):
        """Process the OAuth callback."""
        parsed = urlparse(self.path)

        if parsed.path == "/callback":
            params = parse_qs(parsed.query)

            if "error" in params:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f"Error: {params['error'][0]}".encode())
                self.server.auth_code = None
                return

            if "code" in params:
                self.server.auth_code = params["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                    <html><body>
                    <h1>Success!</h1>
                    <p>You can close this window and return to the terminal.</p>
                    </body></html>
                """)
                return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        """Suppress logging."""
        pass


def get_authorization_url() -> str:
    """Build the LinkedIn authorization URL."""
    return (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES}"
    )


def exchange_code_for_token(auth_code: str) -> dict:
    """Exchange the authorization code for an access token."""
    response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    response.raise_for_status()
    return response.json()


def main():
    """Run the OAuth flow to get an access token."""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: Missing LINKEDIN_CLIENT_ID or LINKEDIN_CLIENT_SECRET in .env")
        print("\nFollow these steps to get your credentials:")
        print("1. Go to https://www.linkedin.com/developers/apps")
        print("2. Create a new app or select existing one")
        print("3. Copy Client ID and Client Secret to your .env file")
        print("4. Add http://localhost:8000/callback to OAuth 2.0 Authorized Redirect URLs")
        print("5. Request access to 'Share on LinkedIn' and 'Sign In with LinkedIn using OpenID Connect' products")
        return

    print("Starting OAuth flow...")
    print(f"\nOpening browser to authorize the app...")

    # Start local server to receive callback
    server = HTTPServer(("localhost", 8000), CallbackHandler)
    server.auth_code = None

    # Open browser for authorization
    auth_url = get_authorization_url()
    webbrowser.open(auth_url)

    print("Waiting for authorization...")

    # Handle the callback
    while server.auth_code is None:
        server.handle_request()

    if server.auth_code:
        print("\nExchanging code for access token...")
        token_data = exchange_code_for_token(server.auth_code)

        access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", "unknown")

        print("\n" + "=" * 50)
        print("SUCCESS! Here's your access token:")
        print("=" * 50)
        print(f"\nLINKEDIN_ACCESS_TOKEN={access_token}")
        print(f"\nToken expires in: {expires_in} seconds (~{int(expires_in)/86400:.0f} days)" if isinstance(expires_in, int) else "")
        print("\nAdd this to your .env file to start posting!")
    else:
        print("Authorization failed or was cancelled.")


if __name__ == "__main__":
    main()
