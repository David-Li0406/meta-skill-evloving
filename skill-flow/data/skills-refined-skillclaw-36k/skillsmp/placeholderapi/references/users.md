# Placeholderapi - Users

**Pages:** 5

---

## Placeholder List¶

**URL:** https://wiki.placeholderapi.com/users/placeholder-list/

**Contents:**
- Placeholder List¶
- Standalone¶
  - Advancements¶
  - Animations¶
  - Armor¶
  - ASCII¶
  - Attribute¶
  - BungeeCord¶
  - CalculateNumbers¶
  - ChangeOutput¶

This is a list of all available placeholders.

A download-command may be found in the infobox located below the title of the Expansion. Should Built into Plugin be displayed is the Expansion included in the Plugin it depends on. Should a URL be shown does it mean you have to download it manually and add it to the expansions folder yourself.

This placeholder list is provided "as-is" without any guarantee of being accurate and/or up-to-date.

Page is only updated on request. We recommend contributing to this list by making a Pull request. Further details on how to contribute to this list or the wiki as a whole can be found on the README file of the Wiki.

Expansions listed here don't need any plugin or extra library to function properly, unless mentioned otherwise. A majority of these Expansions are maintained by the PlaceholderAPI team and can be considered official.

papi ecloud download Advancements

More info about this expansion can be found on the GitHub-Repository.

papi ecloud download Animations

Please note: When using placeholders within the animation text, you must use the bracket variant. Use {player_name} instead of %player_name% within the <tag> </tag> tags.

Please visit the dedicated wiki for all available tags.

papi ecloud download Armor

Gives you info about your armor

papi ecloud download ASCII

Returns the ASCII Value based on input

Ex: %ascii_37% returns %

papi ecloud download Attribute

Adds placeholders to access Attributes. (Minecraft wiki) The expansion can be used only on 1.9+

papi ecloud download Bungee

Allows you to show, how many players are online on the entire network, or just on a specific server.

https://github.com/broken1arrow/CalculateNumbers/releases

The idea with this expansion is that you should be able to charge dynamically, for example in the deluxe menu. For tools, weapons and armor when players need to repair their belongings. Has also added optional so you can also combine it with rank plugin if you have one.

Use decimal,to get two decimal digits.

papi ecloud download changeoutput

Allows you to change the output based on what other placeholders return.

More information can be found on the GitHub Repository

All arguments can be replaced with other placeholders, wrapped in {}

papi ecloud download CheckItem

Allows you to check the inventory of a player for a certain item.

Notes: - mainhand and offhand work in getinfo:<slot> - give and remove placeholders are DISABLED by default for security purposes. See PlaceholderAPI config.yml file to enable.

Modifiers You can combine different modifiers to check for different values. Available modifiers are:

For nbt data you can use compounds by putting .. inside your string Example (%checkitem_nbtstrings:PublicBukkitValues..executableitems:ei-id=Free_Money%) ^

papi ecloud download CooldownBar

More info about this expansion can be found on the GitHub-Repository.

papi ecloud download Distance

This expansion provides placeholders to calculate the distance between two locations.

Supports placeholder inside placeholder, use {} instead of % for inner placeholders.

More info about this expansion can be found on the GitHub-Repository.

https://github.com/TeamVK/PAPI-Enchantment/releases

More info about this expansion can be found on the GitHub-Repository.

papi ecloud download Formatter

More info about this expansion can be found on the Codeberg-Repository.

[] is optional and <> is required. Use {{u}} for underscores and {{prc}} for percent symbols.

papi ecloud download GraalJS

More info about this expansion can be found on the GitHub-Repository.

Due to potential security issues is this expansion currently unverified. Use at your own risk.

Gives you a way, to use javascript, to give a different output, depending on conditions.

papi ecloud download ListPlayers

Lists players with a certain permission or in a certain world... 'nuf said.

papi ecloud download LocalTime

Please read the SimpleDateFormat Javadoc page about possible formats and this post about available time zone IDs for <TimeZoneID>.

papi ecloud download Math

Allows simple and advanced mathematical equations. Any placeholder that returns a number is supported (Use {placeholder} instead of %placeholder%)

Supports all calculations you can do with EvalEx. Note that the % can't be used within the placeholder and that you have to use [prc] instead.

More info on Codeberg

papi ecloud download MVdW

Lets you use placeholders from MVdWPlaceholderAPI. MVdWPlaceholderAPI and one of Maxims plugins, that use it, are required! A list of his placeholders can be found here

