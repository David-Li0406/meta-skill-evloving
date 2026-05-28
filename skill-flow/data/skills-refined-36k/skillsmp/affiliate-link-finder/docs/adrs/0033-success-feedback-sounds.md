# ADR 0033: Success Feedback Sounds (Audio Rewards)

## Status
Accepted

## Context
ADHD coaching strategies emphasize immediate, multi-sensory feedback to increase the "surface area" of dopamine rewards for completing routine tasks. The app already featured visual feedback (Confetti, SnackBars), but lacked an auditory dimension. Adding a distinct "Success Sound" upon logging a dose creates a stronger cognitive seal for the action, making the habit formation loop more robust.

## Decision
We implemented a centralized audio feedback system:
1.  **SoundService Port/Adapter**: Created a `SoundService` interface in the domain/infrastructure layer to abstract audio playback.
2.  **Asset Management**: Integrated a premium, lightweight success sound file (`success.mp3`) into the app's asset bundle.
3.  **Cross-Platform Adapter**: Implemented the service using the `audioplayers` package, ensuring consistent playback on iOS and Android.
4.  **Action Integration**: Wired the `DailyStackViewModel` to trigger `playSuccess()` whenever a supplement dose is successfully marked as taken.
5.  **Preference Support**: Added an "Auditory Feedback" toggle in the Settings repository to allow users to mute sounds if they prefer a silent experience or have sensory sensitivities.

## Consequences
- **Reinforced Habits**: Users obtain immediate auditory confirmation, reducing the "did I log this?" anxiety.
- **Dopamine Delivery**: Higher perceived level of achievement for each intake.
- **Technical Debt**: Dependency on an audio library and local asset management, which requires careful handling in unit tests (using Fakes).
