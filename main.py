# This example covers advanced startup options and uses some real world examples for why you may need them.

import asyncio
import logging
import logging.handlers
import os
import config
import jishaku

from typing import List, Optional

import asyncpg  # asyncpg is not a dependency of the discord.py, and is only included here for illustrative purposes.
import discord
from discord.ext import commands
from aiohttp import ClientSession


class AxomBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        db_pool: asyncpg.Pool,
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.db_pool = db_pool
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            await self.load_extension(extension)

async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    intents = discord.Intents.default()
    intents.message_content = True
    exts = ['jishaku']
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            exts.append(f'cogs.{filename[:-3]}')
    async with asyncpg.create_pool(dsn=config.DB_LINK,min_size=1,max_size=5) as pool:
        async with AxomBot(commands.when_mentioned_or("*"), db_pool=pool, initial_extensions=exts,intents=intents) as bot:
                await bot.start(config.DISCORD_TOKEN)


# For most use cases, after defining what needs to run, we can just tell asyncio to run it:
asyncio.run(main())