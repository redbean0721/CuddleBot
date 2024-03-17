import yaml
import wavelink

config = yaml.safe_load(open("config.yml", "r"))["Wavelink"]


async def connect_wavelink(bot):
    nodes = [wavelink.Node(uri=config["url"], password=config["password"])]
    await wavelink.Pool.connect(nodes=nodes, client=bot, cache_capacity=100)
