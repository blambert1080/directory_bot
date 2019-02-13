import discord
from credentials import login 
from directory import get_church_member_phone

TOKEN = login['token']

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        print(message.content)
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!dir'):
        message_contents = message.content.split(" ")
        first_name = message_contents[1]
        last_name = message_contents[2] if len(message_contents) > 2 else None
        phone_dict = get_church_member_phone(first_name, last_name)
        cell_phone = phone_dict['Cell']
        home_phone = phone_dict['Home']
        msg = "{0} {1}".format(first_name, last_name) if last_name else "{}".format(first_name)
        msg += "\nCell: {}".format(cell_phone) if cell_phone else "" 
        msg += "\nHome: {}".format(home_phone) if home_phone else ""
        msg.format(message)
        await client.send_message(message.channel, msg) 


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)