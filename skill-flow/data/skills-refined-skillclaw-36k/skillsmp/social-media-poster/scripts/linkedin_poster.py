#!/usr/bin/env python3
"""
LinkedIn Posting Script
Posts text, images, videos, and links to your LinkedIn profile.
"""

import os
import json
import time
import requests
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

# LinkedIn API version - update as needed
LINKEDIN_VERSION = "202411"

class LinkedInPoster:
    """Handles posting content to LinkedIn via the API."""

    BASE_URL = "https://api.linkedin.com"

    def __init__(self):
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("LINKEDIN_ACCESS_TOKEN not found in environment")

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": LINKEDIN_VERSION
        }
        self.user_urn = None

    def get_user_profile(self) -> str:
        """Get the current user's URN (unique identifier)."""
        if self.user_urn:
            return self.user_urn

        response = requests.get(
            f"{self.BASE_URL}/v2/userinfo",
            headers=self.headers
        )
        response.raise_for_status()
        data = response.json()
        self.user_urn = f"urn:li:person:{data['sub']}"
        return self.user_urn

    def post_text(self, text: str) -> dict:
        """Post a text-only update to LinkedIn."""
        author = self.get_user_profile()

        payload = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(
            f"{self.BASE_URL}/v2/ugcPosts",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def post_with_link(self, text: str, url: str, title: Optional[str] = None, description: Optional[str] = None) -> dict:
        """Post an update with a link preview."""
        author = self.get_user_profile()

        media = {
            "status": "READY",
            "originalUrl": url
        }
        if title:
            media["title"] = {"text": title}
        if description:
            media["description"] = {"text": description}

        payload = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "ARTICLE",
                    "media": [media]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(
            f"{self.BASE_URL}/v2/ugcPosts",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def _register_image_upload(self) -> tuple[str, str]:
        """Register an image upload and get the upload URL."""
        author = self.get_user_profile()

        payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": author,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }

        response = requests.post(
            f"{self.BASE_URL}/v2/assets?action=registerUpload",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        upload_url = data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        asset = data["value"]["asset"]

        return upload_url, asset

    def _upload_image(self, upload_url: str, image_path: str) -> None:
        """Upload an image to LinkedIn's servers."""
        with open(image_path, "rb") as f:
            image_data = f.read()

        upload_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/octet-stream"
        }

        response = requests.put(upload_url, headers=upload_headers, data=image_data)
        response.raise_for_status()

    def post_with_image(self, text: str, image_path: str, title: Optional[str] = None, description: Optional[str] = None) -> dict:
        """Post an update with an image attachment."""
        # Register and upload image
        upload_url, asset = self._register_image_upload()
        self._upload_image(upload_url, image_path)

        author = self.get_user_profile()

        media = {
            "status": "READY",
            "media": asset
        }
        if title:
            media["title"] = {"text": title}
        if description:
            media["description"] = {"text": description}

        payload = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [media]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(
            f"{self.BASE_URL}/v2/ugcPosts",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def post_with_images(self, text: str, image_paths: list, title: Optional[str] = None, description: Optional[str] = None) -> dict:
        """Post an update with multiple image attachments (up to 9 on LinkedIn)."""
        if len(image_paths) > 9:
            raise ValueError("LinkedIn allows maximum 9 images per post")

        author = self.get_user_profile()
        media_list = []

        # Upload each image
        for image_path in image_paths:
            upload_url, asset = self._register_image_upload()
            self._upload_image(upload_url, image_path)
            media = {
                "status": "READY",
                "media": asset
            }
            media_list.append(media)

        # Add title/description to first image only
        if title and media_list:
            media_list[0]["title"] = {"text": title}
        if description and media_list:
            media_list[0]["description"] = {"text": description}

        payload = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": media_list
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(
            f"{self.BASE_URL}/v2/ugcPosts",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

    # ==================== VIDEO UPLOAD METHODS ====================

    def _initialize_video_upload(self, file_size: int) -> dict:
        """Initialize video upload and get upload URLs."""
        author = self.get_user_profile()

        payload = {
            "initializeUploadRequest": {
                "owner": author,
                "fileSizeBytes": file_size,
                "uploadCaptions": False,
                "uploadThumbnail": False
            }
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": LINKEDIN_VERSION
        }

        response = requests.post(
            f"{self.BASE_URL}/rest/videos?action=initializeUpload",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()["value"]

    def _upload_video_chunks(self, video_path: str, upload_instructions: list) -> list:
        """Upload video in chunks and return ETags."""
        etags = []

        with open(video_path, "rb") as f:
            for instruction in upload_instructions:
                first_byte = instruction["firstByte"]
                last_byte = instruction["lastByte"]
                upload_url = instruction["uploadUrl"]

                # Seek to the correct position and read the chunk
                f.seek(first_byte)
                chunk_size = last_byte - first_byte + 1
                chunk_data = f.read(chunk_size)

                # Upload the chunk
                headers = {
                    "Content-Type": "application/octet-stream"
                }

                response = requests.put(upload_url, headers=headers, data=chunk_data)
                response.raise_for_status()

                # Get ETag from response header
                etag = response.headers.get("etag", "").strip('"')
                if etag:
                    etags.append(etag)

                print(f"  Uploaded chunk: bytes {first_byte}-{last_byte}")

        return etags

    def _finalize_video_upload(self, video_urn: str, upload_token: str, etags: list) -> dict:
        """Finalize the video upload."""
        payload = {
            "finalizeUploadRequest": {
                "video": video_urn,
                "uploadToken": upload_token,
                "uploadedPartIds": etags
            }
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": LINKEDIN_VERSION
        }

        response = requests.post(
            f"{self.BASE_URL}/rest/videos?action=finalizeUpload",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        # Response may be empty on success
        try:
            return response.json()
        except:
            return {}

    def _check_video_status(self, video_urn: str) -> str:
        """Check the processing status of an uploaded video."""
        import urllib.parse
        encoded_urn = urllib.parse.quote(video_urn, safe='')

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": LINKEDIN_VERSION
        }

        response = requests.get(
            f"{self.BASE_URL}/rest/videos/{encoded_urn}",
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        return data.get("status", "UNKNOWN")

    def _wait_for_video_processing(self, video_urn: str, max_wait: int = 300, poll_interval: int = 5) -> bool:
        """Wait for video processing to complete."""
        elapsed = 0
        while elapsed < max_wait:
            status = self._check_video_status(video_urn)
            print(f"  Video status: {status}")

            if status == "AVAILABLE":
                return True
            elif status == "PROCESSING_FAILED":
                raise Exception("Video processing failed on LinkedIn")

            time.sleep(poll_interval)
            elapsed += poll_interval

        raise Exception(f"Video processing timeout after {max_wait} seconds")

    def post_with_video(self, text: str, video_path: str, title: Optional[str] = None, description: Optional[str] = None) -> dict:
        """Post an update with a video attachment."""
        # Get file size
        file_size = os.path.getsize(video_path)
        print(f"Uploading video: {video_path} ({file_size / 1024 / 1024:.1f} MB)")

        # Step 1: Initialize upload
        print("  Initializing video upload...")
        init_response = self._initialize_video_upload(file_size)
        video_urn = init_response["video"]
        upload_instructions = init_response["uploadInstructions"]
        upload_token = init_response.get("uploadToken", "")

        print(f"  Video URN: {video_urn}")
        print(f"  Upload chunks: {len(upload_instructions)}")

        # Step 2: Upload chunks
        print("  Uploading video chunks...")
        etags = self._upload_video_chunks(video_path, upload_instructions)

        # Step 3: Finalize upload
        print("  Finalizing upload...")
        self._finalize_video_upload(video_urn, upload_token, etags)

        # Step 4: Wait for processing
        print("  Waiting for video processing...")
        self._wait_for_video_processing(video_urn)

        # Step 5: Create post with video using the Posts API
        print("  Creating post...")
        author = self.get_user_profile()

        payload = {
            "author": author,
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "content": {
                "media": {
                    "id": video_urn
                }
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }

        if title:
            payload["content"]["media"]["title"] = title

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": LINKEDIN_VERSION
        }

        response = requests.post(
            f"{self.BASE_URL}/rest/posts",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        # Response may be empty, get post ID from header
        post_id = response.headers.get("x-restli-id", "posted")
        return {"id": post_id}


def main():
    """Example usage of the LinkedIn poster."""
    import argparse

    parser = argparse.ArgumentParser(description="Post to LinkedIn")
    parser.add_argument("--text", "-t", required=True, help="Post text content")
    parser.add_argument("--url", "-u", help="URL to include (for link posts)")
    parser.add_argument("--image", "-i", action="append", help="Path to image file (can use multiple times)")
    parser.add_argument("--video", "-v", help="Path to video file")
    parser.add_argument("--title", help="Title for link/image/video")
    parser.add_argument("--description", "-d", help="Description for link/image/video")

    args = parser.parse_args()

    poster = LinkedInPoster()

    try:
        if args.video:
            result = poster.post_with_video(
                args.text,
                args.video,
                title=args.title,
                description=args.description
            )
            print(f"Posted with video! ID: {result.get('id', 'success')}")
        elif args.image:
            if len(args.image) == 1:
                result = poster.post_with_image(
                    args.text,
                    args.image[0],
                    title=args.title,
                    description=args.description
                )
            else:
                result = poster.post_with_images(
                    args.text,
                    args.image,
                    title=args.title,
                    description=args.description
                )
            print(f"Posted with image(s)! ID: {result.get('id', 'success')}")
        elif args.url:
            result = poster.post_with_link(
                args.text,
                args.url,
                title=args.title,
                description=args.description
            )
            print(f"Posted with link! ID: {result.get('id', 'success')}")
        else:
            result = poster.post_text(args.text)
            print(f"Posted text! ID: {result.get('id', 'success')}")
    except requests.exceptions.HTTPError as e:
        print(f"Error posting: {e}")
        print(f"Response: {e.response.text}")


if __name__ == "__main__":
    main()
