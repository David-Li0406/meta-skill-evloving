#!/usr/bin/env python3
"""
Upload File to Google Drive

Usage:
    python3 upload_drive.py <file_path> [--folder_id <id>] [--credentials <creds.json>]

Dependencies:
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""

import sys
import argparse
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def get_service(creds_file="credentials.json", token_file="token.json"):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_file):
                print(
                    f"Error: Credentials file '{creds_file}' not found.",
                    file=sys.stderr,
                )
                return None
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)
    return service


def upload_file(file_path, folder_id=None, service=None):
    if not service:
        return None

    file_name = os.path.basename(file_path)

    file_metadata = {"name": file_name}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)

    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id, webViewLink")
        .execute()
    )
    return file


def main():
    parser = argparse.ArgumentParser(description="Upload file to Google Drive")
    parser.add_argument("file_path", help="Path to file to upload")
    parser.add_argument("--folder_id", help="Destination folder ID")
    parser.add_argument(
        "--credentials", default="credentials.json", help="Path to credentials.json"
    )
    parser.add_argument(
        "--token", default="token.json", help="Path to token.json store"
    )

    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        print(f"Error: File '{args.file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    print("Authenticating...")
    service = get_service(args.credentials, args.token)
    if not service:
        sys.exit(1)

    print(f"Uploading '{args.file_path}'...")
    try:
        file = upload_file(args.file_path, args.folder_id, service)
        print(f"File ID: {file.get('id')}")
        print(f"Link: {file.get('webViewLink')}")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
