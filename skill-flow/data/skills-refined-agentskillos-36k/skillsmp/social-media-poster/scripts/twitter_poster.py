#!/usr/bin/env python3
"""
Twitter/X Posting Script
Posts text, images, and videos to your Twitter/X account.
"""

import os
import time
import tweepy
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()


class TwitterPoster:
    """Handles posting content to Twitter/X via the API."""

    def __init__(self):
        # API v2 credentials
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

        # OAuth 1.0a credentials (needed for posting)
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Missing Twitter API credentials in environment")

        # Set up OAuth 1.0a for media uploads
        self.auth = tweepy.OAuth1UserHandler(
            self.api_key,
            self.api_secret,
            self.access_token,
            self.access_token_secret
        )
        self.api_v1 = tweepy.API(self.auth)

        # Set up v2 client for tweets
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )

    def post_text(self, text: str) -> dict:
        """Post a text-only tweet."""
        response = self.client.create_tweet(text=text)
        return {"id": response.data["id"], "text": text}

    def post_with_image(self, text: str, image_path: str) -> dict:
        """Post a tweet with an image attachment."""
        # Upload media using v1.1 API
        media = self.api_v1.media_upload(image_path)

        # Create tweet with media using v2 API
        response = self.client.create_tweet(
            text=text,
            media_ids=[media.media_id]
        )
        return {"id": response.data["id"], "text": text, "media_id": media.media_id}

    def post_with_images(self, text: str, image_paths: List[str]) -> dict:
        """Post a tweet with multiple images (up to 4)."""
        if len(image_paths) > 4:
            raise ValueError("Twitter allows maximum 4 images per tweet")

        # Upload all media
        media_ids = []
        for path in image_paths:
            media = self.api_v1.media_upload(path)
            media_ids.append(media.media_id)

        # Create tweet with media
        response = self.client.create_tweet(
            text=text,
            media_ids=media_ids
        )
        return {"id": response.data["id"], "text": text, "media_ids": media_ids}

    def _transcode_video_for_twitter(self, video_path: str) -> str:
        """
        Transcode video to Twitter-compatible format using ffmpeg.
        Returns path to the transcoded video (in /tmp).
        """
        import subprocess
        import tempfile

        basename = os.path.splitext(os.path.basename(video_path))[0]
        output_path = f"/tmp/{basename}_twitter.mp4"

        print("  Transcoding video for Twitter compatibility...")
        cmd = [
            "ffmpeg", "-y", "-i", video_path,
            "-c:v", "libx264",        # H.264 video codec
            "-profile:v", "high",     # High profile for better compatibility
            "-level", "4.0",          # Level 4.0 for broad device support
            "-pix_fmt", "yuv420p",    # Pixel format Twitter expects
            "-c:a", "aac",            # AAC audio codec
            "-b:a", "128k",           # Audio bitrate
            "-movflags", "+faststart", # Enable streaming
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # Ensure even dimensions
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  FFmpeg error: {result.stderr}")
            raise Exception(f"Video transcoding failed: {result.stderr}")

        print(f"  Transcoded to: {output_path}")
        return output_path

    def _upload_video_chunked(self, video_path: str) -> int:
        """
        Upload a video using chunked upload.
        Returns the media_id for use in tweets.
        """
        file_size = os.path.getsize(video_path)
        print(f"Uploading video: {video_path} ({file_size / 1024 / 1024:.1f} MB)")

        # Transcode video to ensure Twitter compatibility
        transcoded_path = self._transcode_video_for_twitter(video_path)

        # Use tweepy's chunked_upload which handles INIT, APPEND, FINALIZE
        print("  Uploading video chunks...")
        media = self.api_v1.chunked_upload(
            transcoded_path,
            file_type='video/mp4',
            media_category='tweet_video',
            wait_for_async_finalize=True
        )

        # Check if processing succeeded
        processing_info = getattr(media, 'processing_info', None)
        if processing_info and processing_info.get('state') == 'failed':
            error = processing_info.get('error', {})
            raise Exception(f"Twitter video processing failed: {error.get('message', 'Unknown error')}")

        # Clean up transcoded file
        try:
            os.remove(transcoded_path)
        except:
            pass

        print(f"  Video uploaded! Media ID: {media.media_id}")
        return media.media_id

    def post_with_video(self, text: str, video_path: str) -> dict:
        """Post a tweet with a video attachment."""
        # Upload video using chunked upload
        media_id = self._upload_video_chunked(video_path)

        # Create tweet with video
        # Note: media_ids must be strings for the v2 API
        print("  Creating tweet...")
        response = self.client.create_tweet(
            text=text,
            media_ids=[str(media_id)]
        )

        return {
            "id": response.data["id"],
            "text": text,
            "media_id": media_id
        }

    def post_thread(self, tweets: List[str]) -> List[dict]:
        """Post a thread of tweets."""
        results = []
        reply_to_id = None

        for tweet_text in tweets:
            if reply_to_id:
                response = self.client.create_tweet(
                    text=tweet_text,
                    in_reply_to_tweet_id=reply_to_id
                )
            else:
                response = self.client.create_tweet(text=tweet_text)

            reply_to_id = response.data["id"]
            results.append({"id": reply_to_id, "text": tweet_text})

        return results


def truncate_for_twitter(text: str, max_length: int = 280) -> str:
    """Truncate text to fit Twitter's character limit."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def main():
    """Example usage of the Twitter poster."""
    import argparse

    parser = argparse.ArgumentParser(description="Post to Twitter/X")
    parser.add_argument("--text", "-t", required=True, help="Tweet text content")
    parser.add_argument("--image", "-i", action="append", help="Path to image file (can use multiple times)")
    parser.add_argument("--video", "-v", help="Path to video file")
    parser.add_argument("--truncate", action="store_true", help="Truncate to 280 chars (for non-premium accounts)")

    args = parser.parse_args()

    poster = TwitterPoster()
    text = truncate_for_twitter(args.text) if args.truncate else args.text

    try:
        if args.video:
            result = poster.post_with_video(text, args.video)
            print(f"Posted with video! Tweet ID: {result['id']}")
        elif args.image:
            if len(args.image) == 1:
                result = poster.post_with_image(text, args.image[0])
            else:
                result = poster.post_with_images(text, args.image)
            print(f"Posted with image(s)! Tweet ID: {result['id']}")
        else:
            result = poster.post_text(text)
            print(f"Posted! Tweet ID: {result['id']}")

        print(f"View at: https://twitter.com/i/status/{result['id']}")
    except tweepy.TweepyException as e:
        print(f"Error posting: {e}")


if __name__ == "__main__":
    main()
