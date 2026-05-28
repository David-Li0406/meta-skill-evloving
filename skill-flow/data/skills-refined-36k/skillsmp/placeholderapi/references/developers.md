# Placeholderapi - Developers

**Pages:** 4

---

## Dev Guides¶

**URL:** https://wiki.placeholderapi.com/developers/

**Contents:**
- Dev Guides¶
  - Using PlaceholderAPI¶
  - Creating a PlaceholderExpansion¶
  - eCloud¶

The pages listed under this section are meant for developers of plugins who want to either create PlaceholderExpansions or want to otherwise work with PlaceholderAPI (i.e. supporting external placeholders through it).

Guide on how to use PlaceholderAPI in your own plugin.

Comprehensive guide on how to create a PlaceholderExpansion for other plugins to use through PlaceholderAPI.

Information about PlaceholderAPI's expansion cloud, including how to submit your own expansion or update it.

---

## Creating a PlaceholderExpansion¶

**URL:** https://wiki.placeholderapi.com/developers/creating-a-placeholderexpansion/

**Contents:**
- Creating a PlaceholderExpansion¶
- Table of contents¶
- Getting started¶
  - Common Expansion Parts¶
    - Basic PlaceholderExpansion Structure¶
- Making an Internal Expansion¶
  - Register your Expansion¶
- Making an External Expansion¶
- Making a relational Expansion¶

This page will cover how you can create your own PlaceholderExpansion which you can either integrate into your own plugin (Recommended) or upload to the eCloud.

It's worth noting that PlaceholderAPI relies on expansions being installed. PlaceholderAPI only acts as the core replacing utility while the expansions allow other plugins to use any installed placeholder in their own messages. You can download expansions either directly from the eCloud yourself, or download them through the download command of PlaceholderAPI.

For starters, you need to decide what type of PlaceholderExpansion you want to create. There are various ways to create an expansion. This page will cover the most common ones.

All shown examples will share the same common parts that belong the the PlaceholderExpansion class. In order to not repeat the same basic info for each method throughout this page, and to greatly reduce the overall length, we will cover the most basic/necessary ones here.

Tab the icons in the code block below for additional information.

This method allows you to set the name of the expansion's author. May not be null.

