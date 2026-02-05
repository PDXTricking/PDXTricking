import discord
from discord.ext import commands
import mysql.connector
import datetime
import asyncio
import os

# Discord bot setup
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Database configuration
DB_HOST = '127.0.0.1'
DB_USER = os.getenv('BLOG_DB_USER')
DB_PASSWORD = os.getenv('BLOG_DB_PW')
BLOG_DB_NAME = 'blog_db'

db_config = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'database': BLOG_DB_NAME,
}

def get_daily_question():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    today = datetime.date.today()
    query = "SELECT * FROM daily_questions WHERE asked_date = %s"
    cursor.execute(query, (today,))
    
    question = cursor.fetchone()
    
    if not question:
        query = "SELECT * FROM daily_questions WHERE asked_date IS NULL LIMIT 1"
        cursor.execute(query)
        question = cursor.fetchone()
        
        if question:
            update_query = "UPDATE daily_questions SET asked_date = %s WHERE id = %s"
            cursor.execute(update_query, (today, question['id']))
            connection.commit()
    
    cursor.close()
    connection.close()
    return question['question'] if question else "No more questions available."

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    channel = bot.get_channel(YOUR_CHANNEL_ID)  # Replace with your channel ID
    while True:
        question = get_daily_question()
        await channel.send(f"**Today's Question**: {question}")
        await asyncio.sleep(86400)  # Wait for 1 day

@bot.command(name='addquestion')
async def add_question(ctx, *, question_text):
    """Add a new question to the database."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    add_query = "INSERT INTO daily_questions (question) VALUES (%s)"
    cursor.execute(add_query, (question_text,))
    connection.commit()
    
    cursor.close()
    connection.close()
    await ctx.send(f"Question added: {question_text}")

if __name__ == '__main__':
    bot.run(TOKEN)
