import asyncio
import asyncssh
import sys

server = "bandit.labs.overthewire.org"
port = 2220
password = "bandit0"  # level 0 password
usernamePrefix = "bandit"

commands = [
    "cat readme",
    "cat ./-",
    "cat '.spaces in this filename'",
    "cat inhere/.hidden",
    "cat inhere/-file07",
]


# Connect and fetch next level password
async def getPassword(level):
    global password
    username = usernamePrefix + str(level)

    async with asyncssh.connect(
        server, port=port, username=username, password=password
    ) as conn:
        password = (await conn.run(commands[level])).stdout.strip()
        print(f"Level {level} passed! {password}")


# Levels controller
def runLevels():
    # Iterate over registered commands
    for level in range(len(commands)):
        try:
            asyncio.get_event_loop().run_until_complete(getPassword(level))
        except (OSError, asyncssh.Error) as ex:
            sys.exit(
                f"SSH connection failed: either server is not available or command is wrong ({str(ex)})"
            )


# Entry function
if __name__ == "__main__":
    runLevels()
