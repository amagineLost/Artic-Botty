import discord
from discord.ext import commands
import os
import traceback

# Enable all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.getenv("BOT_PREFIX", "/"), intents=intents)

# Rule Data
rules = [
    {
        "number": 1,
        "title": "Discrimination, Racism, or Hate Crime Towards Anyone",
        "description": "Any discrimination, racism, or hate crimes towards anyone is unacceptable.",
        "punishments": ["Ban (1 day)", "Ban (7 days)", "Ban (30 days)"]
    },
    {
        "number": 2,
        "title": "Aggression Towards a HR",
        "description": "Aggression towards High Ranks is deemed disrespectful and unacceptable behavior.",
        "punishments": ["Warn", "Arrest (10 minutes)", "Arrest (25 minutes)"]
    },
    {
        "number": 3,
        "title": "Ranker+ Ranking Others into Incorrect Ranks",
        "description": "It is possible to spot a Ranker or higher ranking others incorrectly. For example, giving someone an unearned role such as 'The Queen'.",
        "punishments": ["Ban (1 day)", "Demote & Ban (30 days)"]
    },
    {
        "number": 4,
        "title": "Bullying or Mistreatment Towards Another Worker",
        "description": "Disrespecting, bullying, or causing conflicts with other workers is not tolerated. Review chat logs before taking action.",
        "punishments": ["Warn", "Arrest (20 minutes)"]
    },
    {
        "number": 5,
        "title": "Trainer+ Refusing to Train",
        "description": "Trainers must not avoid training duties without a valid reason. Avoidance due to being 'tired' is not acceptable.",
        "punishments": ["Warn", "Arrest (20 minutes)", "Ban (1 day)"]
    },
    {
        "number": 6,
        "title": "Baristas Serving the Wrong Drink",
        "description": "Baristas must serve the correct drinks to workers and other players. Misconduct will result in punishments.",
        "punishments": ["Warn", "Arrest (5 minutes)"]
    },
    {
        "number": 7,
        "title": "Refusal to Work",
        "description": "Workers must be at their stations unless given permission for a break. Use `-xpcheck` to verify their activity.",
        "punishments": ["Warn", "Arrest (15 minutes)", "Arrest (30 minutes)"]
    },
    {
        "number": 8,
        "title": "Player Getting XP Through Hiding",
        "description": "Players must remain visible at their stations. Earning XP while hiding or being AFK is prohibited.",
        "punishments": ["Arrest (10 minutes)", "Arrest (20 minutes)", "Arrest (30 minutes)"]
    },
    {
        "number": 9,
        "title": "Working Incorrectly (Low Rank)",
        "description": "Lower ranks are expected to make occasional mistakes due to inexperience. However, repeated errors will result in action.",
        "punishments": ["Warn", "Arrest (15 minutes)"]
    },
    {
        "number": 10,
        "title": "Working Incorrectly (Mid Rank)",
        "description": "Mid ranks are expected to understand their roles. Frequent mistakes at this level will result in stricter actions.",
        "punishments": ["Warn", "Arrest (20 minutes)", "Set Rank To (Security)"]
    },
    {
        "number": 12,
        "title": "Using Emotes to Hide From High Ranks",
        "description": "Using emotes or similar actions to avoid detection by High Ranks is prohibited.",
        "punishments": ["Warn", "Arrest (5 minutes)", "Arrest (10 minutes)", "Arrest (15 minutes)"]
    },
    {
        "number": 13,
        "title": "Misusing the Call System",
        "description": "Players must not misuse the call system. Always provide evidence of misuse before taking action.",
        "punishments": ["Warn", "Arrest (15 minutes)", "Arrest (30 minutes)"]
    },
    {
        "number": 14,
        "title": "Working Incorrectly (Upper Rank)",
        "description": "Upper ranks should have mastered their roles. Frequent mistakes at this level will be addressed with severe action.",
        "punishments": ["Warn", "Arrest (30 minutes)", "Set Rank To (Advisor)"]
    },
    {
        "number": 15,
        "title": "Managers Not Doing Their Job On Duty",
        "description": "Managers must actively manage their departments and promote good practices. Laziness is not acceptable.",
        "punishments": ["Arrest (15 minutes)", "Arrest (20 minutes)", "Arrest (30 minutes)"]
    }
]

# Embed for a Rule
def rule_embed(rule_number, rule_title, rule_description, punishments):
    embed = discord.Embed(
        title=f"Rule {rule_number}: {rule_title}",
        description=rule_description,
        color=discord.Color.red()
    )
    embed.add_field(
        name="Punishments",
        value="\n".join([f"{i+1}. {p}" for i, p in enumerate(punishments)]),
        inline=False
    )
    embed.set_footer(text="Please follow the rules to maintain a friendly community.")
    return embed

# Manual Pagination
class Paginator:
    def __init__(self, ctx, pages):
        self.ctx = ctx
        self.pages = pages
        self.current_page = 0
        self.message = None

    async def start(self):
        self.message = await self.ctx.send(embed=self.pages[self.current_page])
        await self.message.add_reaction("⬅️")
        await self.message.add_reaction("➡️")

        bot.loop.create_task(self.wait_for_reactions())

    async def wait_for_reactions(self):
        def check(reaction, user):
            return (
                reaction.message.id == self.message.id
                and user == self.ctx.author
                and str(reaction.emoji) in ["⬅️", "➡️"]
            )

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=120.0, check=check)
                await self.message.remove_reaction(reaction, user)

                if str(reaction.emoji) == "➡️":
                    self.current_page = (self.current_page + 1) % len(self.pages)
                elif str(reaction.emoji) == "⬅️":
                    self.current_page = (self.current_page - 1) % len(self.pages)

                await self.message.edit(embed=self.pages[self.current_page])
            except Exception:
                break

# Command: Display All Rules with Pagination
@bot.command()
async def rules(ctx):
    pages = [rule_embed(rule["number"], rule["title"], rule["description"], rule["punishments"]) for rule in rules]
    paginator = Paginator(ctx, pages)
    await paginator.start()

# Event: Bot Ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Command: Strike a User
@bot.command()
@commands.has_permissions(manage_messages=True)
async def strike(ctx, user: str, rule_number: int, degree: int, punishment_length: str = None):
    try:
        rule = next((r for r in rules if r["number"] == rule_number), None)
        if not rule:
            await ctx.send(f"Rule {rule_number} not found.")
            return

        if degree < 1 or degree > len(rule["punishments"]):
            await ctx.send(f"Degree {degree} is out of range for rule {rule_number}.")
            return

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
            embed.add_field(name="Custom Punishment Length", value=punishment_length, inline=False)
        embed.set_footer(text="Issued by moderation team.")

        await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error in strike command: {e}")
        await ctx.send("An error occurred while processing the strike command.")

# Event: Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("A required argument is missing. Please check the command usage.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the required permissions to execute this command.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Use `/help` for a list of available commands.")
    else:
        await ctx.send("An unexpected error occurred.")
        print("".join(traceback.format_exception(None, error, error.__traceback__)))

# Start the bot using the token from environment variables
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
