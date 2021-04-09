# Discord Trollbot
## About

Discord Trollbot is a rather simple Discord Bot to troll and annoy your friends on Discord. You can spam, delete, mute, deafen, move, play soundclips and much more.
## Features
|   | | 
| ------------- |:-------------
|_addTarget @user [length]|adds a target to the spam list[*1]
|_delTarget @user [length]|removes a target from the spam list[*1]
|_blacklist @user|adds user to the blacklist[*2]
|_unblacklist @user|removes user from the blacklist[*2]
|_addSudoer @user|adds user to the sudoers list[*3]
|_delSudoer @user|removes user from the sudoers list[*3]
|_addSuperUser @user|makes user a super user[*4]
|_delSuperUser @user|removes user from super users[*4]
|_voiceBlacklist @user|adds user to the voice blacklist[*5]
|_delVoiceBlacklist @user|removes user from the voice blacklist [*5]
|_spam @user [length]|spams user in current channel and in private messages. Messages will be [length] insults long
|_voiceMove @user [amount]|moves user in voice chat around [amount] random channels
|_voiceBlocker @user [seconds]|moves user in voice chat into random channels excluding the current one for [seconds] seconds
|_voiceAnnoy @user [amount]|bot joins user and plays [amount] random annoying sound clips
|_voiceMute @user [seconds]|server mutes user in voice channel every second for [seconds] seconds
|_voiceDeafen @user [seconds]|server deafens user in voice channel every second for [seconds] seconds
|_setGlobalSpam [amount]|sets messages to be sent by spam to [amount]
|_help|displays all commands
|[*1] spam list|everytime a user on the spam list sends a message the bot will respond and spam insults and also insult the user in private messages. These insults will be [length] insults long
|[*2] blacklist|every message sent by this user will instantly be deleted
|[*3] sudoers list|only users on the sudoers list have permission to execute commands
|[*4] super users|super users are immune to all commands
|[*5] voice blacklist|as soon as the user joins a voice channel annoying sounds will be played and the user will be moved and muted constantly

## Installation and Setup

Clone this repository and open it:
```bash
git clone https://github.com/jaylann/discord-trollbot
cd discord-trollbot
```
Install all required modules.
```bash
pip install -r requirements.txt
```
Now you're ready to run the file but before you do that you first need to create your Discord bot.

To do that head over to the discord developer portal and open your applications. 
Or click **[here](https://discord.com/developers/applications)**.

Click on new application and enter a name.
You can also upload a picture and change the description if you want to.

Now go to the **OAuth2** panel.
From the **"Scopes"** menu select **"bot"**.
Then select all required permissions as shown below.

![Required Permissions](https://i.imgur.com/OwONKGD.png)

Or alternatively just select administrator if you are the owner.

Then copy the link that appears after selecting all permissions and paste it into your browser.
Select your Discord server and add the bot to the server.

Then go to the **"Bot"** section and copy the token.

![Copy Token](https://i.imgur.com/Zf474bJ.png)

In your cloned repository open the **```"Token.env"```** file and replace **```"YOUR_DISCORD_API_TOKEN"```** with your token.

Then open discord, go to your server and right click your name. Select **"Copy ID"**.
Paste this ID into the **```"Token.env"```** file under **```"YOUR_DISCORD_USER_ID"```**.

Open a command prompt in your cloned repository and run.

**Windows:**
```bash
python bot.py
```
**Linux/OS X:**
```bash
python3 bot.py
```
If everything worked you should see a message in the command prompt that your bot has connected to Discord. It might take a few seconds for it to show up though.
