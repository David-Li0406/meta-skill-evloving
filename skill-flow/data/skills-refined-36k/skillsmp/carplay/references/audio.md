# Audio

CarPlay provides templates for audio playback and Now Playing information.


---

# CPNowPlayingTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A shared system template that displays Now Playing information.

## API Reference

### Managing the Shared Template
• **shared** - The Now Playing template the system provides.

### Managing the Template's Buttons
• **nowPlayingButtons** - The Now Playing template's playback control buttons.
• **updateNowPlayingButtons(_:)** - Updates the playback control buttons the template displays.
• **CPNowPlayingButton** - The abstract base class that Now Playing template buttons use.
• **CPNowPlayingImageButton** - A button that displays an image.
• **CPNowPlayingAddToLibraryButton** - A button for adding the current playing item to a collection.

### Managing Albums, Artists, and Up Next
• **isAlbumArtistButtonEnabled** - A Boolean value that indicates whether the album and artist string is a button.
• **isUpNextButtonEnabled** - A Boolean value that manages the display of the Up Next button.
• **upNextTitle** - The title for the Up Next button.

### Observing Now Playing Events
• **add(_:)** - Registers an observer that receives Now Playing template events.
• **remove(_:)** - Removes an observer from receiving Now Playing template events.
• **CPNowPlayingTemplateObserver** - The methods for responding to the user interacting with the Now Playing template.

### Instance Properties
• **nowPlayingMode** - The currently-active now playing mode. See @c CPNowPlayingMode.


---

# CPNowPlayingButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
The abstract base class that Now Playing template buttons use.

## API Reference

### Creating a Button
• **init(handler:)** - Creates a Now Playing button that invokes a handler.

### Managing the Button State
• **isEnabled** - A Boolean value that indicates whether the button is in an enabled state.
• **isSelected** - A Boolean value that indicates whether the button is in a selected state.


---

# CPNowPlayingImageButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A button that displays an image.

## API Reference

### Creating a Button
• **init(image:handler:)** - Creates a Now Playing button that displays a custom image and invokes a handler.
• **CPNowPlayingButtonMaximumImageSize** - The maximum size CarPlay supports for a button's image.

### Getting the Button's Image
• **image** - The image that the button displays.


---

# CPNowPlayingPlaybackRateButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A button for cycling through the available playback rates.


---

# CPNowPlayingRepeatButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A button for cycling through the available repeat modes.


---

# CPNowPlayingShuffleButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A button for cycling through the available shuffle modes.


---

# CPNowPlayingAddToLibraryButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A button for adding the current playing item to a collection.


---

# CPNowPlayingMoreButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A button for presenting more options to the user.


---

# CPNowPlayingSportsTeam

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 18.4, iPadOS 18.4, Mac Catalyst 18.4

## Overview
A representation of a sports team for the now playing screen, in sports that have exactly two teams.

## API Reference

### Initializers
• **init(name:logo:teamStandings:eventScore:possessionIndicator:favorite:)** - Initialize a sports team for display on the now playing screen.

### Instance Properties
• **eventScore** - The numeric score string for this team in the current event. Depending on the size of the car screen, the score may be truncated.
• **isFavorite** - If true, the team is marked with a star to indicate it has been saved as a user favorite.
• **logo** - The team logo or, if no logo is available, the initials/abbreviation for this team.
• **name** - A localized, user-visible name for this sports team.
• **possessionIndicator** - An optional indicator used to indicate possession by this team. Only one team should have possession at a time.


---

# CPNowPlayingSportsEventStatus

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 18.4, iPadOS 18.4, Mac Catalyst 18.4

## Overview
A representation of the status of a sporting event.

## API Reference

### Initializers
• **init(eventStatusText:eventStatusImage:eventClock:)** - Initialize an event status with optional event status text, an optional event status image, and an optional event clock.

### Instance Properties
• **eventClock** - The event timer, if it applies to this event. See CPNowPlayingSportsClock.
• **eventStatusImage** - An optional event status image for this event, if it applies to this event. For example, a baseball game might display a diamond with runners on base.
• **eventStatusText** - Up to three separate strings for event status may be displayed.


---

# CPNowPlayingModeSports

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 18.4, iPadOS 18.4, Mac Catalyst 18.4

## Overview
The sports mode represents a layout for now playing suited to live-streaming or recorded playback of a sporting event that features exactly two teams.

## API Reference

### Initializers
• **init(leftTeam:rightTeam:eventStatus:backgroundArtwork:)** - Initialize a sports mode for display on the CarPlay now playing screen.

### Instance Properties
• **backgroundArtwork** - A large colorful image for the background of the now playing screen.
• **eventStatus** - A representation of the current event status.
• **leftTeam** - The sports team that should appear on the left side of the now playing screen.
• **rightTeam** - The sports team that should appear on the right side of the now playing screen.


---

# CPNowPlayingSportsClock

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 18.4, iPadOS 18.4, Mac Catalyst 18.4

## Overview
A representation of the amount of time elapsed so far in this event, for events where the clock counts UP.

## API Reference

### Initializers
• **init(elapsedTime:paused:)** - Represents a duration of time that has elapsed so far in this event, or play period of the event.
• **init(timeRemaining:paused:)** - Represents an amount of time remaining in the event, or play period of the event.

### Instance Properties
• **countsUp** - If true, the timer is counting UP, so as to indicate an amount of time elapsed so far in this event.
• **isPaused** - Whether the clock should be paused, e.g. due to a stoppage in play.
• **timeValue** - The time value in the clock; either elapsed time or time remaining.


---

# CPNowPlayingSportsTeamLogo

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 18.4, iPadOS 18.4, Mac Catalyst 18.4

## Overview
A logo image or, if no image is available, an abbreviation or initialism for this team.

## API Reference

### Initializers
• **init(teamInitials:)** - If no team logo image is available, initialize a team logo with an abbreviation or initialism for this team.
• **init(teamLogo:)** - Initialize a team logo with an image representation of this team. Provide an image no larger than 35 points.

### Instance Properties
• **initials** - An abbreviation or initialism for this team, used only if no logo image is available for this team.
• **logo** - A team logo image for this team.