Due to possible security concerns is this expansion currently unverified. Use at your own risk.

<key> is a set query that can be found in the config.yml under plugins/PlaceholderAPI/expansion/MySQL.

https://github.com/TeamVK/PAPI-NumberFormatter/releases

More info about this expansion can be found on the PAPI-NumberFormatter.

if %tokenenchant_token_long% returns 43535709321, %nf_4X_tokenenchant_token_long% will return 43B, %nf_###E0X_tokenenchant_token_long% will return 43.5B, %nf_#,##0.#tokenenchant_token_long% will return 43,535,709,321 %nf#,##0.0#:IT_tokenenchant_token_long% will return 43.535.709.321.0

[] is optional and <> is required.

papi ecloud download OtherPlayer

Lets you get placeholders for other players. (Not the one that triggers the action)

papi ecloud download ParseNear

Lets you parse any placeholder for the closest player. Will return blank if no player is found.

papi ecloud download ParseOther

Lets you parse any placeholder for another player. You must use the unsafe placeholder to parse placeholders for username or uuid. Make sure to include the {} brackets, as it won't work without them.

papi ecloud download Pinger

Lets you ping a server through an IP or domain (with port), to check the online-status and to receive some information. The placeholders have a "warmup" time of around one or two minutes after installing the expansion.

Note: These placeholders have a separate update-delay in the config.yml of PlaceholderAPI

Replace testplugins.com:25565 with your own server/IP. %pinger_gameversion_testplugins.com:25565% %pinger_version_testplugins.com:25565% %pinger_online_testplugins.com:25565% %pinger_isonline_testplugins.com:25565% %pinger_max_testplugins.com:25565% %pinger_players_testplugins.com:25565% %pinger_motd_testplugins.com:25565% %pinger_pingversion_testplugins.com:25565% %pinger_online_testplugins.com:25565% and %pinger_isonline_testplugins.com:25565% do the exact same thing.

papi ecloud download Player

Gives you various placeholders for the player, that triggers the action.

papi ecloud download playerlist

More info about this expansion can be found on the GitHub-Repository.

Create a list in PAPI's config and retrieve it through placeholders! %playerlist_<listName>_<list|amount|#>%

papi ecloud download Plugin

Returns information about the specified plugin.

papi ecloud download progress

More info about this expansion can be found on the GitHub-Repository.

https://github.com/JasperLorelai/Expansion-PronounDB/releases

Shows the pronouns of a Minecraft player with a linked account on https://pronoundb.org/

papi ecloud download RainbowColor

More info about the expansion can be found on the GitHub-Repository.

papi ecloud download RandomColor

More info about the expansion can be found on the GitHub-Repository.

https://github.com/TeamVK/PAPI-RandomNumber/releases

More info about the expansion can be found on the GitHub-Repository.

It returns an auto-scaled random number. If you did not specify the scale, the scale will be automatically computed. If both min and max are integer numbers, the returned random number will also be an integer.

papi ecloud download RedisBungee

Same like the BungeeCord-placeholders, but for RedisBungee

papi ecloud download RelCon

More info about the expansion can be found on the GitHub-Repository.

papi ecloud download RNG

More info about the expansion can be found on the GitHub-Repository.

papi ecloud download reparser

Parses a provided input twice.

papi ecloud download ScoreboardObjectives

Get info from a scoreboard objective.

More info about the expansion can be found on the Spigot Page

papi ecloud download Server

Lets you get information about the server.

<time> is the date and time for the countdown. It needs to match the <SimpleDateTime>

Please read the SimpleDateFormat Javadoc page about possible formats.

papi ecloud download Shortcut

Allows to parse large amounts of text, including placeholders from PlaceholderAPI. Please visit the GitHub Repository for details and usage.

papi ecloud download Sound

Plays a sound, when parsed.

papi ecloud download SpeedPerSec

Note: Clicking is supported in left click only

papi ecloud download Statistic

Supports all statistics in SpigotAPI. %statistic_<StatisticType>%

