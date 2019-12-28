import discord
from credentials import login
from directory import get_church_member_info


EMBED = discord.Embed(title="*Twin Creeks Church Directory*")
TOKEN = login['token']
client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!dir'):
        message_contents = message.content.split(" ")
        names = [word for word in message_contents
                 if word != '!dir' and not word.startswith('-')]
        if len(names) > 2 or len(names) is 0:
            embed = make_embedded_error_desc(len(names))
            await message.channel.send(embed=embed)
            return
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else None
        info = get_church_member_info(first_name, last_name)
        if not type(info) is dict:
            embed = make_embedded_clarification(info)
            await message.channel.send(embed=embed)
            return
        commands = [x for x in message_contents if x.startswith('-')]
        if not commands:
            embed = make_embedded_directory(info)
            await message.channel.send(embed=embed)
        else:
            embed = make_specific_embed(info, first_name, commands)
            await message.channel.send(embed=embed)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def make_embedded_directory(info):
    embed = discord.Embed(title="*Twin Creeks Church Directory*")
    populate = True
    for member in info:
        embed.set_image(url=info[member]["image"])
        (embed.add_field(name="Member",
         value=("```" + info[member]["name"] + "```"), inline=False))
        (embed.add_field(name="Address",
         value=info[member]["address"], inline=False) if populate else None)
        (embed.add_field(name="Home Phone",
         value=info[member]["home_phone"], inline=True)
            if info[member]["home_phone"] else None)
        (embed.add_field(name="Cell Phone",
         value=info[member]["cell_phone"], inline=True))
        (embed.add_field(name="Email",
         value=info[member]["email"], inline=False))
        (embed.add_field(name="Birthday",
         value=info[member]["birthday"], inline=True))
        (embed.add_field(name="Anniversary",
         value=info[member]["anniversary"], inline=True) if populate else None)
        populate = False
    return embed


def make_specific_embed(info, name, commands):
    embed = discord.Embed(title="*Twin Creeks Church Directory*")
    members = [key for key in info.keys() if name in key.lower()]
    for member in members:
        embed.add_field(name="Member", value=(
            "```{}```".format(info[member]["name"])), inline=False)
        for command in commands:
            if command == "-a":
                embed.add_field(name="Address",
                                value=info[member]["address"], inline=False)
            elif command == "-cp":
                embed.add_field(name="Cell Phone",
                                value=info[member]["cell_phone"], inline=True)
            elif command == "-e":
                embed.add_field(name="Email",
                                value=info[member]["email"], inline=False)
            elif command == "-h":
                embed.add_field(name="Options", value=(
                    "```-a      Return the address```" +
                    "```-cp     Return the cell phone number```" +
                    "```-e      Return the email address```" +
                    "```-h      Return the list of available options```" +
                    "```-hp     Return the home phone number```"),
                    inline=False)
            elif command == "-hp":
                embed.add_field(name="Home Phone",
                                value=info[member]["home_phone"], inline=True)
            else:
                embed.add_field(name="Command Flag Not Found", value=(
                    "```{0}: command not found```".format(command)),
                    inline=False)
                embed.add_field(name="Options", value=(
                    "```-a      Return the address```" +
                    "```-cp     Return the cell phone number```" +
                    "```-e      Return the email address```" +
                    "```-h      Return the list of available options```" +
                    "```-hp     Return the home phone number```"),
                    inline=False)
    return embed


def make_embedded_address(info, name):
    members = [key for key in info.keys() if name in key]
    for member in members:
        EMBED.add_field(name="Address",
                        value=info[member]["address"], inline=False)


def make_embedded_email(info, name):
    members = [key for key in info.keys() if name in key]
    for member in members:
        EMBED.add_field(name="Email",
                        value=info[member]["email"], inline=False)


def make_embedded_phone_numbers(info, name):
    members = [key for key in info.keys() if name in key]
    for member in members:
        EMBED.add_field(name="Home Phone",
                        value=info[member]["home_phone"], inline=True)
        EMBED.add_field(name="Cell Phone",
                        value=info[member]["cell_phone"], inline=True)


def make_embedded_clarification(info):
    # TODO: Add Spicy memes for Member Not Found images
    embed = discord.Embed(title="*Member Clarification*")
    if not info:
        embed.add_field(name="Member Not Found", value=(
            "The member you entered was not found in the directory."))
        return embed
    for name in info:
        embed.add_field(name=name, value=(
            "To get the directory information for this member try\n" +
            "```!dir {}```".format(str(name))))
    return embed


def make_embedded_error_desc(names):
    embed = discord.Embed(title="*Input Error*")
    if (names < 2):
        (embed.add_field(name="Name Needed",
         value=("What am I supposed to do? You didn't provide a name.")))
        (embed.add_field(name="Try",
         value=("```!dir first_name last_name``` or ```!dir first_name```")))
    elif (names > 3):
        (embed.add_field(name="First and Last Name Only",
         value=("I can only search using the first name and last name")))
        (embed.add_field(name="Try",
         value=("```!dir first_name last_name``` or ```!dir first_name```")))
    return embed


client.run(TOKEN)
