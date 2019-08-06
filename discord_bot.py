import discord
from credentials import login
from directory import get_church_member_info


TOKEN = login['token']
client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!dir'):
        message_contents = message.content.split(" ")
        first_name = str(message_contents[1]).capitalize()
        last_name = (str(message_contents[2]).capitalize
                     if len(message_contents) > 2 else None)
        info = get_church_member_info(first_name, last_name)
        embed = (make_embedded_directory(info)
                 if type(info) is dict else make_embedded_clarification(info))
        await message.channel.send(embed=embed)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def make_embedded_directory(info):
    embed = discord.Embed(title="*West Allen Church Directory*")
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


def make_embedded_clarification(info):
    # TODO: Add Spicy memes for Member Not Found images
    embed = discord.Embed(title="*Member Clarification*")
    if not info:
        (embed.add_field(name="Member Not Found",
         value=("The member you entered was not found in the directory.")))
        return embed
    for name in info:
        (embed.add_field(name=name,
         value=("To get the directory information for this member try\n```" +
                "!dir " + str(name) + "```")))
    return embed

print("THIS IS THE TOKEN: " + TOKEN)
client.run(TOKEN)