For specific blocks, items, entities, ... # Blocks, items, entities, ... %statistic_mine_block:<material>% %statistic_use_item:<Item Material>% %statistic_break_item:<Item Material>% %statistic_craft_item:<Item Material>% %statistic_kill_entity:<MobType>% %statistic_entity_killed_by:<MobType>% # Other statistics %statistic_mob_kills% %statistic_mine_block% %statistic_use_item% %statistic_break_item% %statistic_craft_item% %statistic_ticks_played% %statistic_seconds_played% %statistic_minutes_played% %statistic_hours_played% %statistic_days_played% %statistic_time_played% %statistic_time_played:seconds% %statistic_time_played:minutes% %statistic_time_played:hours% %statistic_time_played:days% %statistic_animals_bred% %statistic_armor_cleaned% %statistic_banner_cleaned% %statistic_beacon_interacted% %statistic_boat_one_cm% %statistic_brewingstand_interaction% %statistic_cake_slices_eaten% %statistic_cauldron_filled% %statistic_cauldron_used% %statistic_chest_opened% %statistic_climb_one_cm% %statistic_crafting_table_interaction% %statistic_crouch_one_cm% %statistic_damage_dealt% %statistic_damage_taken% %statistic_deaths% %statistic_dispenser_inspected% %statistic_dive_one_cm% %statistic_drop% %statistic_dropper_inspected% %statistic_enderchest_opened% %statistic_fall_one_cm% %statistic_fish_caught% %statistic_flower_potted% %statistic_fly_one_cm% %statistic_furnace_interaction% %statistic_hopper_inspected% %statistic_horse_one_cm% %statistic_item_enchanted% %statistic_jump% %statistic_junk_fished% %statistic_leave_game% %statistic_minecart_one_cm% %statistic_noteblock_played% %statistic_noteblock_tuned% %statistic_pig_one_cm% %statistic_player_kills% %statistic_record_played% %statistic_sprint_one_cm% %statistic_swim_one_cm% %statistic_talked_to_villager% %statistic_time_since_death% %statistic_ticks_since_death% %statistic_seconds_since_death% %statistic_minutes_since_death% %statistic_hours_since_death% %statistic_days_since_death% %statistic_traded_with_villager% %statistic_trapped_chest_triggered% %statistic_walk_one_cm% %statistic_sleep_in_bed% %statistic_sneak_time% %statistic_aviate_one_cm%

papi ecloud download String

More info about the expansion can be found on the GitHub-Repository.

Supports placeholders using brackets: {placeholder}

https://www.spigotmc.org/resources/74959/

papi ecloud download teams

papi ecloud download unicode

Example: %unicode_1000% would show က

https://api.extendedclip.com/expansions/unixtime/

Example: %unixtime_1750277249389_dd.MM.yyyy-HH:mm:ss% would show 18.06.2025 20:07:29

papi ecloud download world

For the totalbalance placeholder, you must have a service provider plugin (eg. EssentialsX) to work.

Expansions listed here require the linked resource (plugin) to work properly.

Most of the listed Expansions are NOT made and maintained by the PlaceholderAPI team. Please see #510 for a list of all expansions officially maintained by the PlaceholderAPI team.

Available <check> values:

All information about these placeholders can be found here.

papi ecloud download AcidIsland

Global achievement placeholders: %aach_achievements% - Return the total unlocked achievements (number) %aach_achievements_percentage% - Return the total unlocked achievements (%) %aach_total_achievements% - Return the total achievements (number) Normal achievement placeholders for individual player statistics: %aach_connections% %aach_deaths% %aach_arrows% %aach_snowballs% %aach_eggs% %aach_fish% %aach_treasures% %aach_itembreaks% %aach_eatenitems% %aach_shear% %aach_milk% %aach_lavabuckets% %aach_waterbuckets% %aach_trades% %aach_anvilsused% %aach_enchantments% %aach_beds% %aach_maxlevel% %aach_consumedpotions% %aach_playedtime% %aach_itemdrops% %aach_itempickups% %aach_hoeplowings% %aach_fertilising% %aach_taming% %aach_brewing% %aach_fireworks% %aach_musicdiscs% %aach_enderpearls% %aach_smelting% %aach_petmastergive% %aach_petmasterreceive% %aach_distancefoot% %aach_distancepig% %aach_distancehorse% %aach_distanceminecart% %aach_distanceboat% %aach_distancegliding% %aach_distancellama% %aach_distancesneaking% %aach_raidswon% %aach_riptides% %aach_advancementscompleted% Multiple Achievement Placeholders for individual player statistics: %aach_places_[blockname]% - example: %aach_places_dirt% %aach_breaks_[blockname]% - example: %aach_breaks_stone% %aach_kills_[entityname]% - example: %aach_kills_zombie% %aach_targetsshot_[targetname]% - example: %aach_targetsshot_zombie% %aach_crafts_[itemname]% - example: %aach_crafts_bread% %aach_breeding_[entityname]% - example: %aach_breeding_pig% %aach_playercommands_[command]% - example: %aach_playercommands_aach list% %aach_custom_[customname]% - example: %aach_custom_votes% %aach_jobsreborn_[job]% - example: %aach_jobsreborn_hunter% Placeholders for total category achievements: %aach_total_connections% %aach_total_deaths% %aach_total_arrows% %aach_total_snowballs% %aach_total_eggs% %aach_total_fish% %aach_total_treasures% %aach_total_itembreaks% %aach_total_eatenitems% %aach_total_shear% %aach_total_milk% %aach_total_lavabuckets% %aach_total_waterbuckets% %aach_total_trades% %aach_total_anvilsused% %aach_total_enchantments% %aach_total_beds% %aach_total_maxlevel% %aach_total_consumedpotions% %aach_total_playedtime% %aach_total_itemdrops% %aach_total_itempickups% %aach_total_hoeplowings% %aach_total_fertilising% %aach_total_taming% %aach_total_brewing% %aach_total_fireworks% %aach_total_musicdiscs% %aach_total_enderpearls% %aach_total_smelting% %aach_total_petmastergive% %aach_total_petmasterreceive% %aach_total_distancefoot% %aach_total_distancepig% %aach_total_distancehorse% %aach_total_distanceminecart% %aach_total_distanceboat% %aach_total_distancegliding% %aach_total_distancellama% %aach_total_distancesneaking% %aach_total_raidswon% %aach_total_riptides% %aach_total_advancementscompleted% %aach_total_places% %aach_total_breaks% %aach_total_kills% %aach_total_targetsshot% %aach_total_crafts% %aach_total_breeding% %aach_total_playercommands% %aach_total_custom% %aach_total_commands% %aach_total_jobsreborn%

