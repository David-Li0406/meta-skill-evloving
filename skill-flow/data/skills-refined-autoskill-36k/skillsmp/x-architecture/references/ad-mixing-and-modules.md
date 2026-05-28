# Reference: Ad Mixing & Modules

The final stage of the pipeline doesn't just rank tweets; it assembles a "Product" that includes non-tweet content. This is handled by the `ProductMixer`.

### Component Integration
- **Ads (Promoted Posts):** Fetched from the Ad-Mixer. They are interleaved with organic content using fixed-ratio logic (e.g., an ad every 5th or 20th slot) or predicted value-per-impression logic.
- **WTF (Who To Follow):** Modules containing suggested accounts based on the `Follow-Recommendation-Service` (FRS).
- **Prompts:** Internal system messages (e.g., "Complete your profile") or seasonal banners.

### Mixing Constraints
- **Ad Density:** Strict caps on how many ads a user can see per session.
- **Diversity Rules:** Ensuring a WTF module doesn't appear immediately after an ad or between two very similar tweets.
