from redbot.core import commands

class MQstats(commands.Cog):

    @commands.command()
    async def adcalc(self, ctx, might: str, health: str, defence: str):
        """Returns multiple statistics for bubble damage, set health, and adrenaline optimisation"""

        might = int(str.replace(might, ",", ""))
        health = int(str.replace(health, ",", ""))
        defence = int(str.replace(defence, "%", ""))


        defence = defence / 100
        coeff = 2.79

        dmg = might / coeff
        dmgShielded = dmg * defence

        dmgActual = dmg - dmgShielded

        healthremaining = health - dmgActual
        adreThreshold = health * 0.2

        adreProcReq = healthremaining - adreThreshold + 1

        if (healthremaining <= 0):
            adbool = "MF you're dead"
        elif (healthremaining < adreThreshold):
            adbool = "Yes"
        else:
            adbool = 'No'

        await ctx.send(f"Damage from bubble: {round(dmgActual):,}")
        await ctx.send(f"Health remaining: {round(healthremaining):,}")
        await ctx.send(f"Adrenaline threshold: {round(adreThreshold):,}")
        await ctx.send(f"Adrenaline activated? {adbool}")
        if (adbool == 'No'):
            await ctx.send(f"Required HP decrease to proc adrenaline: {round(adreProcReq)}")

    @commands.command()
    async def ascalc(self, ctx, type: str, speed: str):
        """Returns the time taken to finish your last hit combo based off your weapon type and AS"""

        speed = float(str.replace(speed, "%", ""))
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

        finalspeed = float(basespeed - ((basespeed / 2) * speed))

        await ctx.send(f"Your LHC time is {finalspeed}s")