For more info, visit the wiki of the plugin.

Description of placeholders

Description of placeholders

Examples: %animatedmenu_status_testplugins.com_&aOnline_&cOffline% %animatedmenu_status_testplugins.com_25565_&aOnline_&cOffline%

papi ecloud download AParkour

papi ecloud download ASkyBlock

papi ecloud download AutoRank

papi ecloud download AutoSell

Find examples of how the placeholders can be used on signs and scoreboards.

Find an up-to-date list on the SpigotMC page.

Check out BentoBox placeholders docs for more placeholders.

Replace [gamemode] with one of the following options:

Please refer to the official documentation for more info.

Please check the wiki for more info.

papi ecloud download BlockParty

papi ecloud download BuildBattlePro

https://www.spigotmc.org/resources/82261/

papi ecloud download ChatReaction

papi ecloud download CheckNameHistory

papi ecloud download CraftConomy

papi ecloud download DeluxeChat

papi ecloud download DeluxePM

Placeholders information can be found on Github

You can find an up-to-date list of placeholders on the DiscordSRV Wiki.

papi ecloud download Disease

Replace <n> with a number from 1 to whatever.

papi ecloud download Enjin

papi ecloud download Envoys

papi ecloud download Essentials

This expansion works with both Essentials and EssentialsX (Second one is recommended).

papi ecloud download EZBlocks

papi ecloud download EZPrestige

papi ecloud download EZRanksPro

papi ecloud download Factions

You can find an up-to-date list of placeholders on the FactionsUUID Wiki.

These placeholders work with FactionsUUID and MCore all you need is downloading the expansion of the plugin you're using. if you're using these placeholders in DeluxeChat you need to enable this option "relation_placeholders_enabled: true" you can find that in the config.

papi ecloud download GemsEconomy

papi ecloud download GriefPrevention

papi ecloud download Heroes

Get information about your players from Honeypot. Please refer to the Wiki for more detailed information.

You can find an up-to-date list of placeholders in the HyacinthHello wiki.

Supports ASkyBlock, BentoBox, uSkyBlock and AcidIsland.

papi ecloud download Karma

papi ecloud download KillStats

You can find an up-to-date list of placeholders on the KingdomsX wiki.

A Description of the placeholders can be found on the Lands Wiki.

More info about these placeholders can be found here.

papi ecloud download lemonmobcoins

papi ecloud download LuckPerms

You can find an up-to-date list of placeholders on the LuckPerms wiki.

All placeholders generally support async access as well. You may also find an official list on the MBedwars Wiki.

These are available for each arena, with <arena> being the name of it: %mbedwars_arena-<arena>-displayname% %mbedwars_arena-<arena>-authors% %mbedwars_arena-<arena>-players% %mbedwars_arena-<arena>-maxplayers% %mbedwars_arena-<arena>-minplayers% %mbedwars_arena-<arena>-status% %mbedwars_arena-<arena>-teams% %mbedwars_arena-<arena>-teamsize%

