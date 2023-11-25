import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents) #<-- set your bot prefix

@bot.command()
async def setup_application(ctx):
    embed = discord.Embed(title="[YOUR SERVER NAME]", description="React to this message to apply for staff. 👨‍💼", color=discord.Color.blue()) #react msg setting here
    application_message = await ctx.send(embed=embed)
    await application_message.add_reaction("👨‍💼")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return

    if payload.emoji.name == "👨‍💼":
        user = await bot.fetch_user(payload.user_id)
        await user.send("Welcome to the application process!\nPlease answer the following questions:")

         #add your questions here basic questions are already given as example if you want you can add
        questions = ["Question 1: ``What's your name?``", "Question 2: ``Why do you want to join?``", "Question 3: ``For Which Position You want to apply for ?``", "Question 4: ``What Can You do for our Server ?``", "Question 4: ``How Much Time You Can Give to our server ?``", "Question 5: ``Can You Invite Your Friend in Our Server?``", "Question 6: ``How Will You Make The Server active when no one is chatting ?``", "Question 7: ``What will you do if a staff member of higher role is abusing his power ?``", "Question 8: ``What will you try to do if our server get nuked when the owners and founders are offline ?``"]
        answers = []

        for question in questions:
            await user.send(question)
            try:
                response = await bot.wait_for('message', check=lambda message: message.author == user, timeout=300)
                answers.append(response.content)
            except asyncio.TimeoutError:
                await user.send("You took too long to respond.")
                return
        
        application_channel = bot.get_channel(1144991157793869945) # <-- Replace with your designated msg channel ID if changed in future
        embed = discord.Embed(title="Staff Application", color=discord.Color.green()) #output msg heading
        for i, (question, answer) in enumerate(zip(questions, answers), start=1):
            embed.add_field(name=f"Question {i}:", value=f"{question}\n**Answer:** {answer}", inline=False)
        embed.set_footer(text=f"Application submitted by {user.name}")
        await application_channel.send(embed=embed)

        # Send a response to the user
        response_embed = discord.Embed(title="Application Submitted", description="Your responses have been submitted. Thank you for applying!", color=discord.Color.green()) #msg user will get in their dm
        await user.send(embed=response_embed)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run('YOUR TOKEN HERE')
