import discord
from discord.ext import commands
import os

# Enable all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.getenv("BOT_PREFIX", "/"), intents=intents)

# Example Embed for Rule 1
def rule_embed(rule_number, rule_title, rule_description, punishments):
    embed = discord.Embed(
        title=f"Rule {rule_number}: {rule_title}",
        description=rule_description,
        color=discord.Color.red()
    )

    embed.add_field(name="Punishments", value="\n".join([f"{i+1}. {p}" for i, p in enumerate(punishments)]), inline=False)
    embed.set_footer(text="Please follow the rules to maintain a friendly community.")
    return embed

# Rule Data
rules = [
    {
        "number": 1,
        "title": "Discrimination, Racism, or Hate Crime Towards Anyone",
        "description": (
            "Any Discrimination, Racism, or Hate Crimes towards anyone is a potential usage of hatred "
            "performed by the following user that has attacked another. It is requested to follow along "
            "the punishments and give them rightfully fairness of punishment."
        ),
        "punishments": ["Ban (1 day)", "Ban (7 days)", "Ban (30 days)"]
    },
    {
        "number": 2,
        "title": "Aggression Towards a HR",
        "description": (
            "Aggression towards High Ranks is seen as an unacceptable and deemed as disrespectful "
            "towards the High Rank user."
        ),
        "punishments": ["Warn", "Arrest (10 minutes)", "Arrest (25 minutes)"]
    },
    {
        "number": 3,
        "title": "Ranker+ Ranking Others into Incorrect Ranks",
        "description": (
            "It is potentially possible to spot a Ranker or higher attempting to rank themselves or others "
            "into incorrect ranks. If someone is attempting to rank another player to a rank that is incorrect, "
            "such as 'The Queen' role, simply give them the receiving punishments necessary. Try to identify "
            "them in-game despite their presence not being seen in-game."
        ),
        "punishments": ["Ban (1 day)", "Demote & Ban (30 days)"]
    },
    {
        "number": 4,
        "title": "Bullying or Mistreatment Towards Another Worker",
        "description": (
            "If a worker is caught disrespecting, bullying, or causing a scene between another user by being "
            "aggressive, it is requested to view the chat logs before attempting to resolve the situation. "
            "Afterwards, try to give them advice to solve and fix the issue. If continued, it results in the "
            "following punishments."
        ),
        "punishments": ["Warn", "Arrest (20 minutes)"]
    },
    {
        "number": 5,
        "title": "Trainer+ Refusing to Train",
        "description": (
            "This applies only if Trainers are caught avoiding the training entirely for an unreasonable "
            "circumstance. For example, avoiding training recruits because they are 'tired' is an unacceptable act."
        ),
        "punishments": ["Warn", "Arrest (20 minutes)", "Ban (1 day)"]
    },
    {
        "number": 6,
        "title": "Baristas Serving the Wrong Drink",
        "description": (
            "Baristas are in charge of serving the Queen and workers around the map drinks to replunge "
            "their necessity bars. However, it is unacceptable to give the workers+ the wrong drink. "
            "It is not by any means allowed and will result in fair punishment. Baristas may refuse to "
            "give service if the worker is breaking the rules."
        ),
        "punishments": ["Warn", "Arrest (5 minutes)"]
    },
    {
        "number": 7,
        "title": "Refusal to Work",
        "description": (
            "Workers are required to be at their station at all times to avoid receiving punishment. "
            "However, you must do an XP check on them to see if it's under 20 minutes by simply doing "
            "-xpcheck (username) 60'. If they're under the required amount, you may proceed with action. "
            "However, if they're above or at least at 20 minutes, you may give them free time for a few minutes."
        ),
        "punishments": ["Warn", "Arrest (15 minutes)", "Arrest (30 minutes)"]
    },
    {
        "number": 8,
        "title": "Player Getting XP Through Hiding",
        "description": (
            "Players are required to be visible at their station and not gaining XP by achieving this way of "
            "hiding behind objects to go AFK or potentially just avoiding in general. Players should be at "
            "all cost active and visible to the direct eyes of moderation."
        ),
        "punishments": ["Arrest (10 minutes)", "Arrest (20 minutes)", "Arrest (30 minutes)"]
    },
    {
        "number": 9,
        "title": "Working Incorrectly (Low Rank)",
        "description": (
            "Lower ranks are the newest workers and have less experience behind the stations, they're "
            "expected to have more mishaps than usual. Therefore the level of punishment is less severe "
            "than average. The issue only applies if the worker is making varieties of mistakes within the job. "
            "Please remember that if the player is under 10% marked for percentage complete within the rank "
            "they'll be expected to make mistakes."
        ),
        "punishments": ["Warn", "Arrest (15 minutes)"]
    },
    {
        "number": 10,
        "title": "Working Incorrectly (Mid Rank)",
        "description": (
            "Mid ranks should understand more of the basics of how to work by now, so the punishments "
            "will be more severe than previously. This issue only will apply if the worker is making "
            "varieties of mistakes within the job."
        ),
        "punishments": ["Warn", "Arrest (20 minutes)", "Set Rank To (Security)"]
    },
    {
        "number": 12,
        "title": "Using Emotes to Hide From High Ranks",
        "description": (
            "A worker may use our emotes and etc. At a desk however, using this to avoid being caught "
            "may result in punishment."
        ),
        "punishments": ["Warn", "Arrest (5 minutes)", "Arrest (10 minutes)", "Arrest (15 minutes)"]
    },
    {
        "number": 13,
        "title": "Misusing the Call System",
        "description": (
            "If a user is misusing the call system it is required to hold out available evidence to prove "
            "that it was misused. For example, failure to provide following evidence of the situation will "
            "hold you accountable for your action."
        ),
        "punishments": ["Warn", "Arrest (15 minutes)", "Arrest (30 minutes)"]
    },
    {
        "number": 14,
        "title": "Working Incorrectly (Upper Rank)",
        "description": (
            "Upper ranks have basically mastered the game at working, this shouldn't be a frequent issue "
            "for them to occur. This issue only applies if the worker is making a variety of mistakes "
            "within the job. Please remember if they're under 10% they are likely to still have reoccurring "
            "sometimes frequent issues so take into accountability and consideration that they're still "
            "processing and learning."
        ),
        "punishments": ["Warn", "Arrest (30 minutes)", "Set Rank To (Advisor)"]
    },
    {
        "number": 15,
        "title": "Managers Not Doing Their Job On Duty",
        "description": (
            "If any manager is being lazy to manage the department they were given that is representing you, "
            "you may take action. The rulebook states that Managers must promote good practice within their "
            "designated department that they are representing and suggest changes."
        ),
        "punishments": ["Arrest (15 minutes)", "Arrest (20 minutes)", "Arrest (30 minutes)"]
    }
]

# Embed for Strike Messages
def strike_embed(user, rule_number, degree, punishment_length=None):
    rule = next((r for r in rules if r["number"] == rule_number), None)
    if not rule:
        return None

    embed = discord.Embed(
        title=f"Strike Issued to {user}",
        description=(
            f"**Rule {rule_number}: {rule['title']}**\n"
            f"{rule['description']}\n\n"
            f"**Degree:** {degree}\n"
            f"**Punishment:** {rule['punishments'][degree - 1]}"
        ),
        color=discord.Color.orange()
    )

    if punishment_length:
        embed.add_field(name="Custom Punishment Length", value=f"{punishment_length}", inline=False)

    embed.set_footer(text="Issued by moderation team.")
    return embed

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def rules(ctx):
    for rule in rules:
        embed = rule_embed(rule["number"], rule["title"], rule["description"], rule["punishments"])
        await ctx.send(embed=embed)

@bot.command()
async def strike(ctx, user: str, rule_number: int, degree: int, punishment_length: str = None):
    embed = strike_embed(user, rule_number, degree, punishment_length)
    if embed:
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Rule {rule_number} not found. Please check the rule number and try again.")

# Start the bot using the token from environment variables
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
