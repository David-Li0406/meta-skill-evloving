-- Migration 049: Add social media fields to riders
-- Date: 2025-12-08
-- Description: Adds social media link fields for rider profiles.
--              Allows riders to link their Instagram, Facebook, Strava, YouTube, and TikTok.

-- Add social media columns
ALTER TABLE riders
    ADD COLUMN social_instagram VARCHAR(255) DEFAULT NULL AFTER notes,
    ADD COLUMN social_facebook VARCHAR(255) DEFAULT NULL AFTER social_instagram,
    ADD COLUMN social_strava VARCHAR(255) DEFAULT NULL AFTER social_facebook,
    ADD COLUMN social_youtube VARCHAR(255) DEFAULT NULL AFTER social_strava,
    ADD COLUMN social_tiktok VARCHAR(255) DEFAULT NULL AFTER social_youtube;
