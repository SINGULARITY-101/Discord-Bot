import discord
from discord.ext import commands
import random
import os

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns 

import numpy as np
import math

sns.set_style("darkgrid")
plt.rcParams["figure.dpi"]=360


client = commands.Bot(command_prefix="#")

#A list of reactions that will be added to the poll according to the number of options. The bot supports a total of 10 options in its poll.
reactions=["1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]


#A global variable. Used to store the message ID that we get from the "lastmessage" command.
num=0

#A global list. Used to store the number of votes for each option in the poll.
count=[0,0,0,0,0,0,0,0,0,0]

#A global list. Used to store the options for which the voting is taking place,
categories=[]






#EVENTS

@client.event 

async def on_ready():
    print("Bot is ready")


@client.event

async def on_member_join(member):
    print(f"{member} has joined the server.")


@client.event

async def on_member_remove(member):
    print(f"{member} has left the server.")





#Events for counting the number of reactions. Different events for the addition and removal of the reaction. 

@client.event

async def on_raw_reaction_add(payload):
    global count
    if payload.message_id == num:
        if payload.member != "asmr.new.py":

            if str(payload.emoji)=="1️⃣":
                count[0]=count[0]+1
            
            elif str(payload.emoji)=="2⃣":
                count[1]=count[1]+1
            
            elif str(payload.emoji)=="3⃣":
                count[2]=count[2]+1
            
            elif str(payload.emoji)=="4⃣":
                count[3]=count[3]+1

            elif str(payload.emoji)=="5⃣":
                count[4]=count[4]+1

            elif str(payload.emoji)=="6⃣":
                count[5]=count[5]+1

            elif str(payload.emoji)=="7⃣":
                count[6]=count[6]+1

            elif str(payload.emoji)=="8⃣":
                count[7]=count[7]+1

            elif str(payload.emoji)=="9⃣":
                count[8]=count[8]+1

            elif str(payload.emoji)=="🔟":
                count[9]=count[9]+1
            

            
            channel_id = payload.channel_id
            channel = client.get_channel(channel_id)
            await channel.send(f"Reaction Added: {payload.emoji}\nBy: `{payload.member}`\n")

            await channel.send(f"Count of Reactions:`{count}`")



@client.event

async def on_raw_reaction_remove(payload):
    global count
    if payload.message_id == num:
        if payload.user_id == 765651879858143282:
            pass

        else:

            if str(payload.emoji)=="1️⃣":
                count[0]=count[0]-1
            
            elif str(payload.emoji)=="2⃣":
                count[1]=count[1]-1
            
            elif str(payload.emoji)=="3⃣":
                count[2]=count[2]-1
            
            elif str(payload.emoji)=="4⃣":
                count[3]=count[3]-1

            elif str(payload.emoji)=="5⃣":
                count[4]=count[4]-1

            elif str(payload.emoji)=="6⃣":
                count[5]=count[5]-1

            elif str(payload.emoji)=="7⃣":
                count[6]=count[6]-1

            elif str(payload.emoji)=="8⃣":
                count[7]=count[7]-1

            elif str(payload.emoji)=="9⃣":
                count[8]=count[8]-1

            elif str(payload.emoji)=="🔟":
                count[9]=count[9]-1


            channel_id = payload.channel_id
            channel = client.get_channel(channel_id)
            await channel.send(f"Reaction Removed: {payload.emoji}\nBy: `{payload.member}`\n")

            await channel.send(f"Count of Reactions:`{count}`")
















#COMMANDS
#Name your function what you want your command to be.
#Context containes information like what channel is used etc. Basically it contains a lot of meta-data.

@client.command()

async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)} ms")


#Used to clear the messages in the channel 

@client.command()

async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)








#Used to plot the graph for the pole 


@client.command()

async def endpoll(ctx):
    global count
    global categories
    global num
    votes=[]

    for i in range(0,len(categories)):
        votes.append(count[i])

    print(votes)

    plt.bar(categories, votes, color=(0.5,0.1,0.5,0.6))
    plt.xlabel("Options", fontsize=20, labelpad=5)
    plt.ylabel("Votes", fontsize=20, labelpad=5)
    plt.title("Bar Graph", fontsize=30, pad=10, weight="bold")

    plt.yticks(np.arange(0, math.ceil(max(votes))+1, 1))
    plt.savefig("Data1.jpg")
    plt.close()


    await ctx.send(file=discord.File("Data1.jpg"))

    count=[0,0,0,0,0,0,0,0,0,0]
    categories.clear()
    num=0

    os.remove("Data1.jpg")
    
    await ctx.send("**\nPolling has now been closed!!\nReactions WILL NOT be recorded**")









#Used to make the embed for the poll.
#Issues:- Can't add a string as an option which has a space in between. So might have to use underscores as seprators.

@client.command()

async def makepoll(ctx, question, option, *, options):
    if int(option)>10:
        await ctx.channel.send("**You can only supply a maximum of 10 options to the poll**")
    
    else:
        global categories
        emb = discord.Embed(title="POLL", description=question,  color=0x00ff00)

        list1=options.split(" ")

        if len(list1) < int(option):
            await ctx.channel.send("**Can't make the poll. Required number of categories have not been entered.**")
        
        elif len(list1) > int(option):
            await ctx.channel.send("**Can't make the poll. More than required number of categories have been entered.**")

        else:
            for item in list1:
                categories.append(item)

            for item in range(0, len(list1)):
                emb.add_field(name=f"Option {item+1}", value=list1[item], inline=False)

            msg = await ctx.channel.send(embed=emb)

            for item in range(0,int(option)):
                await msg.add_reaction(reactions[item])

            print(categories)



    



#Finds the last message sent by asmr.new.py. This is to be called after creating the embed for the poll so as to update the message ID
#to be of the embed that was just made for the poll. This way we can start counting reactions on the poll. 

@client.command()

async def startpoll(ctx, users_id=765651879858143282):
    global num
    oldestMessage = None
    for channel in ctx.guild.text_channels:
        fetchMessage = await channel.history().find(lambda m: m.author.id == users_id)
        if fetchMessage is None:
            continue


        if oldestMessage is None:
            oldestMessage = fetchMessage
        else:
            if fetchMessage.created_at > oldestMessage.created_at:
                oldestMessage = fetchMessage

    if (oldestMessage is not None):
        await ctx.send(f"**Message ID of the poll found!!\nReactions on the poll will now be recorded!!**")
        num=oldestMessage.id 
    else:
        await ctx.send("No message found.")




#Enter the bot token to run it
client.run("")