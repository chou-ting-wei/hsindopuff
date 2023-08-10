import discord
import asyncio, datetime, json
import countdown_handler, food_handler, permission_handler

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = discord.Bot()

@bot.event
async def on_ready():
    async def schedule_daily_message():
        with open('data.json', mode='r', encoding='utf8') as data:
            data = json.load(data)
            while True:
                now = datetime.datetime.now()
                midnight = (now + datetime.timedelta(days = 1)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
                wait_time = (midnight - now).total_seconds()
                # midnight = (now + datetime.timedelta(days = 1)).replace(hour=18, minute=0, second=0, microsecond=0)
                # wait_time = (midnight - now).total_seconds()
                if wait_time > 86400:
                    wait_time -= 86400
                print('Next daily message:', wait_time, '(s)')
                await asyncio.sleep(wait_time)
                for i in range(len(data['countdown_channel'])): 
                    embed = discord.Embed(title = "Countdown", color = discord.Colour.from_rgb(225, 198, 153))
                    embed.add_field(name = countdown_handler.get_today(), value = countdown_handler.get_countdown(data['countdown_channel'][i]), inline = False)
                    embed.set_footer(text = countdown_handler.get_now())
                    
                    channel = bot.get_channel(data['countdown_channel'][i])
                    await channel.send(embed = embed)
    
    print(f"{bot.user} is ready and online!")
    game = discord.Game('>_<')
    await bot.change_presence(status = discord.Status.idle, activity = game)
    await schedule_daily_message()
    
@bot.command(description = "Show some information about me.")
async def about(ctx):
    embed = discord.Embed(color = discord.Colour.from_rgb(225, 198, 153))
    embed.set_author(name = "hsindopuff", icon_url = "https://imgur.com/bS6llF5.png")
    embed.add_field(name = "~\(≧▽≦)/~", value = "我們摯愛的hsindoditto，於西元2023年4月18日，悄悄的離開Discord，我們痛徹心扉，就僅僅一眨眼的時間，天人永隔。", inline = False)
    embed.set_footer(text = "Created by userwei")
    await ctx.respond(embed = embed)

@bot.command(description = "Show a list of commands.")
async def help(ctx):
    embed = discord.Embed(color = discord.Colour.from_rgb(225, 198, 153))
    embed.add_field(name = "/about", value = "Show some information about me.", inline = False)
    embed.add_field(name = "/ping", value = "Sends the bot's latency.", inline = False)
    embed.add_field(name = "/spam", value = "Spam some messages.", inline = False)
    embed.add_field(name = "/countdown", value = "Get the countdown.", inline = False)
    embed.add_field(name = "/countdown_list", value = "Get the countdown event date.", inline = False)
    embed.add_field(name = "/food", value = "Pick a restaurant to eat.", inline = False)
    embed.add_field(name = "/food_list", value = "Get the restaurant list.", inline = False)
    embed.set_author(name = "hsindopuff", icon_url = "https://imgur.com/bS6llF5.png")
    embed.set_footer(text = "Created by userwei")
    await ctx.respond(embed = embed)
    
@bot.command(description = "Sends the bot's latency.")
async def ping(ctx):
    embed = discord.Embed(
        title = "Ping",
        description = f"Pong! Latency is `{round(bot.latency * 1000)}` ms",
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)

@bot.command(description = "Spam some messages.")
async def spam(ctx, times):
    embed = discord.Embed(
        title = "Spam",
        description = "There is nothing to spam now.",
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)
    # for i in range(int(times)):
    #     embed = discord.Embed(
    #         title = "Spam",
    #         description = "This is a spam message.",
    #         color = discord.Colour.from_rgb(225, 198, 153)
    #     )
    #     embed.set_footer(text = countdown_handler.get_now())
    #     await ctx.respond(embed = embed)    

@bot.command(description = "Get the countdown.")
async def countdown(ctx):
    chn =str(ctx.channel.id)
    embed = discord.Embed(title = "Countdown", color = discord.Colour.from_rgb(225, 198, 153))
    embed.add_field(name = countdown_handler.get_today(), value = countdown_handler.get_countdown(chn), inline = False)
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)
    
