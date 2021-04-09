import asyncio
import glob
import json
import os
import random
from time import sleep

import discord
from dotenv import load_dotenv

AUDIO_FILES = []

if os.path.exists(r'audio'):

    for file in glob.glob(r'audio\\*.mp3'):
        AUDIO_FILES.append(file)

load_dotenv("Token.env")

TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_USER_ID = os.getenv('ADMIN_ID')
client = discord.Client()

INSULT_LIST = ["<@{0}> is a Motherfucker\n", "<@{0}> You Piece of Shit\n", "<@{0}> You Fucking Wanker\n",
               "<@{0}> is a Fucking Idiot\n", "<@{0}> You Fucking Cunt\n", "<@{0}> is a Bastard\n",
               "You Fuckface <@{0}>\n", "<@{0}> is a Scumbag\n", "<@{0}> You Fucking Bitch\n",
               "<@{0}> You son of a Bitch\n", "Piss off <@{0}>\n", "Go Fucking Kill Yourself <@{0}>\n",
               "<@{0}> You Twat\n", "I'm not Insulting <@{0}> im Describing him\n", "<@{0}> is Human Trash\n"]


async def print_help(message):
    await message.channel.send("```\n"
                               "_addTarget @user [length]      adds a target to the spam list[*1]\n"
                               "_delTarget @user [length]      removes a target from the spam list[*1]\n"
                               "_blacklist @user               adds user to the blacklist[*2]\n"
                               "_unblacklist @user             removes user from the blacklist[*2]\n"
                               "_addSudoer @user               adds user to the sudoers list[*3]\n"
                               "_delSudoer @user               removes user from the sudoers list[*3]\n"
                               "_addSuperUser @user            makes user a super user[*4]\n"
                               "_delSuperUser @user            removes user from super users[*4]\n"
                               "_voiceBlacklist @user          adds user to the voice blacklist[*5]\n"
                               "_delVoiceBlacklist @user       removes user from the voice blacklist [*5]\n"
                               "_spam @user [length]           spams user in current channel and in private\n"
                               "                               messages. Messages will be [length] insults long"
                               "```")

    await message.channel.send("```"
                               "_voiceMove @user [amount]      moves user in voice chat around [amount] random\n"
                               "                               channels\n"
                               "_voiceBlocker @user [seconds]  moves user in voice chat into random channels\n"
                               "                               excluding the current one for [seconds] seconds\n"
                               "_voiceAnnoy @user [amount]     bot joins user and plays [amount] random annoying\n"
                               "                               sound clips\n"
                               "_voiceMute @user [seconds]     server mutes user in voice channel every second for\n"
                               "                               [seconds] seconds\n"
                               "_voiceDeafen @user [seconds]   server deafens user in voice channel every second for\n"
                               "                               [seconds] seconds\n"
                               "_setGlobalSpam [amount]        sets messages to be sent by spam to [amount]\n"
                               "_help                          displays this message"
                               "```")

    await message.channel.send("```"
                               "[*1] spam list                 everytime a user on the spam list sends a message\n"
                               "                               the bot will respond and spam insults and also\n"
                               "                               insult the user in private messages.\n"
                               "                               These insults will be [length] insults long\n"
                               "                               the bot will respond and spam insults and also\n"
                               "                               insult the user in private messages\n"
                               "[*2] blacklist                 every message sent by this user will instantly be\n"
                               "                               deleted\n"
                               "[*3] sudoers list              only users on the sudoers list have permission to\n"
                               "                               execute commands\n"
                               "[*4] super users               super users are immune to all commands\n"
                               "[*5] voice blacklist           as soon as the user joins a voice channel annoying\n"
                               "                               sounds will be played and the user will be moved\n"
                               "                               and muted constantly"
                               "```")


