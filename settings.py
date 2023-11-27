from environs import Env

env = Env()
env.read_env()

API_KEY = env.str('API_KEY')

