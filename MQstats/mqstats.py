from redbot.core import commands
from decimal import *
import discord

class MQstats(commands.Cog):

    @commands.command()
    async def adcalc(self, ctx, might: str, health: str, defence: str, bubbleType='warlike'):
        """Returns multiple statistics for bubble damage, set health, and adrenaline optimisation"""

        bubbleType = str.lower(bubbleType)
        warlikeMulti = 1
        coeff = 1

        #String conversions with error checking
        might = int(str.replace(might, ",", ""))
        health = int(str.replace(health, ",", ""))
        defence = int(str.replace(defence, "%", ""))

        #Calculations
        defence = defence / 100
        if (bubbleType == 'weak'):
            coeff = 4.45
        elif (bubbleType == 'wise'):
            coeff = 3.66
        elif (bubbleType == 'wild'):
            coeff = 2.79
        elif (bubbleType == 'warlike'):
            coeff = 4.45
            warlikeMulti = 2
        else:
            pass

        if (coeff != 1):
            dmg = might / coeff
            dmgShielded = dmg * defence

            dmgActual = dmg - dmgShielded
            dmgActual = dmgActual * warlikeMulti

            healthremaining = health - dmgActual
            adreThreshold = health * 0.2

            adreProcReq = healthremaining - adreThreshold + 1

            #Health checking for string set
            if (healthremaining <= 0):
                adbool = "You're dead"
            elif (healthremaining < adreThreshold):
                adbool = "Yes"
            else:
                adbool = 'No'

            #Embed colour setting
            if (adbool == 'Yes'):
                embedColour = discord.Colour.green()
            elif (adbool == "You're dead"):
                embedColour = discord.Colour.from_rgb(0, 0, 0)
            else:
                embedColour = discord.Colour.red()

            #Embed initialisation
            embedTrue = discord.Embed(
                title = 'Optimisation Results',
                description = f'Results for {ctx.author.mention}',
                colour = embedColour
            )

            #Setting thumbnail URL with exception for DMs or any errors
            try:
                thumbnailURL = ctx.guild.icon_url
            except:
                thumbnailURL = ctx.author.avatar_url

            embedTrue.set_thumbnail(url=thumbnailURL)
            embedTrue.add_field(
                name = '**Damage from bubble:**',
                value = f'{round(dmgActual):,}',
                inline = True
            )
            embedTrue.add_field(
                name = '**Health remaining:**',
                value = f'{round(healthremaining):,}',
                inline = True
            )
            embedTrue.add_field(
                name = '**Adrenaline threshold:**',
                value = f'{round(adreThreshold):,}',
                inline = False
            )
            embedTrue.add_field(
                name = '**Adrenaline activated?**',
                value = adbool,
                inline = False
            )

            if (adbool == 'No'):
                embedTrue.add_field(
                    name = '**Required HP decrease to proc adrenaline:**',
                    value = f'{round(adreProcReq):,}',
                    inline = False
                )
            await ctx.message.reply(embed=embedTrue)
        else:
            embedFalse = discord.Embed(
                title = 'Error!',
                description = f"Error in {ctx.author.mention}'s command, please type either weak, wise, wild, or warlike for bubble type",
                colour = discord.Colour.red
            )
            await ctx.message.reply(embed=embedFalse)

    @commands.command()
    async def ascalc(self, ctx, type: str, speed: str):
        """Returns the time taken to finish your last hit combo based off your weapon type and AS"""

        speed = float(str.replace(speed, "%", ""))
        speed = speed / 100
        type = str.lower(type)

        if (type == 'axe'):
            basespeed = 2.143
        elif (type == 'sword'):
            basespeed = 2.080
        elif (type == 'staff'):
            basespeed = 2.005
        elif (type == 'spear'):
            basespeed = 1.948
        elif (type == 'hammer'):
            basespeed = 1.938

        getcontext().prec = 4
        finalspeed = Decimal(basespeed) - (Decimal(basespeed / 2) * Decimal(speed))

        await ctx.send(f"Your full attack combo time is {finalspeed}s")

    @commands.command()
    async def bubblebars(self, ctx, bubbletype: str, barsleft: int):
        """Returns how much health bubble has left based on bars and bubble type."""

        bubbletype = str.lower(bubbletype)
        if bubbletype == 'weak':
            bubblehealth = 25000
        elif bubbletype == 'wise':
            bubblehealth = 30000
        elif bubbletype == 'wild':
            bubblehealth = 125000
        else:
            bubblehealth = 250000

        await ctx.send(f'**Health left on bubble:**\n{(barsleft * bubblehealth):,}')

    @commands.command()
    async def svarogbars(self, ctx, svarogtype: int, barsleft: int):
        """Returns how much health Svarog has left based on bars and bubble type."""

        if svarogtype == 1:
            svaroghealth = 25000
        elif svarogtype == 2:
            svaroghealth = 45000
        elif svarogtype == 3:
            svaroghealth = 175000
        else:
            svaroghealth = 350000
        await ctx.send(f'**Health left on Svarog:**\n{(barsleft * svaroghealth):,}')