The identifier is the part in the placeholder that is between the first % (or { for bracket placeholders) and the first _. The identifier may not be null nor contain %, {, } or _.

If you still want to use them in your expansion name, override the getName() method.

This method returns the version of the expansion. May not be null. Due to it being a string are you not limited to numbers alone, but it is recommended to stick with a number pattern.

PlaceholderAPI uses this String to compare with the latest version on the eCloud (if uploaded to it) to see if a new version is available. If your expansion is included in a plugin, this does not matter.

Called by PlaceholderAPI to have placeholder values parsed. When not overriden will call onPlaceholderRequest(Player, String), converting the OfflinePlayer to a Player if possible or else providing null.

Using this method is recommended for the usage of the OfflinePlayer, allowing to use data from a player without their presence being required.

Called by PlaceholderAPI through onRequest(OfflinePlayer, String) to have placeholder values parsed. When not overriden will return null, which PlaceholderAPI will understand as an invalid Placeholder.

Overriding onRequest(OfflinePlayer, String) or onPlaceholderRequest(Player, String) is not required if you create relational placeholders.

Internal PlaceholderExpansions are classes directly integrated in the plugin they depend on. This method of creating a PlaceholderExpansion is recommended as it has the following benefits:

Internal PlaceholderExpansions are not automatically registered by PlaceholderAPI, due to them not being a separate jar file located in the expansion folder. Please see the Regsister your Expansion section for more details.

You are also required to override and set persist() to true. This tells PlaceholderAPI to not unload your expansion during plugin reload, as it would otherwise unregister your expansion, making it no longer work.

Please see the Basic PlaceholderExpansion Structure section for an explanation of all common methods in this example.

Tab the icons in the code block below for additional information.

Mockup plugin used to showcase the use of dependency injection to access specific plugin related data.

We can use the authors set in the plugin's plugin.yml file as the authors of this expansion.

Since our expansion is internal can this version be the same as the one defined in the plugin's plugin.yml file.

This needs to be set, or else will PlaceholderAPI unregister our expansion during a plugin reload.

Example of accessing data of the plugin's config.yml file.

Example of accessing data of the plugin's config.yml file.

Reaching this means that an invalid params String was given, so we return null to tell PlaceholderAPI that the placeholder was invalid.

Due to the PlaceholderExpansion being internal, PlaceholderAPI does not load it automatically, we'll need to do it manually. This is being done by creating a new instance of your PlaceholderExpansion class and calling the register() method of it.

Here is a quick example:

We check that PlaceholderAPI is present and enabled on the server, or else we would get Exceptions. Also, make sure you set PlaceholderAPI as depend or softdepend in your plugin's plugin.yml file!

This registers our expansion in PlaceholderAPI. It also gives the Plugin class as dependency injection to the Expansion class, so that we can use it.

External Expansions are separate Jar files located inside PlaceholderAPI's expansions folder, that contain the PlaceholderExpansion extending class. It is recommended to only make external Expansions for the following situations.

Should the above cases not match your situation, meaning your expansion is for a plugin you maintain, is the creation of an internal Expansion recommended.

Some benefits of an external expansion include automatic (re)loading of your expansion by PlaceholderAPI and having the option to upload it to the eCloud allowing the download of it through the /papi ecloud download command. Downsides include a more tedious setup in terms of checking for a required plugin being present.

Please see the Basic PlaceholderExpansion Structure section for an explanation of all common methods in this example.

Tab the icons in the code block below for additional information.

This is an example expansion without any plugin dependency.

Please see the Basic PlaceholderExpansion Structure section for an explanation of all common methods in this example.

Tab the icons in the code block below for additional information.

This is an example expansion with a plugin dependency.

We set the value of this instance in the canRegister() method, which means that it can't be set to be final.

The name of the plugin this expansion depends on. It is recommended to set this, as it would result in PlaceholderAPI reporting any missing plugin for your expansion.

This does two things:

Example of accessing data of the plugin's config.yml file.

Example of accessing data of the plugin's config.yml file.

Reaching this means that an invalid params String was given, so we return null to tell PlaceholderAPI that the placeholder was invalid.

Relational Placeholders always start with rel_ to properly identify them. This means that if you make a relational placeholder called friends_is_friend would the full placeholder be %rel_friends_is_friend%.

Relational PlaceholderExpansions are special in that they take two players as input, allowing you to give outputs based on their relation to each other.

To create a relational expansion you will need to implement the Relational interface into your expansion. You also still need to extend the PlaceholderExpansion class. Implementing this interface will add the onPlaceholderRequest(Player, Player, String) with the first two arguments being the first and second player to use and the third argument being the content after the second _ and before the final % (Or } if bracket placeholders are used) in the placeholder.

Please see the Basic PlaceholderExpansion Structure section for an explanation of all common methods in this example.

Tab the icons in the code block below for additional information.

This is a complete example of using relational placeholders. For the sake of simplicity are we using the internal Expansion setup here and assume that SomePlugin offers a areFriends(Player, Player) method that returns true or false based on if the players are friends or not.

Mockup plugin used to showcase the use of dependency injection to access specific plugin related data.

We can use the authors set in the plugin's plugin.yml file as the authors of this expansion.

Since our expansion is internal can this version be the same as the one defined in the plugin's plugin.yml file.

This needs to be set, or else will PlaceholderAPI unregister our expansion during a plugin reload.

Our placeholder requires both players to be present, so if either one is not will this return null.

In case the identifier matches (Meaning the placeholder is %rel_example_friends% or {rel_example_friends}) will we check if Player one and two are friends through our plugin's areFriends(Player, Player) method. Should they be friends, return green text saying they are and else return red text saying they aren't.

Reaching this means that an invalid params String was given, so we return null to tell PlaceholderAPI that the placeholder was invalid.

Don't forget to register your expansion.

**Examples:**

Example 1 (java):
```java
package at.helpch.placeholderapi.example.expansion;

import me.clip.placeholderapi.expansion.PlaceholderExpansion;

public class SomeExpansion extends PlaceholderExpansion {

    @Override
    @NotNull
    public String getAuthor() {
        return "Author"; // (1)
    }

    @Override
    @NotNull
    public String getIdentifier() {
        return "example"; // (2)
    }

    @Override
    @NotNull
    public String getVersion() {
        return "1.0.0"; // (3)
    }

    // These methods aren't overriden by default.
    // You have to override one of them.

    @Override
    public String onRequest(OfflinePlayer player, @NotNull String params) {
        // (4)
    }

    @Override
    public String onPlaceholderRequest(Player player, @NotNull String params) {
        // (5)
    }
}
```

