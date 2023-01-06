import config

from discord.ext.commands import Bot

import commands_folder.BotCommands as BotCommands
import events_folder.BotEvents as BotEvents

def main():
    modules = config.modules

    bot = Bot(help_command = None)

    cogs = {
        BotCommands: modules['commands'],
        BotEvents: modules['events']
    }

    for cog in cogs:
        if not cogs[cog]: continue
        cog.setup(bot)
        print(f'Ког установлен: {cog.__name__}')

    bot.run(config.token)

if __name__ == '__main__':
    main()
