---
name: linkedin-poster
description: Automated LinkedIn posting skill that logs in to LinkedIn using stored credentials, creates a post with specified content, and publishes it. Use this skill when you need to post content to LinkedIn without manual steps. Triggers when user requests to post on LinkedIn.
---

# LinkedIn Poster Skill

Automated LinkedIn posting skill that handles the entire posting process from login to publishing.

## Overview

This skill automates the process of posting on LinkedIn by:
- Opening LinkedIn
- Logging in using stored credentials
- Creating a new post with provided content
- Publishing the post

## Prerequisites

- LinkedIn credentials must be stored in creds.json in the .claude directory
- The creds.json file must contain a "linkedin" object with "email" and "password" fields

## Usage

When prompted to post on LinkedIn, this skill will automatically:
1. Navigate to LinkedIn
2. Log in using stored credentials
3. Create a new post with the provided content
4. Publish the post to your feed

## Expected Input

Provide the content you want to post on LinkedIn. The skill will handle the rest of the process automatically.

## Workflow Steps

1. Navigate to LinkedIn.com
2. Extract login credentials from creds.json
3. Fill login form with credentials
4. Click Sign In button
5. Click on Start a Post button
6. Fill post content in the text area
7. Optional: Add media (images/video) to the post - see detailed steps below
8. Click Post button to publish

### Adding Media (Images/Video) to Post - Detailed Steps

1. Click the "Add media" button in the post editor
2. Use the file upload tool to select the media file(s) from the specified path
   - For single image: Select one image file (jpg, png, etc.)
   - For multiple images: Select multiple image files
   - For video: Select one video file (mp4, mov, etc.)
3. The media editor dialog will appear with the uploaded media
4. If multiple images were selected, use the editor to arrange or remove any unwanted images
5. Click the "Add" button in the media editor to confirm the media(s)
6. The media will be attached to the post
7. Verify the media appears in the post editor as a preview

### Scheduling a Post - Detailed Steps

1. After adding content (and optionally media) to your post, click the "Schedule for later" button
2. The scheduling dialog will appear with current date and time
3. Click the Date field to expand the date picker options (optional, current date is usually fine)
4. Select the desired date (e.g., "10")
5. Click the time field to expand the time picker options
6. Select the desired time (e.g., "6:00 PM")
7. Verify the date and time are correct
8. Click the "Next" button to proceed
9. Add content to the post text area if not already done (required for scheduling)
10. The post will be configured for the selected date and time
11. Click the "Schedule" button to finalize scheduling
12. The post will be scheduled and appear in your scheduled posts
