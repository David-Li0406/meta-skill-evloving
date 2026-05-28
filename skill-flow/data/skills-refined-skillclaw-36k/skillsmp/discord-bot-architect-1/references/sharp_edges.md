# Discord Bot Architect - Sharp Edges

## Interaction Timeout (3 Second Rule)

### **Id**
3-second-interaction-timeout
### **Severity**
critical
### **Situation**
Handling slash commands, buttons, select menus, or modals
### **Symptom**
  User sees "This interaction failed" or "The application did not respond."
  Command works locally but fails in production.
  Slow operations never complete.
  
### **Why**
  Discord requires ALL interactions to be acknowledged within 3 seconds:
  - Slash commands
  - Button clicks
  - Select menu selections
  - Context menu commands
  
  If you do ANY slow operation (database, API, file I/O) before responding,
  you'll miss the window. Discord shows an error even if your bot processes
  the request correctly afterward.
  
  After acknowledgment, you have 15 minutes for follow-up responses.
  
### **Solution**
  ## Acknowledge immediately, process later
  
  ```javascript
  // Discord.js - Defer for slow operations
  module.exports = {
    async execute(interaction) {
      // DEFER IMMEDIATELY - before any slow operation
      await interaction.deferReply();
      // For ephemeral: await interaction.deferReply({ ephemeral: true });
  
      // Now you have 15 minutes
      const result = await slowDatabaseQuery();
      const aiResponse = await callLLM(result);
  
      // Edit the deferred reply
      await interaction.editReply(`Result: ${aiResponse}`);
    }
  };
  ```
  
  ```python
  # Pycord
  @bot.slash_command()
  async def slow_command(ctx):
      await ctx.defer()  # Acknowledge immediately
      # await ctx.defer(ephemeral=True)  # For private response
  
      result = await slow_operation()
      await ctx.followup.send(f"Result: {result}")
  ```
  
  ## For components (buttons, menus)
  
  ```javascript
  // If you're updating the message
  await interaction.deferUpdate();
  
  // If you're sending a new response
  await interaction.deferReply({ ephemeral: true });
  ```
  
### **Detection Pattern**
  - interaction failed
  - application did not respond
  - timeout
  - 3 second

## Missing Privileged Intent Configuration

### **Id**
privileged-intents-missing
### **Severity**
critical
### **Situation**
Bot needs member data, presences, or message content
### **Symptom**
  Members intent: member lists empty, on_member_join doesn't fire
  Presences intent: statuses always unknown/offline
  Message content intent: message.content is empty string
  
### **Why**
  Discord has 3 privileged intents that require manual enablement:
  1. **GUILD_MEMBERS** - Member join/leave, member lists
  2. **GUILD_PRESENCES** - Online status, activities
  3. **MESSAGE_CONTENT** - Read message text (deprecated for commands)
  
  These must be:
  1. Enabled in Discord Developer Portal > Bot > Privileged Gateway Intents
  2. Requested in your bot code
  
  At 100+ servers, you need Discord verification to keep using them.
  
### **Solution**
  ## Step 1: Enable in Developer Portal
  
  ```
  1. Go to https://discord.com/developers/applications
  2. Select your application
  3. Go to Bot section
  4. Scroll to Privileged Gateway Intents
  5. Toggle ON the intents you need
  ```
  
  ## Step 2: Request in code
  
  ```javascript
  // Discord.js
  const { Client, GatewayIntentBits } = require('discord.js');
  
  const client = new Client({
    intents: [
      GatewayIntentBits.Guilds,
      GatewayIntentBits.GuildMembers,       // PRIVILEGED
      // GatewayIntentBits.GuildPresences,  // PRIVILEGED
      // GatewayIntentBits.MessageContent,  // PRIVILEGED - avoid!
    ]
  });
  ```
  
  ```python
  # Pycord
  intents = discord.Intents.default()
  intents.members = True       # PRIVILEGED
  # intents.presences = True   # PRIVILEGED
  # intents.message_content = True  # PRIVILEGED - avoid!
  
  bot = commands.Bot(intents=intents)
  ```
  
  ## Avoid Message Content Intent if possible
  
  Use slash commands, buttons, and modals instead of message parsing.
  These don't require the Message Content intent.
  
### **Detection Pattern**
  - intent
  - members
  - message_content
  - privileged
  - empty

## Command Registration Rate Limited

### **Id**
command-registration-rate-limit
### **Severity**
high
### **Situation**
Registering slash commands
### **Symptom**
  Commands not appearing. 429 errors when deploying.
  "You are being rate limited" messages.
  Commands appear for some guilds but not others.
  