These depend on the arena in which the player is currently playing within: %mbedwars_playerarena-name% %mbedwars_playerarena-displayname% %mbedwars_playerarena-authors% %mbedwars_playerarena-players% %mbedwars_playerarena-maxplayers% %mbedwars_playerarena-status% %mbedwars_playerarena-teams% %mbedwars_playerarena-teamsize% %mbedwars_playerarena-current-team% %mbedwars_playerarena-current-team-color% %mbedwars_playerarena-current-team-initials% %mbedwars_playerarena-team-<team>-size% %mbedwars_playerarena-team-<team>-status%

These are the total stats of the player. APIs are able to add their own ones, with their general format being %mbedwars_stats-<id>%. The ones that MBedwars provides are the following: %mbedwars_stats-rank% %mbedwars_stats-wins% %mbedwars_stats-loses% %mbedwars_stats-win_streak% %mbedwars_stats-top_win_streak% %mbedwars_stats-rounds_played% %mbedwars_stats-wl% %mbedwars_stats-kills% %mbedwars_stats-final_kills% %mbedwars_stats-deaths% %mbedwars_stats-final_deaths% %mbedwars_stats-kd% %mbedwars_stats-beds_destroyed% %mbedwars_stats-beds_lost% %mbedwars_stats-play_time%

These are the stats of the current match of which the player is a part of. APIs are able to add their own ones, with their general format being %mbedwars_gamestats-<id>%. The ones that MBedwars provides are the following: %mbedwars_gamestats-kills% %mbedwars_gamestats-final_kills% %mbedwars_gamestats-deaths% %mbedwars_gamestats-kd% %mbedwars_gamestats-beds_destroyed% %mbedwars_gamestats-play_time%

These display the amount of players per mode. You may add own modes using the players-in-mode-placeholders config: %mbedwars_players-in-mode-all% %mbedwars_players-in-mode-solos% %mbedwars_players-in-mode-doubles% %mbedwars_players-in-mode-trios% %mbedwars_players-in-mode-quads%

Miscellaneous placeholders: %mbedwars_achievements-earned-count%

papi ecloud download marriage

papi ecloud download MineCrates

The below Placeholders are only for Multiverse-Core v5!

All placeholders allow a _<world> to be added with <world> being the name of a Multiverse-loaded World. Example: %multiverse-core_alias_myworld%

papi ecloud download multiverse

You can find more information on the Wiki.

papi ecloud download Nicknamer

papi ecloud download Nicky

papi ecloud download OnTime

Description and usage for placeholders

You can find an up-to-date list of placeholders on the OreAnnouncer Wiki.

Replace <map_name> with name of the map you wish to get time for. Replace <player_name> with name of the player you wish to display time for. Replace <position> with number that coresponds to the position you want to display.

Replace <AttractionID> with the ID of your attraction. Replace <Position> with the ridecount position. Replace [Type] with the top type. Supported values: DAILY, WEEKLY, MONTHLY, YEARLY, TOTAL

The plugin provides placeholders for statistics stored in the plugin for players and the server.

Check Plan Wiki for the placeholders list.

papi ecloud download playerstats

For more information and usage examples, see the PlayerStatsExpansion GitHub.

For a detailed explanation of how to use PlayTimeManager's placeholders, you can take a look at the PlayTimeManager Wiki.

<server> is the name of the server it should show the player count of.

Each placeholder has a shorter alias, which follows the primary placeholder below.

Prison uses PlaceholderAPI to support any plugin placeholders within the GUI Ranks Lore and the GUI Mine Lore.

Prison Placeholder Attributes:

Prison supports Placeholder Attributes which allows an infinite way to customize most placeholders, such as numeric formatting, hex colors, and reductions. Can customize any bar-graph for character codes, colors, and size.

Simple examples using placeholder attributes with the results following each example. Colors are not shown.

PLAYER placeholders are used directly with a player, such as with player chat prefixes and scoreboards.

Rank related placeholders apply to all ranks that a player may have, and may return more than one value. Use the LADDER placeholders to control the order that is displayed. Rank based placeholder can return zero, one, or more rank related values depending upon how many ladders the player is on.

Must be used directly with a player, and returns the information related to their active rank on the specified ladder.

Use the ladder name, all lowercase, in place of <laddername>, and it will return zero or one rank related values.

RANKS placeholders deal directly with specific rank information.

Use the rank name in place of <rankname>, and may return zero or one value.