Example 2 (java):
```java
package at.helpch.placeholderapi.example.expansion;

import at.helpch.placeholderapi.example.SomePlugin;
import me.clip.placeholderapi.expansion.PlaceholderExpansion;
import org.bukkit.OfflinePlayer;
import org.jetbrains.annotations.NotNull;

public class SomeExpansion extends PlaceholderExpansion {

    private final SomePlugin plugin; // (1)

    public SomeExpansion(SomePlugin plugin) {
        this.plugin = plugin;
    }

    @Override
    @NotNull
    public String getAuthor() {
        return String.join(", ", plugin.getDescription().getAuthors()); // (2)
    }

    @Override
    @NotNull
    public String getIdentifier() {
        return "example";
    }

    @Override
    @NotNull
    public String getVersion() {
        return plugin.getDescription().getVersion(); // (3)
    }

    @Override
    public boolean persist() {
        return true; // (4)
    }

    @Override
    public String onRequest(OfflinePlayer player, @NotNull String params) {
        if (params.equalsIgnoreCase("placeholder1")) {
            return plugin.getConfig().getString("placeholders.placeholder1", "default1"); // (5)
        }

        if (params.equalsIgnoreCase("placeholder2")) {
            return plugin.getConfig().getString("placeholders.placeholder1", "default1"); // (6)
        }

        return null; // (7)
    }
}
```

Example 3 (java):
```java
package at.helpch.placeholderapi.example;

import at.helpch.placeholderapi.example.expansion.SomeExpansion;
import org.bukkit.Bukkit;
import org.bukkit.plugin.java.JavaPlugin;

public class SomePlugin extends JavaPlugin {

    @Override
    public void onEnable() {
        if (Bukkit.getPluginManager().isPluginEnabled("PlaceholderAPI")) { // (1)
            new SomeExpansion(this).register(); // (2)
        }
    }
}
```

Example 4 (java):
```java
package at.helpch.placeholderapi.example.expansion;

import me.clip.placeholderapi.expansion.PlaceholderExpansion;
import org.bukkit.OfflinePlayer;
import org.jetbrains.annotations.NotNull;

public class SomeExpansion extends PlaceholderExpansion {

    @Override
    @NotNull
    public String getAuthor() {
        return "Author";
    }

    @Override
    @NotNull
    public String getIdentifier() {
        return "example";
    }

    @Override
    @NotNull
    public String getVersion() {
        return "1.0.0";
    }

    @Override
    public String onRequest(OfflinePlayer player, @NotNull String params) {
        if (params.equalsIgnoreCase("placeholder1")) {
            return "text1";
        }

        if (params.equalsIgnoreCase("placeholder2")) {
            return "text2";
        }

        return null; // (1)
    }
}
```

---

## Using PlaceholderAPI¶

**URL:** https://wiki.placeholderapi.com/developers/using-placeholderapi/

**Contents:**
- Using PlaceholderAPI¶
- First steps¶
  - Set PlaceholderAPI as (soft)depend¶
- Adding placeholders to PlaceholderAPI¶
- Setting placeholders in your plugin¶

This page is about using PlaceholderAPI in your own plugin, to either let other plugins use your plugin, or just use placeholders from other plugins in your own.

Please note, that the examples in this page are only available for PlaceholderAPI 2.10.0 or higher!

Before you can actually make use of PlaceholderAPI, you first have to import it into your project. Use the below code example matching your dependency manager.

Using Javascript, {version} is replaced with the latest available API version of PlaceholderAPI. Should you see the placeholder as-is does it mean that you either block Javascript, or that the version couldn't be obtained in time during page load.

You can always find the latest version matching the API version on the releases tab of the GitHub Repository.

Next step is to go to your plugin.yml or paper-plugin.yml and add PlaceholderAPI as a depend or softdepend, depending (no pun intended) on if it is optional or not.

Tab the icons in the code block below for additional information.

Tab the icons in the code block below for additional information.

Tab the icons in the code block below for additional information.

Tab the icons in the code block below for additional information.

A full guide on how to create expansions can be found on the Creating a PlaceholderExpansion page.

PlaceholderAPI offers the ability, to automatically parse placeholders from other plugins within your own plugin, giving the ability for your plugin to support thousands of other placeholders without depending on each plugin individually. To use placeholders from other plugins in our own plugin, we simply have to (soft)depend on PlaceholderAPI and use the setPlaceholders method.

It is also important to point out, that any required plugin/dependency for an expansion has to be on the server and enabled, or the setPlaceholders method will just return the placeholder itself (do nothing).

Let's assume we want to send a custom join message that shows the primary group a player has. To achieve this, we can do the following:

The below example assumes a soft dependency on PlaceholderAPI to handle PlaceholderAPI not being present more decently.

Tab the icons in the code block below for additional information.

