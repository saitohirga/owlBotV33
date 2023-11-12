import discord
import data.key
import datetime, os
from discord.ext import commands
from Utilities.Logging import autoLog


"""

    Refactored a significant amount just to future-proof it.
    All Cogs are located in /Cogs, and are loaded into the client like client.load_extension('Cogs.Thing')

    Most common practice for python main files is the name/main conditional statement show below.
    Not completely necessary but it's "proper" and I am ALIVE!

    ----
    There is also a logger function to help maintain readable but verbose monitoring in terminal.
    Check the import at the top

        autoLog(message, color-type)

"""

# pulls in all cogs in /Cogs and automatically registers them
def load(client):
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"Cogs.{filename[:-3]}")

def main():
    autoLog('Revving up my tiny little motor...', 'bold')
    # god I hate discord's intent system shit, not because it exists, 
    # but because every demo and documentation conveniently left it the fuck out
    intents = discord.Intents.default()
    intents.message_content = True

    # see https://stackoverflow.com/questions/71369200/pycord-error-discord-errors-extensionfailed-extension-cogs-cmds-raised-an-er
    client = commands.Bot(command_prefix='.', intents=intents) # had to be changed to commands.Bot from discord.Bot
    load(client)

    # does the thing
    client.run(data.key.token)

if __name__ == "__main__":
    # the machine wakes up
    print('.                                                                              .')
    print(' .&&&&*...........................&&&&&&&&&&..............................*&&&&.')
    print('  ..&&&   #&&&&&&&&&&&&&&&&&&&&&&&%        &&&&&&&&&&&&&&&&&&&&&&&&&&&&/  &&&.. ')
    print('   ..&&&&                       &     &     &&&&        &&              (&&&..  ')
    print('    .%&&&&*          &&&&&&&&&.     &&&(    *&&&&      &&&&          &&&&#.     ')
    print('       ..&&&              &&&                 &&&       &&&&     %&&&&..        ')
    print('       ..&&/    &%   &&&/       &&&&&&&&&&&       &&         &%     &&..        ')
    print('         .%&.      &&&&&&&&      &&&&&&&&,     &&&      &&&&&     ,&/.          ')
    print('     ..&&      *&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&      *&&&..      ')
    print('    .&&,&&&&&&&&&&&&##%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&###&&&&&&&&&&*& &%.     ')
    print('   .&&&&&&&&&&&&&&&&&&&######&&&&&&&&&&&&&&&&&&&&&######&&&&&&&&&&&&&&&&&&.     ')
    print('    .,&&..&&&&&&  &&&&&&&&&&&#####&&&&&&&&&&%#####&&&&&&&&&&&  &&&&&&.(&&.      ')
    print('       ..&&&&&(  &&&&...&&&&&&&&&&###&&&&%###&&&&&&&&&&...&&&&  %&&&&&..        ')
    print('       .%&&&&& ,&&&&&..&&&&&  &&&&&&&&#&#&&&&&&&&  &&&&(.,&&&%&  &&&&&(.        ')
    print('       ..&&&&&% &&&&&&&..&&&&&&&&..&&&&/&&&&..&&&&&&&&..&&&&&&& &&&&&&..        ')
    print('        ..(&&&&&   &&&&&&&&&&&&&&&&&&&&/..&&&&&&&&&&&&&&&&&&   &&&&&*..         ')
    print('           ..&&&&&&.    %&&&&&&&&&&&.&&/...&&&&&&&&&&&%    *&&&&&&..            ')
    print('              ...*&&&&&&&         &&&.&/..(&&         &&&&&&&....               ')
    print('                    .....&&&&&&&&&&&&&./.&&&&&&&&&&&&&.....                     ')
    print('                             ........&&&........                                \n')
    # print('<=[[LOGGING]]=>')
    print('<<<<----------------------------<=[[LOGGING]]=>------------------------------->>>')
    main()