RANKPLAYERS placeholders are used with players and shows what their adjusted costs are for the specified rank. These placeholders are ideal for showing a player how much each rank will cost using their personal rank cost multipliers.

Use the rank name in place of <rankname>, and may return zero or one value.

MINES placeholder provides stats for the given mine.

Use the mine name in place of <minename>, and may return zero or one value.

Note: The placeholders %prison_top_mine_block_line_header_<minename>% and %prison_top_mine_block_line_totals_<minename>% are used with the STATSMINES placeholders and provide the headers and total details for the given mines.

MINEPLAYERS placeholders are tied to a player and dynamically shows the details of the mine the player is in, or blanks when not in a mine. These are ideal for use in scoreboards or chat prefixes.

Must be used with a player.

PLAYERBLOCKS placeholders are tied to a player, but through the mines modules. The placeholders that are supported are one for each block type that is defined in all mines.

Must be used with a player. The use of <blockname> is the name of the block as provided with the command /mines block search help, but all lowercase and any ":" should use "-" instead. These placeholders will return a value of 0 or more. If the block name is invalid it will return a blank.

Examples: prison_player_total_blocks__cobblestone prison_player_total_blocks__customitems-compressedcobblestone

The STATSMINES placeholders represents the blocks that in the specified mine. The value nnn should be replaced with a number starting with a 1, or 001 and refers to one block. The "line placeholder is composed of the other placeholders and can simplify the use of these placeholders. See the headers and footer totals within the MINES placeholders.

Use the mine name in place of <minename>, and may return zero or one value. Invalid values for _nnn_ will return blanks.

The STATSRANKS placeholders represents the top-n players for a given rank. The value nnn should be replaced with a number starting with a 1, or 001 and refers to a given player.

Use the mine name in place of <rankname>, and may return zero or one value. Invalid values for _nnn_ will return blanks.

papi ecloud download PrisonMines

You can find an up-to-date list of placeholders in the ProtectionStones Wiki.

For a description of the placeholders please read the PvPManager Wiki

papi ecloud download Quests

papi ecloud download QuickSell

%treasuresrecentfind_find_number_<number>% %treasuresrecentfind_from_first_<number>% 1 is most recent, 2 is second most, 3 third most, etc.

<name> is the name you configured in the config.yml of this plugin. Read More

papi ecloud download rogueparkour-temporary

You can find an up-to-date list of placeholders with detailed information and examples in the ScreamingBedWars Documentation.

Replace [world] with the name of a loaded world. Placeholders ending in a [world] will retrieve information from the specified world instead of the player's current world.

Replace [variable name] with the name of the signlink variable.

You can find an up-to-date list of placeholders in the SimpleClans Wiki.

papi ecloud download SimplePrefix

papi ecloud download SkillAPI

The following placeholders are the same as above but instead of specifying the skillName, you can specify a number from 1 to pretty much infinity (amount of skills a player has) which will show the information related to the players 1st, 2nd, 3rd skill and so on... %skillapi_player_skill_points_<#>% %skillapi_player_skill_level_<#>% %skillapi_player_skill_levelreq_<#>% %skillapi_player_skill_name_<#>% %skillapi_player_skill_message_<#>% %skillapi_player_skill_req_<#>% %skillapi_player_skill_type_<#>% %skillapi_player_skill_can_autolevel_<#>% %skillapi_player_skill_can_cast_<#>%

papi ecloud download SkinsRestorer

https://api.extendedclip.com/expansions/skippi/

papi ecloud download spark

papi ecloud download StaffFacilities

papi ecloud download staffplusplus

All placeholders are listed here: https://wiki.staffplusplus.org/integrations/papi-expansion

papi ecloud download Statz

papi ecloud download SuperbVote

papi ecloud download ThemePark

Replace <AttractionID> with the ID of your attraction. Replace <Position> with the ridecount position. Replace [Type] with the top type. Supported values: DAILY, WEEKLY, MONTHLY, YEARLY, TOTAL

papi ecloud download Thirst

If you add _long to the cost related placeholder, it will returne a number without comma/decimal point.

You can find an up-to-date list of placeholders in the Towny wiki.

papi ecloud download TownyChat

Detailed explanation and example outputs of placeholders are listed on modrinth.

papi ecloud download uSkyBlock

*Add rel_ before placeholder and tag to support relational placeholder

papi ecloud download UltimateVotes

You can find an up-to-date list of placeholders in the Ultra Economy Wiki.

You can find an up-to-date list of placeholders in the Ultra Motd Wiki.

