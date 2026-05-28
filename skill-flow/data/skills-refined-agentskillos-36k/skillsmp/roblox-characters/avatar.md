# Avatar Reference

## Contents
- [Photo-to-Avatar generation](#photo-to-avatar-generation)
- [Avatar in-experience creation](#avatar-in-experience-creation)
- [Create avatar items](#create-avatar-items)
- [Resources](#resources)
- [Tutorials](#tutorials)

---

## Photo-to-Avatar generation

<Alert severity = 'success'>
The Photo-to-Avatar feature is currently in alpha. Please refer to the [DevForum announcement](https://devforum.roblox.com/t/early-preview-alpha-release-of-photo-to-avatar-apis/3931624) for latest information.
</Alert>

<Alert severity = 'warning'>
The following guide applies to creators who are familiar with scripting and Roblox Studio and intend to develop experiences that allow user-generated avatar items.
</Alert>

You can create an experience that allows players to generate a fully functional avatar character using a photo and a text prompt.

This process involves the following steps:

1. Request an AvatarGeneration session
2. Prompt the user to take a selfie and generate a 2D preview image of the avatar
3. Generate the full Avatar character using `Class.HumanoidDescription`

### Request an AvatarGeneration session

To start a photo-to-avatar generation, call `Class.AvatarCreationService:RequestAvatarGenerationSessionAsync()` from the server to request a session for the player. A session provides a `Class.Player` with a certain number of Avatar previews and Avatar generations.

As it may take some time for a session to become available, `Class.AvatarCreationService:RequestAvatarGenerationSessionAsync()` returns a `Datatype.RBXScriptConnection` and a waitTime in seconds. The waitTime can be used to provide the `Class.Player` with information on how long it will take them to be able to start their generations.

Once a session is ready, the callback is invoked with a `Dictionary` of information about the session. The `Dictionary` includes:

- `SessionId` — passed as an argument when calling `Class.AvatarCreationService:GenerateAvatar2DPreviewAsync` and `Class.AvatarCreationService:GenerateAvatarAsync`
- `Allowed2DGenerations` — the number of 2D preview generations allowed in a session
- `Allowed3DGenerations` — the number of 3D avatar generations allowed in a session
- `SessionTime` — the maximum time for a session in seconds

### Prom

[Content truncated - see full docs]

---

## Avatar in-experience creation

<Alert severity = 'warning'>
The following guide applies to creators who are familiar with scripting and Roblox Studio and intend to develop experiences that allow user-generated avatar items.
</Alert>

You can publish an experience that allows players to create, customize, and purchase avatar bodies in real time. When purchased, these custom bodies save directly to the player's Roblox inventory, allowing players to equip and wear the custom avatars in other experiences.

Experience owners that implement in-experience avatar creation benefit from [Marketplace commissions](../marketplace/marketplace-fees-and-commissions.md#commissions) as both **creator** of the avatar item and **experience owner**. If an asset created in-experience is inspected, the item provides a link to the original experience it was created.

You can test in-experience creation in Roblox's [Avatar Creator](https://www.roblox.com/games/124012682058672/Roblox-Avatar-Creator) demo.

<Alert severity = 'warning'>
Avatar assets created in-experience are not listed on the Marketplace, and cannot be resold or traded. At this time, in-experience creation only allows the creation of custom avatar bodies.
</Alert>

## How to implement in-experience creation

Use the following instructions and code references to create your first in-experience avatar creation project. The following instructions uses a base body `Class.Model` that players can modify and customize before publishing.

Before getting started, familiarize yourself with the following:

- Avatar models — The following implementation requires importing a base body that meets Roblox's 15 part specifications. This `Class.Model` serves as a base for additional user customization and modification.
  - The base body must meet Roblox's [Avatar body guidelines](../marketplace/marketplace-policy.md#avatar-body-guidelines), including the minimum number of FACS control for facial rigging.
- [Avatar creation tokens](#generate-an-avatar-creation-token) — Exper

[Content truncated - see full docs]

---

## Create avatar items

export const sections = [

{
title: "Turn your creativity into virtual assets",
description: "Roblox streamlines the creation process, letting you focus more on building and bringing your ideas to life with powerful, state-of-the-art tools.",
content: [
{
title: "Design a 2D classic shirt",
description: "Use an image editor of your choice and create your first basic 2D cosmetic.",
video: "https://www.youtube-nocookie.com/embed/r_unfGZT5Ps",
links: [
{ text: "Learn more", href: "../art/classic-clothing.md" }
]
},
{
title: "Create a 3D accessory",
description: "Use a 3D modeling tool and Roblox Studio to make a 3D cosmetic.",
video: "https://www.youtube-nocookie.com/embed/Eed29gV0hLA",
links: [
{ text: "Guides and tutorials", href: "../art/accessories.md" },
{ text: "Get Blender", href: "https://www.blender.org" },
{ text: "Get Studio", href: "./studio/setup/" }
]
},
{
title: "Make 3D layered clothing",
description: "Use your 3D modeling skills and Roblox Studio to create clothing that stretches, fits, and layers.",
video:"https://www.youtube-nocookie.com/embed/C-DwGRBHvmE",
links: [
{ text: "Guides and tutorials", href: "../art/accessories/layered-clothing.md" },
{ text: "Get Blender", href: "https://www.blender.org" },
{ text: "Get Studio", href: "./studio/setup/" }
]
},
]
},

{
title: "What's new?",
description: "Check out our latest videos and guides designed to help you create faster — whether you're a complete newbie or a seasoned industry pro!",
buttons: [
{ text: "See all videos", href: "https://www.youtube.com/playlist?list=PLMneGxZNs3ZYZ5cJ1IPeaO1Eyd4ejY1Lz" },
],
content: [
{
title: "Make your own shoes",
description: "Create your first shoes — an advanced type of layered clothing.",
video: "https://www.youtube-nocookie.com/embed/NHgYM78afqc",
},
{
title: "Convert body cages and clothing cages",
description: "Convert a body cage to a clothing cage and back again! Useful for advanced clothing or body creators.",
video: "https://www.youtube-nocookie.com/embed

[Content truncated - see full docs]

---

## Resources

The following downloadable files are available for your use:

- [References](#references) — Finished assets you can use as reference.
- [Auto-Setup References](#auto-setup-references) — Assets that meet specific avatar auto-setup requirements.
- [Project Files](#project-files) — Fundamental resources like rigs and cages for building your own assets.
- [Mannequins](#mannequin-models) — Models you can use as sizing reference.
- [Templates](#templates) — Prebuilt characters that require small additional customization.
- [Add-ons and Tools](#add-ons-and-tools) — Third-party tools and add-ons.

## References

The following are source files used for actual Roblox assets. Finished assets like Nature Girl and Stylish Male include clothing and accessory items and may cause validation errors unless removed.

<Grid container alignItems='stretch' style={{margin: -6}}>

<Grid item XSmall={12} Medium={6} Large={4} style={{padding: 6}}>
<Card style={{height: '100%'}}>
<CardContent style={{marginBottom:'66px'}}>

<center>Nature Girl</center>
<figure>
<center> <img src="../assets/art/resources/Archer-Girl-Preview.png" width="100%" /> </center>
</figure>
<figure>
A comprehensive `.zip` folder of an avatar-ready character body, including clothing and rigid accessory assets. Each asset includes its own Blender and Maya project file, as well as their respective PBR textures. <br /> <br />

If you are opening these files in Blender, the armature bones may display in an unexpected orientation because the source model was originally exported from Maya. This different orientation doesn't affect the performance of the armature rig.

</figure>
</CardContent>

<CardActions style={{position: 'absolute', bottom: 0, width: '100%'}}>
<Button href="../assets/art/reference-files/NatureArcherGirl.zip" fullWidth size='large' color='primary' variant='contained' style={{marginBottom:"4px;"}}>Download</Button>
</CardActions>

</Card>
</Grid>

<Grid item XSmall={12} Medium={6} Large={4} style={{padding: 6

[Content truncated - see full docs]

---

## Tutorials

Learn how to create assets with structured tutorials that walks through each creation step from modeling in a third-party tool to importing in Studio.

<br /> <br />

<BaseAccordion>
<AccordionSummary>
<Typography variant="h4">Prerequisites</Typography>

  </AccordionSummary>
  <AccordionDetails>

  <Typography variant="body2" color="textSecondary" component="p">
  These tutorials use Blender, a free and open-source software. If you never used Blender or Roblox Studio before, start with the following resources before continuing.
  </Typography>

- [Download Blender](https://www.blender.org/) - Install and setup Blender. Roblox's tutorial content uses Blender 3.0+.
- [Familiarize yourself with Blender](https://docs.blender.org/manual/en/latest/) - Use Blender's official docs or community-created content of your choice to get up to speed with Blender's UI and functions.
- [Setting up Roblox Studio](../studio/setup.md) - Install
  and configure Roblox Studio.

</AccordionDetails>
</BaseAccordion>

<Card>
<CardContent>

<h2 style={{marginBottom: 12}}>Rigid accessories</h2>

<Typography variant="body2" color="textSecondary" component="p">
This tutorial covers the basic steps to successfully create and sell an accessory. Model and texture an object in Blender, upload the publishable accessory item to Studio, and sell the item on the Marketplace.
</Typography>

<>
<Grid
    alignItems="stretch"
    container
    direction="row">

<Grid item Medium={6} XSmall={12} direction="column" style={{"maxWidth": "800px"}}>

<div class="container"
style={{position: "relative"}}>
<img src="../assets/art/accessories/creating-rigid/Chest-Studio.png" width = "90%" />
</div>

</Grid>

<Grid item Medium={6} XSmall={12} direction="column">

<>
<Stepper activeStep={6} orientation="vertical">

<Step style={{marginTop: -36}}>
<a href="../art/accessories/creating-rigid/index.md"><StepLabel optional="Create your custom asset in Blender.">

<h5 style={{marginTop: 36}}>Model</h5>
</StepLabel></a>



[Content truncated - see full docs]

---

