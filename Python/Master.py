from Project import Project
import argparse
from pythonosc import udp_client

search = "cat"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="192.168.1.145",
                        help="The ip of the OSC server")
    parser.add_argument("--port2", default=12000,
                        help="The port the OSC server is listening on")
    parser.add_argument("--port", type=int, default=7004,
                        help="The port the OSC server is listening on")
    args = parser.parse_args();

client = udp_client.SimpleUDPClient(args.ip, args.port)

client.send_message("/HA/Jackfreesound", search)

SimpleThings = Project(search, 10, 25)
SimpleThings.Haiku.display_haiku()