You can find an up-to-date list of placeholders in the Ultra Permissions Wiki.

You can find an up-to-date list of placeholders in the Ultra Punishments Wiki.

You can find an up-to-date list of placeholders in the Ultra Regions Wiki.

papi ecloud download UnityGen

papi ecloud download Vault

papi ecloud download ViaVersion

You can find an up-to-date list of placeholders on the VoteParty wiki.

papi ecloud download VoteRoulette

papi ecloud download VotingPlugin

papi ecloud download WorldBorder

papi ecloud download WorldGuard

papi ecloud download XLTournaments

**Examples:**

Example 1 (typescript):
```typescript
%advancements_<advancement>%
%advancements_player_<player>;<advancement>%
%advancements_list%
%advancements_list_<command>%
%advancements_playerList_<player>%
%advancements_playerList_<player>,<command>%
%advancements_listFormat%
%advancements_playerListFormat_<player>%
%advancements_completedAmount%
%advancements_completedAmount_<category>%
%advancements_playerCompletedAmount_<player>%
%advancements_playerCompletedAmount_<player>,<category>%
%advancements_remainingAmount%
%advancements_remainingAmount_<category>%
%advancements_playerRemainingAmount_<player>%
%advancements_playerRemainingAmount_<player>,<category>%
```

Example 2 (jsx):
```jsx
%animations_<tag>Text</tag>%
%animations_<tag option>Text</tag>%
%animations_<tag option=:value>Text</tag>%
```

Example 3 (unknown):
```unknown
Chose one value that's inside () and replace SLOT with one of the following: helmet, chestplate, leggings, boots.

%armor_amount_SLOT%
%armor_color_(red/green/blue/hex)_SLOT%
%armor_durability_(left/max)_SLOT%
%armor_has_SLOT%
%armor_material_SLOT%
%armor_maxamount_SLOT%
```

Example 4 (typescript):
```typescript
%ascii_<value>%
```

---

## Commands¶

**URL:** https://wiki.placeholderapi.com/users/commands/

**Contents:**
- Commands¶
- Overview¶
  - Parse Commands¶
    - /papi bcparse¶
    - /papi cmdparse¶
    - /papi parse¶
    - /papi parserel¶
  - eCloud Commands¶
    - /papi ecloud clear¶
    - /papi ecloud disable¶

This page shows all commands, including with a detailed description of what every command does.

These commands are used to parse placeholders into their respective values. Useful for debugging.

Description: Parses placeholders of a String and broadcasts the result to all players.

Example: /papi bcparse funnycube My name is %player_name%!

Description: Parses placeholders of a String and executes it as a command.

Example: /papi cmdparse funnycube say My name is %player_name%!

Description: Parses the placeholders in a given text and shows the result.

Example: /papi parse funnycube My group is %vault_group%

Description: Parses a relational placeholder.

Example: /papi parserel funnycube extended_clip %placeholder%

These commands all start with /papi ecloud and are used for things related about the Expansion Cloud. Only executing /papi ecloud without any arguments will list all commands available for it.

Description: Clears the cache for the eCloud.

Description: Disables the connection to the eCloud.

Description: Allows you to download an expansion from the eCloud

Example: /papi ecloud download Vault /papi ecloud download Vault 1.5.2

Description: Enables the connection to the eCloud

Description: Gives information about a specific Expansion.

Example: /papi ecloud info Vault

Description: Lists either all Expansions on the eCloud, only those by a specific author or only those that you have installed. Installed Expansions show as green in the list and Expansions that are installed and have an update available show as gold.

Example: /papi ecloud list all /papi ecloud list clip /papi ecloud list installed

Description: List all placeholders of an Expansion.

Example: /papi ecloud placeholders Vault

Description: Refresh the cached data from the eCloud.

Description: Displays the actual Status of the eCloud.

These commands can be used to manage the expansions that you have currently installed.

Description: Gives you information about the specified Expansion.

Example: /papi info Vault

