# Effects Classes

## Contents
- [ParticleEmitter](#particleemitter)
- [Beam](#beam)
- [Trail](#trail)
- [Fire](#fire)
- [Smoke](#smoke)
- [Sparkles](#sparkles)
- [PointLight](#pointlight)
- [SpotLight](#spotlight)
- [SurfaceLight](#surfacelight)
- [Atmosphere](#atmosphere)
- [Sky](#sky)
- [Clouds](#clouds)

---

## ParticleEmitter

A special object that emits customizable 2D particles into the world.

**Properties:**
- `ParticleEmitter.Acceleration`: Vector3 - Determines the global-axis acceleration of all active particles, measured
- `ParticleEmitter.Brightness`: float - Scales the light emitted from the emitter when
- `ParticleEmitter.Color`: ColorSequence - Determines the color of all active particles over their individual
- `ParticleEmitter.Drag`: float - Determines the rate at which particles will lose half their speed through
- `ParticleEmitter.EmissionDirection`: NormalId - Determines the face of the object that particles emit from.
- `ParticleEmitter.Enabled`: boolean - Determines if particles emit from the emitter.
- `ParticleEmitter.FlipbookFramerate`: NumberRange - Determines how fast the flipbook texture animates in frames per second.
- `ParticleEmitter.FlipbookIncompatible`: string - The error message to display if the
- `ParticleEmitter.FlipbookLayout`: ParticleFlipbookLayout - Determines the layout of the flipbook texture. Must be None, Grid2x2,
- `ParticleEmitter.FlipbookMode`: ParticleFlipbookMode - Determines the type of the flipbook animation. Must be Loop, OneShot,
- ...and 27 more

**Methods:**
- `ParticleEmitter:Clear` - Clears all particles that have been emitted.
- `ParticleEmitter:Emit` - Emits a given number of particles.

---

## Beam

Connects two `Class.Attachment|Attachments` by drawing a texture between them.

**Properties:**
- `Beam.Attachment0`: Attachment - The `Class.Attachment` the beam originates from.
- `Beam.Attachment1`: Attachment - The `Class.Attachment` the beam ends at.
- `Beam.Brightness`: float - Scales the light emitted from the beam when
- `Beam.Color`: ColorSequence - Determines the color of the beam across its
- `Beam.CurveSize0`: float - Determines, along with `Class.Beam.Attachment0|Attachment0`, the position
- `Beam.CurveSize1`: float - Determines, along with `Class.Beam.Attachment1|Attachment1`, the position
- `Beam.Enabled`: boolean - Determines whether the beam is visible or not.
- `Beam.FaceCamera`: boolean - Determines whether the `Class.Beam.Segments|Segments` of the beam will
- `Beam.LightEmission`: float - Determines to what degree the colors of the beam are blended with the
- `Beam.LightInfluence`: float - Determines the degree to which the beam is influenced by the environment's
- ...and 10 more

**Methods:**
- `Beam:SetTextureOffset` - Sets the current offset of the beam's texture cycle.

---

## Trail

Used to create a trail effect between two attachments.

**Properties:**
- `Trail.Attachment0`: Attachment - Along with `Class.Trail.Attachment1|Attachment1`, determines where the
- `Trail.Attachment1`: Attachment - Along with `Class.Trail.Attachment0|Attachment0`, determines where the
- `Trail.Brightness`: float - Scales the light emitted from the trail when
- `Trail.Color`: ColorSequence - The color of the trail throughout its lifetime.
- `Trail.Enabled`: boolean - Determines whether the trail will be drawn or not.
- `Trail.FaceCamera`: boolean - Determines whether the trail will always face the camera, regardless of
- `Trail.Lifetime`: float - Determines how long each segment in a trail will last, in seconds.
- `Trail.LightEmission`: float - Determines to what degree the colors of the trail are blended with the
- `Trail.LightInfluence`: float - Determines the degree to which the trail is influenced by the
- `Trail.LocalTransparencyModifier`: float
- ...and 7 more

**Methods:**
- `Trail:Clear` - Clears the segments of the trail.

---

## Fire

A preconfigured particle emitter with the visual aesthetic of fire.

**Properties:**
- `Fire.Color`: Color3 - Determines the color of the primary (outer) flame particles.
- `Fire.Enabled`: boolean - Determines whether flame particles are emit.
- `Fire.Heat`: float - Determines the velocity at which particles are emit.
- `Fire.LocalTransparencyModifier`: float - A multiplier for the `Class.Fire` object's transparency that is only
- `Fire.SecondaryColor`: Color3 - Determines the color of the of the secondary (inner) flame particles.
- `Fire.Size`: float - Determines the size of the flame particles.
- `Fire.size`: float
- `Fire.TimeScale`: float - Controls the speed of the particle effect.

---

## Smoke

A particle emitter with the visual aesthetic of smoke.

**Properties:**
- `Smoke.Color`: Color3 - Determines the color of the smoke particles.
- `Smoke.Enabled`: boolean - Determines whether smoke particles emit.
- `Smoke.LocalTransparencyModifier`: float
- `Smoke.Opacity`: float - Determines how opaque smoke particles render.
- `Smoke.RiseVelocity`: float - Determines the velocity of the smoke particles.
- `Smoke.Size`: float - Determines the size of newly emit smoke particles.
- `Smoke.TimeScale`: float - Value between 0-1 that controls the speed of the particle effect.

---

## Sparkles

A particle emitter with the visual aesthetic of sparkles.

**Properties:**
- `Sparkles.Color`: Color3 - Determines the color of the sparkle particles.
- `Sparkles.Enabled`: boolean - Determines whether sparkles are emit.
- `Sparkles.LocalTransparencyModifier`: float
- `Sparkles.SparkleColor`: Color3 - Determines the color of the sparkle particles.
- `Sparkles.TimeScale`: float

---

## PointLight

A light source that emits illumination from a single point.

**Properties:**
- `PointLight.Range`: float - The size of the area that the PointLight will illuminate.

---

## SpotLight

A light source that emits light directionally in the shape of a cone with a
spherical base.

**Properties:**
- `SpotLight.Angle`: float - The angle of which the light is shone from the SpotLight.
- `SpotLight.Face`: NormalId - Sets the side of the parent that the SpotLight comes from.
- `SpotLight.Range`: float - The size of the area that the SpotLight will illuminate.

---

## SurfaceLight

A light source that emits illumination of a specified color and brightness
from a face for a specified range.

**Properties:**
- `SurfaceLight.Angle`: float - The angle of which the light is shone from the SurfaceLight.
- `SurfaceLight.Face`: NormalId - Sets the side of the parent that the SurfaceLight comes from.
- `SurfaceLight.Range`: float - The distance from the SurfaceLight's face that will illuminate.

---

## Atmosphere

The `Class.Atmosphere` object pushes Roblox closer toward realistic
environments where sunlight scatters in different ways depending on density
and other air particle properties.

**Properties:**
- `Atmosphere.Color`: Color3 - Changes the `Class.Atmosphere` hue for subtle environmental moods.
- `Atmosphere.Decay`: Color3 - When used with increased `Class.Atmosphere.Haze` and
- `Atmosphere.Density`: float - Defines the amount of particles in the `Class.Atmosphere` and essentially
- `Atmosphere.Glare`: float - When used with increased `Class.Atmosphere.Haze`, specifies the glow/glare
- `Atmosphere.Haze`: float - Defines the haziness of the `Class.Atmosphere` with a visible effect both
- `Atmosphere.Offset`: float - Controls how light transmits between the camera and the sky background.

---

## Sky

Changes the default appearance of the experience's sky.

**Properties:**
- `Sky.CelestialBodiesShown`: boolean - Sets whether the sun, moon, and stars will show.
- `Sky.MoonAngularSize`: float - The perceived angular size of the moon while using this skybox, in
- `Sky.MoonTextureContent`: Content
- `Sky.MoonTextureId`: ContentId - The texture of the moon while using this skybox.
- `Sky.SkyboxBackContent`: Content
- `Sky.SkyboxBk`: ContentId - The URL link to a picture for the back surface of the sky.
- `Sky.SkyboxDn`: ContentId - Asset ID for the bottom surface of the skybox.
- `Sky.SkyboxDownContent`: Content
- `Sky.SkyboxFrontContent`: Content
- `Sky.SkyboxFt`: ContentId - Asset ID for the front surface of the skybox.
- ...and 11 more

---

## Clouds

Renders realistic clouds that drift slowly across the sky.

**Properties:**
- `Clouds.Color`: Color3 - Controls the material color of cloud particles.
- `Clouds.Cover`: float - Defines the cloud cover within the overall skyscape layer.
- `Clouds.Density`: float - Controls the particulate density of clouds.
- `Clouds.Enabled`: boolean - Toggles rendering of the `Class.Clouds` object.

---

