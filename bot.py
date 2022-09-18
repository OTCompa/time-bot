from time import time
from decouple import config
import interactions
import mysql.connector

def connect():
    db = mysql.connector.connect(
        host = config('CLEARDB_DATABASE_URL'),
        user = config('CLEARDB_DATABASE_LOGIN'),
        password = config('CLEARDB_DATABASE_PASS'),
        database = config('CLEARDB_DATABASE_DBNAME')
        )
    return db

bot = interactions.Client(token=config('discordtoken'))

# Set command
@bot.command(
    name="set",
    description="Creates a new event with the specified tag.",
    scope=205384125513859074,
    default_member_permissions=interactions.Permissions.KICK_MEMBERS,
    options = [
        interactions.Option(
            name="tag",
            description="Tag to place the event under",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="event",
            description="Event name",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="starttime",
            description="Start time of event",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
        interactions.Option(
            name="endtime",
            description="End time of event",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
    ],
)
async def set(ctx: interactions.CommandContext, tag: str, event: str, starttime: int, endtime: int):
    try:
        sql = ("INSERT INTO events "
                "(tag, name, starttime, endtime) "
                "VALUES (%s, %s, %s, %s)")
        data = (tag, event, starttime, endtime)
        db = connect()
        cursor = db.cursor()
        cursor.execute(sql, data)
        db.commit()
        await ctx.send("Event successfully created.", ephemeral=True)
    except Exception as err:
        await ctx.send(f"There was an error.\n{err}", ephemeral=True)

# View command
@bot.command(
    name="view",
    description="Responds with events under the specified tag.",
    scope=205384125513859074,
    default_member_permissions=interactions.Permissions.KICK_MEMBERS,
    options = [
        interactions.Option(
            name="tag",
            description="Tag name",
            type=interactions.OptionType.STRING,
            required=True
        ),
    ],
)
async def view(ctx: interactions.CommandContext, tag: str):
    # Query tag
    currentTime = time()
    getEvents = ("SELECT name, starttime, endtime FROM events "
                    "WHERE tag=%s")
    data = (tag,)
    db = connect()
    cursor = db.cursor()
    cursor.execute(getEvents, data)
    msgToSend = ""

    # Formatting results
    events = cursor.fetchall()
    ongoing = ""
    upcoming = ""
    for event in events:
        if event[1] < currentTime and event[2] > currentTime:
            ongoing += "**" + event[0] + "** <t:" + str(event[2]) + ":F> **(Ends <t:" + str(event[2]) + ":R>)**\n"

    for event in events:
        if event[1] > currentTime:
            upcoming += "**" + event[0] + "** <t:" + str(event[1]) + ":F> **(Begins <t:" + str(event[1]) + ":R>)**\n"
    if ongoing and upcoming:
        msgToSend += "__**Ongoing Events**__\n"
        msgToSend += ongoing
        msgToSend += "\n__**Upcoming Events**__\n"
        msgToSend += upcoming
    elif ongoing:
        msgToSend += "__**Ongoing Events**__\n"
        msgToSend += ongoing
    elif upcoming:
        msgToSend += "\n__**Upcoming Events**__\n"
        msgToSend += upcoming
    else:
        msgToSend += "No events found under this tag."
    await ctx.send(msgToSend)

# Remove command
@bot.command(
    name="remove",
    description="Removes the event with the specified tag and name.",
    scope=205384125513859074,
    default_member_permissions=interactions.Permissions.KICK_MEMBERS,
    options = [
        interactions.Option(
            name="tag",
            description="Tag name",
            type=interactions.OptionType.STRING,
            required=True
        ),
        interactions.Option(
            name="event",
            description="Event name",
            type=interactions.OptionType.STRING,
            required=True
        ),
    ],
)
async def remove(ctx: interactions.CommandContext, tag: str, event: str):
    sql = ("DELETE FROM events "
            "WHERE tag=%s AND name=%s")
    data = (tag, event)
    db = connect()
    cursor = db.cursor()
    try: 
        cursor.execute(sql, data)
        db.commit()
        await ctx.send("Event successfully deleted.", ephemeral=True)
    except Exception as err:
        await ctx.send(f"There was an error.\n{err}", ephemeral=True)

# GL events command
@bot.command(
    name="glevents",
    description="View ongoing and upcoming GL events.",
    scope=205384125513859074
)
async def glevents(ctx: interactions.CommandContext):
    # Query tag
    getEvents = ("SELECT name, starttime, endtime FROM events "
                    "WHERE tag=\"glevents\"")
    db = connect()
    cursor = db.cursor()
    cursor.execute(getEvents)
    msgToSend = ""

    # Formatting results
    events = cursor.fetchall()
    currentTime = time()
    msgToSend = ""
    ongoing = ""
    upcoming = ""
    for event in events:
        if event[1] < currentTime and event[2] > currentTime:
            ongoing += "**" + event[0] + "** <t:" + str(event[2]) + ":F> **(Ends <t:" + str(event[2]) + ":R>)**\n"

    for event in events:
        if event[1] > currentTime:
            upcoming += "**" + event[0] + "** <t:" + str(event[1]) + ":F> **(Begins <t:" + str(event[1]) + ":R>)**\n"
    if ongoing and upcoming:
        msgToSend += "__**Ongoing Events**__\n"
        msgToSend += ongoing
        msgToSend += "\n__**Upcoming Events**__\n"
        msgToSend += upcoming
    elif ongoing:
        msgToSend += "__**Ongoing Events**__\n"
        msgToSend += ongoing
    elif upcoming:
        msgToSend += "\n__**Upcoming Events**__\n"
        msgToSend += upcoming
    else:
        msgToSend += "No events found under this tag."
    await ctx.send(msgToSend)

# JP events command
@bot.command(
    name="jpevents",
    description="View ongoing and upcoming JP events.",
    scope=205384125513859074
)
async def jpevents(ctx: interactions.CommandContext):
    # Query tag
    getEvents = ("SELECT name, starttime, endtime FROM events WHERE tag='jpevents'")
    db = connect()
    cursor = db.cursor()
    cursor.execute(getEvents)
    msgToSend = ""

    # Formatting results
    events = cursor.fetchall()
    currentTime = time()
    msgToSend = ""
    ongoing = ""
    upcoming = ""
    for event in events:
        if event[1] < currentTime and event[2] > currentTime:
            ongoing += "**" + event[0] + "** <t:" + str(event[2]) + ":F> **(Ends <t:" + str(event[2]) + ":R>)**\n"

    for event in events:
        if event[1] > currentTime:
            upcoming += "**" + event[0] + "** <t:" + str(event[1]) + ":F> **(Begins <t:" + str(event[1]) + ":R>)**\n"
    if ongoing and upcoming:
        msgToSend += "__**Ongoing Events**__\n"
        msgToSend += ongoing
        msgToSend += "\n__**Upcoming Events**__\n"
        msgToSend += upcoming
    elif ongoing:
        msgToSend += "__**Ongoing Events**__\n"
        msgToSend += ongoing
    elif upcoming:
        msgToSend += "\n__**Upcoming Events**__\n"
        msgToSend += upcoming
    else:
        msgToSend += "No events found under this tag."
    await ctx.send(msgToSend)

@bot.event
async def on_ready():
    await bot.change_presence(
        interactions.ClientPresence(
            activities = [interactions.PresenceActivity(
                name="test1",
                details="test2",
                state="test3",
                type=interactions.PresenceActivityType.GAME
            )]
        )
    )
    print("Bot is ready")

bot.start()