Description: Lists all active/registered expansions. This is different to /papi ecloud list installed in the fact, that it also includes expansions that were installed through a plugin (That aren't a separate jar-file) and it also doesn't show which one have updates available.

Description: Registers an expansion from a specified filename. This is useful in cases, where you downloaded the expansion manually and don't want to restart the server. The file needs to be inside /plugins/PlaceholderAPI/expansions.

Example: /papi register MyExpansion.jar

Description: Unregisters the specified expansion.

Example: /papi unregister MyExpansion.jar

These are other commands of PlaceholderAPI that don't fit any of the above categories.

Description: Pastes useful information from PlaceholderAPI such as plugin version, server version and installed expansions to https://paste.helpch.at for simple sharing and support.

Description: Displays all the commands PlaceholderAPI currently offers.

Description: Reloads the config settings. You need to use this command after downloading Expansions from the eCloud or they won't be properly registered.

Description: Shows the current version and authors of PlaceholderAPI.

**Examples:**

Example 1 (unknown):
```unknown
/papi bcparse funnycube My name is %player_name%!
```

Example 2 (unknown):
```unknown
/papi cmdparse funnycube say My name is %player_name%!
```

Example 3 (unknown):
```unknown
/papi parse funnycube My group is %vault_group%
```

Example 4 (unknown):
```unknown
/papi parserel funnycube extended_clip %placeholder%
```

---

## User Guides¶

**URL:** https://wiki.placeholderapi.com/users/

**Contents:**
- User Guides¶
  - Commands¶
  - Using Placeholders¶
  - Placeholder List¶
  - Plugins using PlaceholderAPI¶

The pages listed under this section are meant for server owners who want to use PlaceholderAPI.

List of all available commands in PlaceholderAPI.

User Guide on how to use placeholders in a plugin.

Community-curated list of available PlaceholderExpansions and their placeholders.

List of Plugins that support PlaceholderAPI and/or provide their own placeholders to use.

---

## Using Placeholders¶

**URL:** https://wiki.placeholderapi.com/users/using-placeholders/

**Contents:**
- Using Placeholders¶
- Prerequisites¶
  - Plugin supports PlaceholderAPI¶
  - Proper Internet connection¶
- Download/Get Expansion¶
- Use Expansion¶

This page is intended for server owners or server staff who want to learn how to use placeholders in a plugin.

If you're a developer and would like to learn how to provide placeholders or support placeholders from other plugins in your own, check out Using PlaceholderAPI.

Before you can use placeholders should you check a few things first.

The first and most important thing is, to find out if the plugin you want to use placeholders in is actually supporting PlaceholderAPI. Chat-plugins such as EssentialsXChat do not natively support PlaceholderAPI and instead require separate plugins to "inject" the parsed placeholders into the final chat message.

One way to check, if a Plugin is supporing PlaceholderAPI, is to check the Plugins using PlaceholderAPI page. If the plugin is listed and if the Supports placeholders text has a check, does it mean that PlaceholderAPI support is available.

If the plugin isn't listed, can you usually check its plugin page, or any other source of information, such as a wiki, for clues on if PlaceholderAPI is supported.

PlaceholderAPI connects towards an eCloud located under https://api.extendedclip.com to retrieve information about placeholder expansions, but also to download said expansions from it. Make sure that your server is allowing external connections to the above URL. If it doesn't, and you're using a host, contact their support and ask them to whitelist this URL.

PlaceholderAPI provides and checks for a specific Environment variable to block the download of specific expansions. Should you as a host want to block the download of specific expansions, add the PAPI_BLOCKED_EXPANSIONS Environment variable containing a comma-separated list of expansion names that PlaceholderAPI should not be able to download.

This feature exists since version 2.11.4 of PlaceholderAPI

The way PlaceholderAPI's system works, allows a Placeholder Expansion and its corresponding placeholders to either be included within a plugin (If placeholder requires said plugin) or to be available as a separate jar file on the eCloud of PlaceholderAPI. Depending on what type you have, will you need to do some extra steps to use the placeholder from the Placeholder Expansion.

One way to find out, if an Expansion is included or separate, is to check the Placeholder List page for any entry of it. If it exists on the page, can you check the infobox right below the title of the Expansion for one of the following cases:

You can check what expansions are loaded by running /papi list.

Using the placeholders of the Expansion is a straigh forward process. Simply put the right placeholder format (i.e. %player_name%) inside whatever configuration option supports it. Please refer to any manuals or wikis a plugin may offer about what options support placeholders.

---

## Plugins using PlaceholderAPI¶

**URL:** https://wiki.placeholderapi.com/users/plugins-using-placeholderapi/

**Contents:**
- Plugins using PlaceholderAPI¶
- Plugins¶
- A¶
- B¶
- C¶
- D¶
- E¶
- F¶
- G¶
- H¶

This here is a list of all plugins supporting PlaceholderAPI by either having their own placeholders added, or just allowing other placeholders to be used. If your plugin isn't shown here and you want it to be added, read the Wiki README on how you can submit your changes.

---
