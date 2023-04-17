import discord
import os, asyncio, datetime
import countdown_handler, food_handler
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot()

@bot.event
async def on_ready():
    async def schedule_daily_message():
        while True:
            now = datetime.datetime.now()
            midnight = (now + datetime.timedelta(days = 1)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
            wait_time = (midnight - now).total_seconds()
            if wait_time > 86400:
                wait_time -= 86400
            print('Next daily message:', wait_time, '(s)')
            await asyncio.sleep(wait_time)
            
            embed = discord.Embed(title = "Countdown", color = discord.Colour.from_rgb(225, 198, 153))
            embed.add_field(name = countdown_handler.get_today(), value = countdown_handler.get_countdown_list(), inline = False)
            embed.set_footer(text = "Created by userwei")
            
            channel1 = bot.get_channel(1097459343584141362)
            await channel1.send(embed = embed)
    
    print(f"{bot.user} is ready and online!")
    game = discord.Game('>_<')
    await bot.change_presence(status = discord.Status.idle, activity = game)
    await schedule_daily_message()
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)
    print(f"{username} said: '{user_message}' ({channel})")
    
@bot.slash_command(description = "Show some information about me")
async def about(ctx):
    embed = discord.Embed(color = discord.Colour.from_rgb(225, 198, 153))
    embed.set_author(name = "hsindopuff", icon_url = "https://imgur.com/bS6llF5.png")
    embed.add_field(name = "~\(≧▽≦)/~", value = "我們摯愛的hsindoditto，將於西元2023年4月18日，悄悄的離開Discord，我們痛徹心扉，就僅僅一眨眼的時間，天人永隔。", inline = False)
    embed.set_footer(text = "Created by userwei")
    await ctx.respond(embed = embed)

@bot.slash_command(description = "Show a list of commands")
async def help(ctx):
    embed = discord.Embed(color = discord.Colour.from_rgb(225, 198, 153))
    embed.add_field(name = "/about", value = "Show some information about me", inline = False)
    embed.add_field(name = "/countdown", value = "Get the countdown", inline = False)
    embed.add_field(name = "/countdown_list", value = "Get the countdown event date", inline = False)
    embed.add_field(name = "/food", value = "Pick a restaurant to eat", inline = False)
    embed.add_field(name = "/food_list", value = "Get the restaurant list", inline = False)
    embed.set_author(name = "hsindopuff", icon_url = "https://imgur.com/bS6llF5.png")
    embed.set_footer(text = "Created by userwei")
    await ctx.respond(embed = embed)

@bot.slash_command(description = "Get the countdown")
async def countdown(ctx):
    embed = discord.Embed(title = "Countdown", color = discord.Colour.from_rgb(225, 198, 153))
    embed.add_field(name = countdown_handler.get_today(), value = countdown_handler.get_countdown(), inline = False)
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)
    
@bot.slash_command(description = "Get the countdown event date")
async def countdown_list(ctx):
    embed = discord.Embed(title = "Countdown List", color = discord.Colour.from_rgb(225, 198, 153))
    embed.add_field(name = "Date                   Event", value = countdown_handler.get_countdown_list(), inline = False)
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)

@bot.slash_command(description = "Pick a restaurant to eat")
async def food(ctx):
    embed = discord.Embed(
        title = "Food",
        description = "hsindopuff 決定這餐要吃 `" + food_handler.get_food() + '`',
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)
    
@bot.slash_command(description = "Get the restaurant list")
async def food_list(ctx):
    embed = discord.Embed(
        title = "Food List",
        description = food_handler.get_food_list(),
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))