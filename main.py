import discord
import asyncio
from discord.ext import commands,tasks
import random
from easy_pil import Editor, load_image_async, Font

bot = commands.Bot(command_prefix=[".","-"],intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Logged in as " + str(bot.user))
    clearCmds.start()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("***You don't have the required permission to use this command*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return

    if isinstance(error, commands.MemberNotFound):
        await ctx.reply("***Member not found, Please mention a valid user*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return

    if isinstance(error, commands.BotMissingPermissions):
        await ctx.reply("***I don't have the permission to do that*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return

    if isinstance(error, discord.Forbidden):
        await ctx.reply("***I don't have the permission to do that*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return
    
    if isinstance(error, commands.ChannelNotFound):
        await ctx.reply("***Channel not found, Please mention a valid text channel*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return
    
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.NoPrivateMessage):
        await ctx.reply("***This command does not work in direct messages*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return
    
    if isinstance(error,commands.CommandOnCooldown):
        await ctx.reply("***Still on cooldown, please try again in {:.0f} seconds*** :alarm_clock:".format(error.retry_after), mention_author=False)
        await ctx.message.add_reaction("⏰")
        return
        
    raise error


@bot.event
async def on_member_join(member: discord.Member):
    await asyncio.sleep(1)
    background_image = await load_image_async("https://i.imgur.com/V8EENEK.jpg")
    if member.avatar:
        image = member.avatar.url
    else:
        num = random.randint(0,5)
        image = f'https://cdn.discordapp.com/embed/avatars/{num}.png'
    profile_image = await load_image_async(image)
    background = Editor(background_image)
    profile = Editor(profile_image).resize((150,150)).circle_image()
    poopins = Font.poppins(size=50,variant="bold")
    poopins_small = Font.poppins(size=20, variant="regular")
    background.paste(profile,(325,90))
    background.ellipse((325,90), 150,150, outline="white",stroke_width=5)
    background.text((400,260),f'WELCOME TO {member.guild.name}',color="white",font=poopins, align="center")
    background.text((400,325),f'{member.name}#{member.discriminator}',color="white",font=poopins_small, align="center")
    file = discord.File(fp=background.image_bytes,filename=f'{member.name}{member.discriminator}.jpg')

    channel = bot.get_channel(1047990016829296721)
    await channel.send(file=file)
    await channel.send(f'Hello {member.mention}! Welcome To **{member.guild.name}**')


@bot.command(name="ping", description="test the latency between the bot and Discord")
async def ping(ctx):
    await ctx.send(f'***Pong!*** `{round (bot.latency * 1000)}ms` :ping_pong:')

@bot.command(name="kick", aliases=["طرد","كيك"], description="kick a member from the server")
@commands.has_any_role()
async def kick(ctx, member: discord.Member = None, *, reason = ""):
    if member == None or isinstance(member,discord.Member) == False:
        await ctx.reply("***Mention a member to kick*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return
            
    if member.top_role >= ctx.author.top_role and member.guild.owner_id != ctx.author.id:
        await ctx.reply("***You can't kick this member*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return

    await member.kick(reason=reason + f" by {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.reply(f"{member.name}#{member.discriminator} ***has been kicked*** :airplane:", mention_author=False)
    await ctx.message.add_reaction("✅")


@bot.command(name="ban", aliases=["حظر","بان"], description="ban a member from the server")
@commands.has_permissions(ban_members=True)  
async def ban(ctx, member: discord.Member = None, *, reason = ""):
    if member == None or isinstance(member,discord.Member) == False:
        await ctx.reply("***Mention a member to ban*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return

    if member.top_role >= ctx.author.top_role and member.guild.owner_id != ctx.author.id:
        await ctx.reply("***You can't ban this member*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return

    await member.ban(reason=reason + f" by {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.reply(f"{member.name}#{member.discriminator} ***has been banned*** :airplane:", mention_author=False)
    await ctx.message.add_reaction("✅")


@bot.command(name="unban", aliases=["رفع حطر"], description="unban a user from the server")
@commands.has_permissions(ban_members=True)
async def unban(ctx, id = None, *, reason = ""):
    if id == None:
        await ctx.reply("***Specify the user id to unban*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return

    try:
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user,reason=reason + f" by {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.reply(f"{user.name}#{user.discriminator} ***has been unbanned*** :airplane_arriving:", mention_author=False)
        await ctx.message.add_reaction("✅")
    except discord.NotFound:
        await ctx.reply("***Couldn't find this user id in the ban list*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")


@bot.command(name="purge", aliases=["clear","مسح"], description="delete a specified amount of messages")
@commands.has_permissions(manage_channels=True)
async def purge(ctx, limit : int = None, *, reason = ""):
   if limit == None or limit > 500:
        await ctx.reply("***Specify the amount of messages you want to delete (max is 500)*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return
   else:
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit, reason=reason + f" by {ctx.author.name}#{ctx.author.discriminator}")
        message = await ctx.send(f'***Deleted {limit} messages :wastebasket:. Requested by {ctx.author.mention} :white_check_mark:***')
        await asyncio.sleep(1)
        await message.delete()


@bot.command(name="lock", aliases=["close","قفل"], description="lock a channel")
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None, *, reason = ""):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=reason + f" channel locked by {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.reply(f'{channel.mention} ***has been locked*** 🔒', mention_author=False)
    await ctx.message.add_reaction("✅")


@bot.command(name="unlock", aliases=["open","فتح"], description="unlock a channel")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None, *, reason = ""):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=reason + f" channel unlocked by {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.reply(f'{channel.mention} ***has been unlocked*** 🔓', mention_author=False)
    await ctx.message.add_reaction("✅")


@bot.command(name="mute", aliases=["كتم"], description="mute a member")
@commands.has_guild_permissions(mute_members=True)
async def mute(ctx,member: discord.Member = None, args = None, *, reason = ""):
    if member == None or isinstance(member,discord.Member) == False:
        await ctx.reply("***Mention a member to mute*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return
    
    if member.top_role >= ctx.author.top_role or member.guild_permissions.administrator:
        await ctx.reply("***You can't mute this member*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return

    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if role not in member.roles:
        total_seconds = 0
        if args:
            days = 0
            hours = 0
            minutes = 0
            tmp = 0
            seconds = 0
            total_seconds = 0
            args = args.lower()
            for arg in args:
                if arg == 'd':
                    days += tmp
                    tmp = 0
                elif arg == 'h':
                    hours += tmp
                    tmp = 0 
                elif arg == 'm':
                    minutes += tmp
                    tmp = 0
                elif arg == 's':
                    seconds += tmp
                    tmp = 0
                elif arg.isdigit():
                    tmp = tmp * 10
                    tmp += int(arg)
            total_seconds = (days * 3600 * 24) + (hours * 3600) + (minutes * 60) + seconds
            if total_seconds <= 0:
                reason = args + reason
        await member.add_roles(role, reason=reason + f" muted by {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.reply(f'{member.name}#{member.discriminator} ***has been muted*** :zipper_mouth:', mention_author=False)
        await ctx.message.add_reaction("✅")
        if total_seconds > 0:
            await asyncio.sleep(total_seconds)
            await member.remove_roles(role)
    else:
        await ctx.reply(f'{member.name}#{member.discriminator} ***is already muted*** :interrobang:', mention_author=False)
        await ctx.message.add_reaction("⁉️")


@bot.command(name="unmute", aliases=["تكلم"], description="unmute a member")
@commands.has_guild_permissions(mute_members=True)
async def unmute(ctx, member: discord.Member = None, *, reason = ""):
    if member == None or isinstance(member,discord.Member) == False:
        await ctx.reply("***Mention a member to unmute*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return
    
    role = discord.utils.get(ctx.guild.roles,name="Muted")
    
    if role in member.roles:
        await  member.remove_roles(role, reason=reason + f" unmuted by {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.reply(f'{member.name}#{member.discriminator} ***has been unmuted*** :white_check_mark:', mention_author=False)
        await ctx.message.add_reaction("✅")
    else:
        await ctx.reply(f'{member.name}#{member.discriminator} ***is not muted in the first place*** :interrobang:', mention_author=False)
        await ctx.message.add_reaction("⁉️")


@bot.command(name="role")
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member = None, *, name = None):
    if member == None or isinstance(member,discord.Member) == False:
        await ctx.reply("***Mention a member to give a specifed role*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return

    if name == None:
        await ctx.reply("***Specify an role name*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return

    role = discord.utils.get(ctx.guild.roles,name=name)
    if role:
        if role >= ctx.author.top_role and member.guild.owner_id != ctx.author.id:
            await ctx.reply("***You can't manage this role*** :x:", mention_author=False)
            await ctx.message.add_reaction("❌")
        else:
            await member.add_roles(role, reason=f"by {ctx.author.name}#{ctx.author.discriminator}")
            await ctx.message.add_reaction("✅")
    else:
        await ctx.reply("***Couldn't find this specified role name*** :question:", mention_author=False)
        await ctx.message.add_reaction("❌")


@bot.command(name="unrole")
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member = None, *, name = None):
    if member == None or isinstance(member,discord.Member) == False:
        await ctx.reply("***Mention a member to remove from them a specifed role*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return

    if name == None:
        await ctx.reply("***Specify an role name*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return

    role = discord.utils.get(ctx.guild.roles,name=name)
    if role:
        if role >= ctx.author.top_role and member.guild.owner_id != ctx.author.id:
            await ctx.reply("***You can't manage this role*** :x:", mention_author=False)
            await ctx.message.add_reaction("❌")
        else:
            await member.remove_roles(role, reason=f"by {ctx.author.name}#{ctx.author.discriminator}")
            await ctx.message.add_reaction("✅")
    else:
        await ctx.reply("***Couldn't find this specified role name*** :question:", mention_author=False)
        await ctx.message.add_reaction("❌")

@bot.command(name="move", description="move a member to your current voice channel")
@commands.has_guild_permissions(move_members=True)
async def move(ctx, member: discord.Member = None, reason = ""):
    if ctx.author.voice is None:
        await ctx.reply("***You need to be in a voice channel to use this command*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return

    if member == None or isinstance(member,discord.Member) == False:
        await ctx.reply("***Mention a member to move them to your voice channel*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return

    if member.voice is None:
        await ctx.reply("***This member has to be connected to any voice channel first*** :x:", mention_author=False)
        await ctx.message.add_reaction("❌")
        return

    await member.move_to(ctx.author.voice.channel, reason=reason + f" by {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.message.add_reaction("✅")

@bot.command(name="sahra", aliases=["سهره"])
@commands.has_guild_permissions(mute_members=True)
async def sahra(ctx, member: discord.Member = None):
    if member == None or isinstance(member,discord.Member) == False:
        await ctx.reply("***Mention a member*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return
    
    pic_role = ctx.guild.get_role(1047989966640263290) 
    emoji_role = ctx.guild.get_role(1047989965344211078)
    ni_role = ctx.guild.get_role(1047989967449759836) 

    await member.add_roles(pic_role,emoji_role,ni_role) 
    await ctx.message.add_reaction("✅")

@bot.command(name="type", aliases=["اكتب"])
@commands.has_permissions(manage_roles=True)
async def type(ctx, member: discord.Member = None):
    if member == None or isinstance(member,discord.Member) == False:
        await ctx.reply("***Mention a member*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return
    
    type_role = ctx.guild.get_role(1047989992800129056) 

    await member.add_roles(type_role) 
    await ctx.message.add_reaction("✅")


@bot.command(name="color", aliases=["لون"])
async def color(ctx, limit : int = None):
    if limit == None or limit > 20:
        await ctx.reply("***Pick a valid color number*** :question:", mention_author=False)
        await ctx.message.add_reaction("❓")
        return

    for role in ctx.message.author.roles:
        if role.name.isnumeric():
            await ctx.message.author.remove_roles(role)

    if limit != 0:
        color = discord.utils.get(ctx.guild.roles,name=str(limit))
        await ctx.message.author.add_roles(color)
        await ctx.message.add_reaction("✅")


@tasks.loop(minutes=10.0)
async def clearCmds():
    channel = bot.get_channel(1047990019098423336)
    await channel.purge(limit=None, check=lambda msg: not msg.pinned)


bot.run("MTA0NDAxNTM3MTM2NTEyNjIxNA.GCM4rz.Il6pbgo4RHO99mJyaZ1dIyKukTO79FSouLCBp8")