def generate_insults(length, user_id):
    word_len = 0
    insult_string = ""
    insult_len = len(INSULT_LIST) - 1

    insult_string += ((INSULT_LIST[random.randint(0, insult_len)]).format(user_id))
    word_len += 1

    if len(insult_string) < 2000 and word_len < length:
        generating_insults = True

    else:
        return insult_string

    while generating_insults:

        random_insult = random.randint(0, insult_len)

        if len(insult_string) + len((INSULT_LIST[random_insult]).format(user_id)) < 2000 and word_len < length:

            insult_string += ((INSULT_LIST[random_insult]).format(user_id))
            word_len += 1

        else:
            insult_string = "".join(insult_string)
            return insult_string


async def spam_messages(channel, global_spam, msg_amount, target):
    for _ in range(global_spam):

        send_msg = generate_insults(msg_amount, target.id)

        await channel.send(send_msg)

        if not target.bot:

            await target.send(send_msg)


async def check_args(message, amount):
    try:

        cmd_args = []

        for x in range(1, amount + 1):
            cmd_arg = message.content.split()[x]
            cmd_args.append(cmd_arg)

        return cmd_args

    except IndexError:
        print("Please Parse Required Arguments")
        await print_help(message)


def add_to_json(data, key, value_key, value):
    if not data:
        data = {}

    try:

        if not data[key]:
            data[key] = []

    except KeyError:

        data[key] = []

    data[key].append({
        value_key: value,
    })

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)


def del_from_json(data, key, value_key, value):
    try:

        i = 0
        if key == "spamList":
            for s in data[key]:
                if s[value_key][0] == value:
                    data[key].pop(i)
                i += 1
        else:
            for s in data[key]:

                if s[value_key] == value:
                    data[key].pop(i)

                i += 1

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

    except KeyError:
        print("[-] GIVEN KEY NOT FOUND!")


def load_config(categories):
    out_list = []

    if os.path.exists("data.json"):
        with open('data.json') as json_file:
            data = json.load(json_file)

            for category in categories:
                cat_list = []

                try:
                    if data[category]:
                        for cat in data[category]:

                            if category == "spamList":
                                cat_list.append(cat[categories[category]])

                            else:

                                cat_list.append(cat[categories[category]])

                    else:
                        if category == "globalSpam":
                            cat_list.append(3)

                        else:
                            cat_list.append(None)

                except KeyError:
                    print(f"COULD NOT FIND CATEGORY: {category}")

                    if category == "sudoerList" or category == "superUsers":
                        cat_list.append(int(ADMIN_USER_ID))

                    elif category == "settings":
                        cat_list.append(3)

                out_list.append(cat_list)

    else:
        with open("data.json", "a+") as json_file:
            json_file.write('{}')

        with open("data.json") as json_file:
            data = json.load(json_file)

        out_list.append([3])

        del categories['settings']

        for _ in categories:
            out_list.append(None)

    out_list.append(data)

    return out_list


async def voice_fucker(user_id, amount):
    voice_channels = []

    for channel in client.guilds[0].voice_channels:
        voice_channels.append(channel)

    for x in range(amount):
        channel = voice_channels[random.randint(0, len(voice_channels)-1)]

        await user_id.move_to(channel)


async def voice_blocker(user_id, duration):
    voice_channels = []

    for channel in client.guilds[0].voice_channels:
        if not channel == user_id.voice.channel:
            voice_channels.append(channel)

    x = 0
    while x < duration:
        channel = voice_channels[random.randint(0, len(voice_channels) - 1)]

        await user_id.move_to(channel)

        sleep(1)
        x += 1


async def play_sound(user_id, amount):
    for _ in range(0, amount):

        vc = await user_id.voice.channel.connect()

        random_sound = AUDIO_FILES[random.randint(0, len(AUDIO_FILES) - 1)]

        vc.play(discord.FFmpegPCMAudio(random_sound), after=lambda e: print('done', e))

        while vc.is_playing():
            await asyncio.sleep(1)

        vc.stop()

        await vc.disconnect()
        await asyncio.sleep(random.randint(0, 5))


