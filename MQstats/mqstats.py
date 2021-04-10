from redbot.core import commands

class MQstats(commands.Cog):

    @commands.command()
    async def adcalc(self, ctx, might: str, health: str, defence: str):

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

        await ctx.send(f"Actual damage: {round(dmgActual):,}")
        await ctx.send(f"Health remaining: {round(healthremaining):,}")
        await ctx.send(f"Adrenaline threshold: {round(adreThreshold):,}")
        await ctx.send(f"Adrenaline activated? {adbool}")
        if (adbool == 'No'):
            await ctx.send(f"HP decrease for adrenaline proc: {round(adreProcReq)}")
