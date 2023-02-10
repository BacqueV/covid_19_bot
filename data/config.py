from environs import Env

# using environs library
env = Env()
env.read_env()

# environment variables
BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
