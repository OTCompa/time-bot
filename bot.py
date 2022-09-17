# This example requires the 'message_content' intent.
from time import time
import interactions
from decouple import config
import mysql.connector

def connect():
    db = mysql.connector.connect(
        host = config('CLEARDB_DATABASE_URL'),
        user = config('CLEARDB_DATABASE_LOGIN'),
        password = config('CLEARDB_DATABASE_PASS'),
        database = config('CLEARDB_DATABASE_DBNAME')
        )
    return db

TABLES = {}
TABLES['events'] = (
    "CREATE TABLE 'events' ("
    "'id' int PRIMARY KEY UNIQUE AUTO_INCREMENT,"
    "'tag' varchar NOT NULL,"
    "'starttime' int(11) NOT NULL,"
    "'endtime' int(11) NOT NULL"
)

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
    scope=205384125513859074, # remove after done testing
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
            ongoing += "**" + event[0] + "** <t:" + str(event[2]) + ":F> **(<t:" + str(event[2]) + ":R>)**\n"

    for event in events:
        if event[1] > currentTime:
            upcoming += "**" + event[0] + "** <t:" + str(event[1]) + ":R>\n"
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

bot.start()