Using PlaceholderAPI.setPlaceholders(Player, String) we can parse %placeholder% text in the provided String, should they have a matching expansion and said expansion return a non-null String. In our example are we providing a text containing %player_name% and %vault_rank% to be parsed, which require the Player and Vault expansion respectively.

Example output: Notch joined the server! They are rank Admin

**Examples:**

Example 1 (typescript):
```typescript
<repositories>
        <repository>
            <id>placeholderapi</id>
            <url>https://repo.extendedclip.com/releases/</url>
        </repository>
    </repositories>
    <dependencies>
        <dependency>
         <groupId>me.clip</groupId>
          <artifactId>placeholderapi</artifactId>
          <version>{version}</version>
         <scope>provided</scope>
        </dependency>
    </dependencies>
```

Example 2 (json):
```json
repositories {
    maven {
        url = 'https://repo.extendedclip.com/releases/'
    }
}

dependencies {
    compileOnly 'me.clip:placeholderapi:{version}'
}
```

Example 3 (yaml):
```yaml
name: ExamplePlugin
version: 1.0
author: author
main: your.main.path.Here

softdepend: ["PlaceholderAPI"] # (1)
```

Example 4 (yaml):
```yaml
name: ExamplePlugin
version: 1.0
author: author
main: your.main.path.Here

depend: ["PlaceholderAPI"] # (1)
```

---

## eCloud¶

**URL:** https://wiki.placeholderapi.com/developers/expansion-cloud/

**Contents:**
- eCloud¶
- About¶
- How it works¶
- Adding your own expansion¶
- Updating your expansion¶
- Downloading a specific expansion version¶
  - Download with PlaceholderAPI¶
  - Download manually¶

PlaceholderAPI uses an expansion-cloud (A website that has all kinds of expansions stored), to download jar files, that contain the placeholders for it to use.

The expansion-cloud can be seen under https://api.extendedclip.com/home

PlaceholderAPI connects to the ecloud on startup of your server, to check if the cloud is available and how many expansions are available on it. If you run /papi ecloud download <expansion>, PlaceholderAPI will connect to the site to first check if the specified expansion exists and then downloads it if it does.

PlaceholderAPI can only download expansions that are verified on the eCloud. Any unverified expansion needs to be downloaded manually.

You can disable the connection to the cloud by setting cloud_enabled in the config.yml to false.

You can add your own expansion to the expansion-cloud for others to use. In order to do that, you have to follow those steps:

Click on the button that says Choose an file... and select the jar of your expansion.

Important! Make sure, that the name of the jar file contains the same version like you set in the version field.

Click on Submit Expansion

Your expansion is now uploaded and will be reviewed by a moderator. If everything is ok will your expansion be approved and will be available on the ecloud for PlaceholderAPI*.

You can block specific expansions from being downloaded using the PAPI_BLOCKED_EXPANSIONS environment variable. Just define it with a value of comma-separated expansion names that should not be downloadable by PlaceholderAPI.

This feature exists since version 2.11.4 of PlaceholderAPI.

Before you update, please note the following: Updating your expansion will automatically make it unverified, requiring a site moderator to verify it again. This was made to combat malware from being uploaded and distributed.

To update your expansion, you first have to go to the list of your expansions. For that click on Expansions and select Your Expansions. After that, follow those steps:

Fill out the fields and upload the new jar.

Important! Make sure, that the name of the jar file contains the same version like you set in the version field.

Click on Save Changes

Your version should now be uploaded to the eCloud. You can now ask a responsible staff member on the HelpChat Discord to review your expansion to get it re-verified. Please remain patient and polite when asking.

In some cases, you may want to use a specific, older version of an expansion. Such a case could be for example, when you run an old server version and the newest version of an expansion uses methods that aren't available on that particular server version, causing compatability issues. For that case is there a way, to download a specific version of expansion. You can download the expansion either manually, or through PlaceholderAPI itself. Here is how you can do it for each.

This is the easiest of both methods since it requires the least amount of effort. Run the following command in-game or in your console to download a specific version: /papi ecloud download <expansion> [version]

To find out, what versions are available for the expansion, run /papi ecloud info <expansion>.

After you downloaded the specific version, run /papi reload to refresh the installed expansions.

To download an expansion manually, you first have to connect to the website and go to the expansion of your choice. There, you click on the button that says Version and click on the download-icon of the version you want to download.

Finally, stop your server, upload the jar to the folder in /plugins/PlaceholderAPI/expansions (Make sure to delete the old jar, if there's already one) and start the server again.

---
