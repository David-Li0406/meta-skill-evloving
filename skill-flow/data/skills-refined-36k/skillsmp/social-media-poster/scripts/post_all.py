#!/usr/bin/env python3
"""
Unified Social Media Posting Script
Posts content to multiple platforms simultaneously.

Supported platforms:
- LinkedIn
- Twitter/X
- (Future: Instagram, Facebook)
"""

import os
import argparse
from typing import Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()

# Platform availability flags
PLATFORMS = {
    "linkedin": True,
    "twitter": True,
    # "instagram": False,  # Future
    # "facebook": False,   # Future
}


def post_to_linkedin(text: str, image_path: Optional[str] = None,
                     image_paths: Optional[List[str]] = None,
                     video_path: Optional[str] = None,
                     url: Optional[str] = None, title: Optional[str] = None) -> Dict:
    """Post to LinkedIn."""
    try:
        from linkedin_poster import LinkedInPoster
        poster = LinkedInPoster()

        if video_path:
            result = poster.post_with_video(text, video_path, title=title)
        elif image_paths and len(image_paths) > 1:
            result = poster.post_with_images(text, image_paths, title=title)
        elif image_path:
            result = poster.post_with_image(text, image_path, title=title)
        elif image_paths and len(image_paths) == 1:
            result = poster.post_with_image(text, image_paths[0], title=title)
        elif url:
            result = poster.post_with_link(text, url, title=title)
        else:
            result = poster.post_text(text)

        return {
            "platform": "LinkedIn",
            "success": True,
            "id": result.get("id", "posted"),
            "url": f"https://www.linkedin.com/feed/"
        }
    except Exception as e:
        return {
            "platform": "LinkedIn",
            "success": False,
            "error": str(e)
        }


def post_to_twitter(text: str, image_path: Optional[str] = None,
                    image_paths: Optional[List[str]] = None,
                    video_path: Optional[str] = None,
                    url: Optional[str] = None, title: Optional[str] = None) -> Dict:
    """Post to Twitter/X. Supports long-form posts for premium accounts."""
    try:
        from twitter_poster import TwitterPoster
        poster = TwitterPoster()

        # Append URL to text if provided (Twitter shows link previews automatically)
        full_text = f"{text}\n\n{url}" if url else text

        if video_path:
            result = poster.post_with_video(full_text, video_path)
        elif image_paths and len(image_paths) > 1:
            result = poster.post_with_images(full_text, image_paths)
        elif image_path:
            result = poster.post_with_image(full_text, image_path)
        elif image_paths and len(image_paths) == 1:
            result = poster.post_with_image(full_text, image_paths[0])
        else:
            result = poster.post_text(full_text)

        return {
            "platform": "Twitter",
            "success": True,
            "id": result["id"],
            "url": f"https://twitter.com/i/status/{result['id']}"
        }
    except Exception as e:
        return {
            "platform": "Twitter",
            "success": False,
            "error": str(e)
        }


# Future platform functions
# def post_to_instagram(text: str, image_path: Optional[str] = None, **kwargs) -> Dict:
#     """Post to Instagram."""
#     pass

# def post_to_facebook(text: str, image_path: Optional[str] = None, **kwargs) -> Dict:
#     """Post to Facebook."""
#     pass


PLATFORM_HANDLERS = {
    "linkedin": post_to_linkedin,
    "twitter": post_to_twitter,
    # "instagram": post_to_instagram,
    # "facebook": post_to_facebook,
}


def post_to_all(
    text: str,
    platforms: Optional[List[str]] = None,
    image_path: Optional[str] = None,
    image_paths: Optional[List[str]] = None,
    video_path: Optional[str] = None,
    url: Optional[str] = None,
    title: Optional[str] = None,
    parallel: bool = True
) -> List[Dict]:
    """
    Post content to multiple social media platforms.

    Args:
        text: The post content
        platforms: List of platforms to post to (default: all available)
        image_path: Optional path to single image file (deprecated, use image_paths)
        image_paths: Optional list of paths to image files
        video_path: Optional path to video file
        url: Optional URL to include
        title: Optional title for link/image/video
        parallel: Whether to post to platforms in parallel

    Returns:
        List of result dictionaries for each platform
    """
    if platforms is None:
        platforms = [p for p, enabled in PLATFORMS.items() if enabled]

    # Handle backwards compatibility - merge image_path into image_paths
    if image_path and not image_paths:
        image_paths = [image_path]

    results = []

    if parallel:
        with ThreadPoolExecutor(max_workers=len(platforms)) as executor:
            futures = {}
            for platform in platforms:
                if platform in PLATFORM_HANDLERS:
                    handler = PLATFORM_HANDLERS[platform]
                    future = executor.submit(
                        handler,
                        text=text,
                        image_path=image_paths[0] if image_paths and len(image_paths) == 1 else None,
                        image_paths=image_paths if image_paths and len(image_paths) > 0 else None,
                        video_path=video_path,
                        url=url,
                        title=title
                    )
                    futures[future] = platform

            for future in as_completed(futures):
                results.append(future.result())
    else:
        for platform in platforms:
            if platform in PLATFORM_HANDLERS:
                handler = PLATFORM_HANDLERS[platform]
                result = handler(
                    text=text,
                    image_path=image_paths[0] if image_paths and len(image_paths) == 1 else None,
                    image_paths=image_paths if image_paths and len(image_paths) > 0 else None,
                    video_path=video_path,
                    url=url,
                    title=title
                )
                results.append(result)

    return results


def main():
    """CLI interface for posting to all platforms."""
    parser = argparse.ArgumentParser(
        description="Post to multiple social media platforms simultaneously"
    )
    parser.add_argument("--text", "-t", required=True, help="Post content")
    parser.add_argument("--image", "-i", action="append", help="Path to image file (can use multiple times for multiple images)")
    parser.add_argument("--video", "-v", help="Path to video file")
    parser.add_argument("--url", "-u", help="URL to include in post")
    parser.add_argument("--title", help="Title for link/image/video")
    parser.add_argument(
        "--platforms", "-p",
        nargs="+",
        choices=list(PLATFORMS.keys()),
        help="Platforms to post to (default: all)"
    )
    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Post sequentially instead of in parallel"
    )

    args = parser.parse_args()

    print("=" * 50)
    print("Posting to social media platforms...")
    print("=" * 50)

    results = post_to_all(
        text=args.text,
        platforms=args.platforms,
        image_paths=args.image,  # Now a list from action="append"
        video_path=args.video,
        url=args.url,
        title=args.title,
        parallel=not args.sequential
    )

    print("\nResults:")
    print("-" * 50)

    success_count = 0
    for result in results:
        platform = result["platform"]
        if result["success"]:
            success_count += 1
            print(f"✅ {platform}: Posted successfully!")
            print(f"   ID: {result['id']}")
            print(f"   URL: {result['url']}")
        else:
            print(f"❌ {platform}: Failed")
            print(f"   Error: {result['error']}")
        print()

    print("-" * 50)
    print(f"Summary: {success_count}/{len(results)} platforms succeeded")


if __name__ == "__main__":
    main()