@bot.command(description = "Get the countdown event date.")
async def countdown_list(ctx):
    author = str(ctx.author.id)
    chn = str(ctx.channel.id)
    ret_title = "Countdown List"
    if permission_handler.find_permission(author):
        ret_title += " for Admin"
    embed = discord.Embed(title = ret_title, color = discord.Colour.from_rgb(225, 198, 153))
    embed.add_field(name = "Date                   Event", value = countdown_handler.get_countdown_list(permission_handler.find_permission(author), chn), inline = False)
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)

@bot.command(description = "Pick a restaurant to eat.")
async def food(ctx):
    embed = discord.Embed(
        title = "Food",
        description = "hsindopuff 決定這餐要吃 `" + food_handler.get_food() + '`',
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)
    
@bot.command(description = "Get the restaurant list.")
async def food_list(ctx):
    embed = discord.Embed(
        title = "Food List",
        description = food_handler.get_food_list(),
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)
    
admin = bot.create_group("admin", "Some cool commands")

@admin.command()
async def admin_add(ctx, id):
    author = str(ctx.author.id)
    embed = discord.Embed(
        title = "Add Admin",
        description = permission_handler.add_permission(permission_handler.find_permission(author), id),
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    if permission_handler.find_permission(id):
        embed.add_field(name = "Identity Document", value = id, inline = False)
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)
    
@admin.command()
async def admin_delete(ctx, id):
    author = str(ctx.author.id)
    embed = discord.Embed(
        title = "Delete Admin",
        description = permission_handler.delete_permission(permission_handler.find_permission(author), id),
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    if not permission_handler.find_permission(id):
        embed.add_field(name = "Identity Document", value = id, inline = False)
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)

@admin.command()
async def countdown_add(ctx, view, event, year, month, day, last, add):
    author = str(ctx.author.id)
    chn =str(ctx.channel.id)
    embed = discord.Embed(
        title = "Add Countdown",
        description = countdown_handler.add_countdown(permission_handler.find_permission(author), view, event, year, month, day, last, add, chn),
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    if countdown_handler.find_countdown(event, chn):
        if view == 'true':
            embed.add_field(name = "View", value = view, inline = False)
            embed.add_field(name = "Event", value = event, inline = False)
            start_date = datetime.date(int(year), int(month), int(day))
            end_date = start_date + datetime.timedelta(days = int(last) - 1)
            embed.add_field(name = "Date", value = start_date.strftime("%Y/%m/%d") + " ~ " + end_date.strftime("%Y/%m/%d"), inline = False)
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)
    
@admin.command()
async def countdown_delete(ctx, event):
    author = str(ctx.author.id)
    chn =str(ctx.channel.id)
    embed = discord.Embed(
        title = "Delete Countdown",
        description = countdown_handler.delete_countdown(permission_handler.find_permission(author), event, chn),
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    if not countdown_handler.find_countdown(event, chn):
        embed.add_field(name = "Event", value = event, inline = False)
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)
 
@admin.command()
async def food_add(ctx, restaurant):
    author = str(ctx.author.id)
    embed = discord.Embed(
        title = "Add Food",
        description = food_handler.add_food(permission_handler.find_permission(author), restaurant),
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    if food_handler.find_food(restaurant):
        embed.add_field(name = "Restaurant", value = restaurant, inline = False)
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)
   
@admin.command()
async def food_delete(ctx, restaurant):
    author = str(ctx.author.id)
    embed = discord.Embed(
        title = "Delete Food",
        description = food_handler.delete_food(permission_handler.find_permission(author), restaurant),
        color = discord.Colour.from_rgb(225, 198, 153)
    )
    if not food_handler.find_food(restaurant):
        embed.add_field(name = "Restaurant", value = restaurant, inline = False)
    embed.set_footer(text = countdown_handler.get_now())
    await ctx.respond(embed = embed)

if __name__ == "__main__":
    bot.run(jdata['TOKEN'])