### **Why**
  Command registration is rate limited:
  - Global commands: 200 creates/day, updates take up to 1 hour to propagate
  - Guild commands: 200 creates/day per guild, instant update
  
  Common mistakes:
  - Registering commands on every bot startup
  - Registering in every guild separately
  - Making changes in a loop without delays
  
### **Solution**
  ## Use a separate deploy script (not on startup)
  
  ```javascript
  // deploy-commands.js - Run manually, not on bot start
  const { REST, Routes } = require('discord.js');
  
  const rest = new REST().setToken(process.env.DISCORD_TOKEN);
  
  async function deploy() {
    // For development: Guild commands (instant)
    if (process.env.GUILD_ID) {
      await rest.put(
        Routes.applicationGuildCommands(
          process.env.CLIENT_ID,
          process.env.GUILD_ID
        ),
        { body: commands }
      );
      console.log('Guild commands deployed instantly');
    }
  
    // For production: Global commands (up to 1 hour)
    else {
      await rest.put(
        Routes.applicationCommands(process.env.CLIENT_ID),
        { body: commands }
      );
      console.log('Global commands deployed (may take up to 1 hour)');
    }
  }
  
  deploy();
  ```
  
  ```python
  # Pycord - Don't sync on every startup
  @bot.event
  async def on_ready():
      # DON'T DO THIS:
      # await bot.sync_commands()
  
      print(f"Ready! Commands should already be registered.")
  
  # Instead, sync manually or use a flag
  if __name__ == "__main__":
      if "--sync" in sys.argv:
          # Only sync when explicitly requested
          bot.sync_commands_on_start = True
      bot.run(token)
  ```
  
  ## Testing workflow
  
  1. Use guild commands during development (instant updates)
  2. Only deploy global commands when ready for production
  3. Run deploy script manually, not on every restart
  
### **Detection Pattern**
  - rate limit
  - 429
  - command
  - register

## Bot Token Exposed

### **Id**
token-exposure
### **Severity**
critical
### **Situation**
Storing or sharing bot token
### **Symptom**
  Unauthorized actions from your bot.
  Bot joins random servers.
  Bot sends spam or malicious content.
  "Invalid token" after Discord invalidates it.
  
### **Why**
  Your bot token provides FULL control over your bot. Attackers can:
  - Send messages as your bot
  - Join servers, create invites
  - Access all data your bot can access
  - Potentially take over servers where bot has admin
  
  Discord actively scans GitHub for exposed tokens and invalidates them.
  Common exposure points:
  - Committed to Git
  - Shared in Discord itself
  - In client-side code
  - In public screenshots
  
### **Solution**
  ## Never hardcode tokens
  
  ```javascript
  // BAD - never do this
  const token = 'MTIzNDU2Nzg5MDEyMzQ1Njc4.ABCDEF.xyz...';
  
  // GOOD - environment variables
  require('dotenv').config();
  client.login(process.env.DISCORD_TOKEN);
  ```
  
  ## Use .gitignore
  
  ```
  # .gitignore
  .env
  .env.local
  config.json
  ```
  
  ## If token is exposed
  
  1. Go to Developer Portal immediately
  2. Regenerate the token
  3. Update all deployments
  4. Review bot activity for unauthorized actions
  5. Check git history and force push to remove if needed
  
  ## Use environment variables properly
  
  ```bash
  # .env (never commit)
  DISCORD_TOKEN=your_token_here
  CLIENT_ID=your_client_id
  ```
  
  ```javascript
  // Load with dotenv
  require('dotenv').config();
  const token = process.env.DISCORD_TOKEN;
  ```
  
### **Detection Pattern**
  - token
  - MTI
  - exposed
  - leaked

## Bot Missing applications.commands Scope

### **Id**
missing-application-commands-scope
### **Severity**
high
### **Situation**
Slash commands not appearing for users
### **Symptom**
  Bot is in server but slash commands don't show up.
  Typing / shows no commands from your bot.
  Commands worked in development server but not others.
  
### **Why**
  Discord has two important OAuth scopes:
  - `bot` - Traditional bot permissions (messages, reactions, etc.)
  - `applications.commands` - Slash command permissions
  
  Many bots were invited with only the `bot` scope before slash commands
  existed. They need to be re-invited with both scopes.
  
### **Solution**
  ## Generate correct invite URL
  
  ```
  https://discord.com/api/oauth2/authorize
    ?client_id=YOUR_CLIENT_ID
    &permissions=0
    &scope=bot%20applications.commands
  ```
  
  ## In Discord Developer Portal
  
  1. Go to OAuth2 > URL Generator
  2. Select BOTH:
     - `bot`
     - `applications.commands`
  3. Select required bot permissions
  4. Use generated URL
  
  ## Re-invite without kicking
  
  Users can use the new invite URL even if bot is already in server.
  This adds the new scope without removing the bot.
  
  ```javascript
  // Generate invite URL in code
  const inviteUrl = client.generateInvite({
    scopes: ['bot', 'applications.commands'],
    permissions: [
      'SendMessages',
      'EmbedLinks',
      // Add other needed permissions
    ]
  });
  ```
  