async def edit_voice(user_id, action, duration):
    for _ in range(0, duration):
        if action == "deafen":
            await user_id.edit(deafen=True)

        elif action == "mute":
            await user_id.edit(mute=True)

        await asyncio.sleep(1)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_voice_state_update(member, _before, _after):
    voice_blacklist = []

    tmp_voice_blacklist = load_config({'voiceBlacklist': "userID"})

    for x in tmp_voice_blacklist:
        try:
            if x:
                voice_blacklist.append(x[0])
        except KeyError:
            pass

    if member.id in voice_blacklist:
        while True:
            try:
                await edit_voice(member, "mute", 1)
                await voice_fucker(member, 1)

                try:
                    await play_sound(member, 1)

                except discord.errors.ClientException:
                    pass

            except discord.errors.HTTPException:
                break


@client.event
async def on_message(message):
    categories = {'settings': 'globalSpam', 'spamList': 'userID', 'sudoerList': 'userID', 'superUsers': 'userID',
                  'blackList': 'userID', 'voiceBlacklist': 'userID'}
    spam_list = {}
    global_spam, tmp_spam_list, sudo_users, super_users, blacklist, voice_blacklist, data = load_config(categories)

    global_spam = global_spam[0]
    print(tmp_spam_list)

    if tmp_spam_list:
        if tmp_spam_list[0]:
            for x in tmp_spam_list:
                spam_list[x[0]] = x[1]

    if message.author == client.user:
        return

    if message.content.startswith('_'):
        if message.author.id in sudo_users or message.author.id == int(ADMIN_USER_ID):
            cmd = message.content.split()[0].replace("_", "")

            if cmd == "help":
                await print_help(message)

            if cmd == "voiceAnnoy":

                if message.mentions[0].id not in super_users or message.author.id == int(ADMIN_USER_ID):
                    cmd_args = await check_args(message, 2)
                    await play_sound(message.mentions[0], int(cmd_args[1]))

            elif cmd == "voiceBlacklist":
                if message.mentions[0].id not in super_users or message.author.id == int(ADMIN_USER_ID):
                    if not await check_args(message, 1):
                        return

                    add_to_json(data, "voiceBlacklist", 'userID', message.mentions[0].id)

                    await message.channel.send(str(message.mentions[0]) + "has been added to the Voice Blacklist "
                                                                          ":DDDDD")

            elif cmd == "delVoiceBlacklist":
                if message.mentions[0].id not in super_users or message.author.id == int(ADMIN_USER_ID):
                    if not await check_args(message, 1):
                        return

                    del_from_json(data, 'voiceBlacklist', 'userID', message.mentions[0].id)

                    await message.channel.send(str(message.mentions[0]) + " has been removed from the Voice Blacklist")

            elif cmd == "voiceMove":
                if message.mentions[0].id not in super_users or message.author.id == int(ADMIN_USER_ID):
                    cmd_args = await check_args(message, 2)

                    if not cmd_args:
                        return

                    if message.mentions[0] not in super_users:
                        await voice_fucker(message.mentions[0], int(cmd_args[1]))

            elif cmd == "voiceBlock":
                if message.mentions[0].id not in super_users or message.author.id == int(ADMIN_USER_ID):
                    cmd_args = await check_args(message, 2)

                    if not cmd_args:
                        return

                    if message.mentions[0] not in super_users:
                        await voice_blocker(message.mentions[0], int(cmd_args[1]))

            elif cmd == "addSudoer":

                if not await check_args(message, 1):
                    return

                add_to_json(data, 'sudoerList', 'userID', message.mentions[0].id)

                await message.channel.send(str(message.mentions[0]) + " has been added to the Sudoers list")

            elif cmd == "delSudoer":

                if not await check_args(message, 1):
                    return

                del_from_json(data, 'sudoerList', 'userID', message.mentions[0].id)

                await message.channel.send(str(message.mentions[0]) + " has been removed from the Sudoers list")

            elif cmd == "addTarget":
                if message.mentions[0].id not in super_users or message.author.id == int(ADMIN_USER_ID):
                    args = await check_args(message, 2)

                    if not args:
                        return

                    if message.mentions[0].id in spam_list:
                        return

                    add_to_json(data, 'spamList', 'userID', (message.mentions[0].id, int(args[1])))

                    await message.channel.send(str(message.mentions[0]) + " is now a Target :D")

            elif cmd == "delTarget":

                if not await check_args(message, 1):
                    return

                del_from_json(data, 'spamList', 'userID', message.mentions[0].id)

                await message.channel.send(str(message.mentions[0]) + " is no longer a Target D:")

            elif cmd == "setGlobalSpam":

                data['settings'] = []
                global_spam = await check_args(message, 1)

                add_to_json(data, 'settings', 'globalSpam', int(global_spam[0]))

                await message.channel.send("GlobalSpam Value has been Changed to: " + global_spam[0])

            elif cmd == "spam":
                if message.mentions[0].id not in super_users or message.author.id == int(ADMIN_USER_ID):

                    spam_amount = await check_args(message, 2)
                    if not spam_amount[1]:
                        return

                    await spam_messages(message.channel, global_spam, int(spam_amount[1]), message.mentions[0])

            elif cmd == "addSuperUser":

                if message.author.id in sudo_users or message.author.id == int(ADMIN_USER_ID):
                    if not await check_args(message, 1):
                        return

                    add_to_json(data, 'superUsers', 'userID', message.mentions[0].id)

                    await message.channel.send(str(message.mentions[0]) + " is now a SUPER USER")

            elif cmd == "delSuperUser":

                if message.author.id in sudo_users or message.author.id == int(ADMIN_USER_ID):

                    if not await check_args(message, 1):
                        return

                    del_from_json(data, 'superUsers', 'userID', message.mentions[0].id)

                    await message.channel.send(str(message.mentions[0]) + " is not so super anymore")

            elif cmd == "blacklist":
                if message.mentions[0].id not in super_users or message.author.id == int(ADMIN_USER_ID):
                    if not await check_args(message, 1):
                        return

                    add_to_json(data, 'blackList', 'userID', message.mentions[0].id)

                    await message.channel.send(str(message.mentions[0]) + " is now on the BLACKLIST uh-oh")

            elif cmd == "unblacklist":

                if not await check_args(message, 1):
                    return

                del_from_json(data, 'blackList', 'userID', message.mentions[0].id)

                await message.channel.send(str(message.mentions[0]) + " is sadly no longer on the Blacklist D:")

            elif cmd == "voiceMute":
                if message.mentions[0].id not in super_users or message.author.id == int(ADMIN_USER_ID):
                    duration = await check_args(message, 2)

                    await edit_voice(message.mentions[0], "mute", int(duration[1]))

            elif cmd == "voiceDeafen":
                if message.mentions[0].id not in super_users or message.author.id == int(ADMIN_USER_ID):
                    duration = await check_args(message, 2)

                    await edit_voice(message.mentions[0], "deafen", int(duration[1]))

        else:

            await message.channel.send("YOU DO NOT HAVE PERMISSION TO EXECUTE THAT COMMAND")

            if message.author.id not in super_users:
                await spam_messages(message.channel, global_spam, 3, message.author)

    elif message.author.id in spam_list and message.author.id not in super_users and message.author.id in blacklist:
        await message.delete()
        await spam_messages(message.channel, global_spam, spam_list[message.author.id], message.author)

    elif message.author.id in blacklist and message.author.id not in super_users:
        await message.delete()

    elif message.author.id in spam_list and message.author.id not in super_users:
        await spam_messages(message.channel, global_spam, spam_list[message.author.id], message.author)


client.run(TOKEN)
