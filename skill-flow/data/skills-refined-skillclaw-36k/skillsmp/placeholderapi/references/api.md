# Placeholderapi - Api

**Pages:** 3

---

## Common Issues¶

**URL:** https://wiki.placeholderapi.com/common-issues/

**Contents:**
- Common Issues¶
- java.lang.NoClassDefFoundError: com/google/gson/Gson¶
- Expansions won't work¶
- Failed to load expansion class <expansion> ...¶
  - - One of its properties is null which is not allowed¶
  - (Is a dependency missing?)¶

This page lists common issues you may encounter with PlaceholderAPI and how you can solve them.

If you have more questions, feel free to join the Discord Server.

If you encounter an issue such as

does it mean that the Server you're using PlaceholderAPI on does not have Gson included. This is often the case for servers running 1.8 or older. To fix this, make sure to use at least 1.8.8 as that version does include the required dependency.

If one or multiple expansions don't work, make sure you checked the following:

When this error appears does it mean that either getAuthor(), getIdentifier() or getVersion() in the expansion return null which is not allowed. In such a case, contact the developer of the expansion and inform them about this issue and that it should be fixed.

This error is given whenever the expansion cannot be loaded, which often happens due to a missing dependency (required plugin) or because creating an expansion instance failed.

The only thing you can do is to provide the full error so that we can check if the issue is caused by PlaceholderAPI (More unlikely) or by the expansion.

**Examples:**

Example 1 (unknown):
```unknown
org.bukkit.plugin.InvalidPluginException: java.lang.NoClassDefFoundError: com/google/gson/Gson
```

---

## Welcome¶

**URL:** https://wiki.placeholderapi.com/

**Contents:**
- Welcome¶
- Navigation¶
  - User Guides¶
  - Dev Guides¶
  - Common Issues¶
  - FAQ¶

This wiki gives you information on how to create placeholders in your plugin that can be used in other plugins, how to use other placeholders inside your plugin, or how to make an expansion. It also has a community-curated list of all available Placeholder expansions and their placeholders.

Pages aimed at server owners who want to utilize PlaceholderAPI.

Pages aimed at plugin developers who want to use PlaceholderAPI in their own plugin or want to make their own PlaceholderExpansion.

Common problems you may face while using PlaceholderAPI, and how to solve them.

Frequently Asked Questions and their answers.

---

## FAQ¶

**URL:** https://wiki.placeholderapi.com/faq/

**Contents:**
- FAQ¶
- What is an Expansion?¶
- It only shows %placeholder% and not the variable¶
  - The expansion is actually installed.¶
  - Plugin actually supports PlaceholderAPI¶
  - No typo in the placeholder¶
  - Plugin is enabled¶
- I can't download the expansion¶
- How can other plugins use my placeholders with PlaceholderAPI?¶
- Can I help on this wiki?¶

Here are frequently asked questions about stuff related to PlaceholderAPI.

An expansion (or PlaceholderExpansion) refers to either a jar file or part of a plugin that provides placeholders to use through PlaceholderAPI itself. Whether said expansion is a separate jar file or part of a plugin depends on the expansion itself and its main purpose.

Expansions that are separate jar files can be found on the eCloud and are downloadable through /papi ecloud download <expansion> if the expansion is verified.

When a plugin or /papi parse me %placeholder% only returns the placeholder itself and no value should you check for the following things:

Some expansions may not be integrated into a plugin or don't even have a plugin to depend on, meaning that they may be their own separate jar file that you have to download. Such expansions can usually be found on the eCloud of PlaceholderAPI and be downloaded using the /papi ecloud download <expansion> command.

Whether an expansion is available on the eCloud or not can be found out in the Placeholder List with any expansion displaying a papi command being downlodable.

It can happen that the plugin you use to display the placeholder in doesn't support PlaceholderAPI. In such a case check, if the parse command returns the actual value of a placeholder. If that is the case while the plugin is still displaying the placeholder, can this be an indicator of the plugin not supporting PlaceholderAPI.

You can find a list of plugins supporting PlaceholderAPI here. Just make sure that "Supports placeholders" has a check mark in front of it.

Double-check that the placeholder you set doesn't contain a typo. You can use /papi ecloud placeholders <expansion> (replace <expansion> with the name of the expansion) to get a list of all the placeholders the expansion may have. Keep in mind that this only works for separate expansions on the eCloud and not for those that are loaded by plugins.

Additionally can the placeholder list from the eCloud be outdated. It is recommended to check the Placeholder List or see if there is any documentation for the placeholders you want to use.

If an expansion depends on a plugin, make sure you have the plugin installed and that it is enabled (Shows green in /pl).

Make the following checks:

If the above checks are all fine and you still can't get the expansion through the download command, consider downloading it manually. To do that, head to the expansion's page on the ecloud, download the jar file and put it into /plugins/PlaceholderAPI/expansions/ before using /papi reload.

See the Using PlaceholderAPI page.

You sure can! We welcome contributions to our wiki by everyone. If you found a typo or want to improve this wiki in another way, head over to the Wiki's readme file to find out about how you can contribute towards this wiki.

If you receive the above error, try to do the following steps:

If the issue persists after you've done those checks, report it to the author of the expansion. In most cases is the issue that either a dependency is missing or that the expansion tries to use outdated methods from PlaceholderAPI.

**Examples:**

Example 1 (json):
```json
[00:00:01 ERROR]: [PlaceholderAPI] Failed to load Expansion class <expansion> (Is a dependency missing?)
[00:00:01 ERROR]: [PlaceholderAPI] Cause: NoClassDefFoundError <path>
```

---