### **Detection Pattern**
  - commands not showing
  - slash commands missing
  - scope
  - applications.commands

## Global Commands Not Appearing Immediately

### **Id**
global-command-delay
### **Severity**
medium
### **Situation**
Deploying global slash commands
### **Symptom**
  Commands don't appear after deployment.
  Guild commands work but global commands don't.
  Commands appear after an hour.
  
### **Why**
  Global commands can take up to 1 hour to propagate to all Discord servers.
  This is by design for Discord's caching and CDN.
  
  Guild commands are instant but only work in that specific guild.
  
### **Solution**
  ## Development: Use guild commands
  
  ```javascript
  // Instant updates for testing
  await rest.put(
    Routes.applicationGuildCommands(CLIENT_ID, GUILD_ID),
    { body: commands }
  );
  ```
  
  ## Production: Deploy global commands during off-peak
  
  ```javascript
  // Takes up to 1 hour to propagate
  await rest.put(
    Routes.applicationCommands(CLIENT_ID),
    { body: commands }
  );
  ```
  
  ## Workflow
  
  1. Develop and test with guild commands (instant)
  2. When ready, deploy global commands
  3. Wait up to 1 hour for propagation
  4. Don't deploy global commands frequently
  
### **Detection Pattern**
  - commands not appearing
  - global
  - propagate
  - hour

## Frequent Gateway Disconnections

### **Id**
gateway-disconnect
### **Severity**
medium
### **Situation**
Bot randomly goes offline or misses events
### **Symptom**
  Bot shows as offline intermittently.
  Events are missed (member joins, messages).
  Reconnection messages in logs.
  
### **Why**
  Discord gateway requires regular heartbeats. Issues:
  - Blocking operations prevent heartbeat
  - Network instability
  - Memory pressure causing GC pauses
  - Too many guilds without sharding (2500+ requires sharding)
  
### **Solution**
  ## Never block the event loop
  
  ```javascript
  // BAD - blocks event loop
  const data = fs.readFileSync('file.json');
  
  // GOOD - async
  const data = await fs.promises.readFile('file.json');
  ```
  
  ## Handle reconnections gracefully
  
  ```javascript
  client.on('shardResume', (id, replayedEvents) => {
    console.log(`Shard ${id} resumed, replayed ${replayedEvents} events`);
  });
  
  client.on('shardDisconnect', (event, id) => {
    console.log(`Shard ${id} disconnected`);
  });
  
  client.on('shardReconnecting', (id) => {
    console.log(`Shard ${id} reconnecting...`);
  });
  ```
  
  ## Implement sharding at scale
  
  ```javascript
  // Required at 2500+ guilds
  const manager = new ShardingManager('./bot.js', {
    token: process.env.DISCORD_TOKEN,
    totalShards: 'auto'
  });
  manager.spawn();
  ```
  
### **Detection Pattern**
  - disconnect
  - offline
  - heartbeat
  - reconnect

## Modal Must Be First Response

### **Id**
modal-must-be-first
### **Severity**
medium
### **Situation**
Showing a modal from a slash command or button
### **Symptom**
  "Interaction has already been acknowledged" error.
  Modal doesn't appear.
  Works sometimes but not others.
  
### **Why**
  Modals have a special requirement: showing a modal MUST be the first
  response to an interaction. You cannot:
  - defer() then showModal()
  - reply() then showModal()
  - Think for more than 3 seconds then showModal()
  
### **Solution**
  ## Show modal immediately
  
  ```javascript
  // CORRECT - modal is first response
  async execute(interaction) {
    const modal = new ModalBuilder()
      .setCustomId('my-modal')
      .setTitle('Input Form');
  
    // Show immediately - no defer, no reply first
    await interaction.showModal(modal);
  }
  ```
  
  ```javascript
  // WRONG - deferred first
  async execute(interaction) {
    await interaction.deferReply();  // CAN'T DO THIS
    await interaction.showModal(modal);  // Will fail
  }
  ```
  
  ## If you need to check something first
  
  ```javascript
  async execute(interaction) {
    // Quick sync check is OK (under 3 seconds)
    if (!hasPermission(interaction.user.id)) {
      return interaction.reply({
        content: 'No permission',
        ephemeral: true
      });
    }
  
    // Show modal (still first interaction response for this path)
    await interaction.showModal(modal);
  }
  ```
  
### **Detection Pattern**
  - modal
  - already acknowledged
  - showModal