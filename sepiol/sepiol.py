import os
import sys

import requests
import argparse

import schedule
import irc
import irc.client
import jaraco.logging


endpoint
reqSession = requests.Session()

client_id = os.environ("")
api_headers = {'Client-ID': client_id,
               'Accept': 'application/vnd.twitchtv.v5+json'}


class BaseScheduler(irc.schedule.IScheduler):
    def execute_every(self, period, func):
        schedule.every(period).do(func)

    def execute_at(self, when, func):
        schedule.at(when).do(func)

    def execute_after(self, delay, func):
        raise NotImplementedError("Not supported")

    def run_pending(self):
        schedule.run_pending()


def isTwitchUserStreaming(user_id):
    url = endpoint.format(user_id)

    try:
        req = requests.get(url, headers=api_headers)
        twitch_user_json = req.json()
        if 'stream' in twitch_user_json:
            if twitch_user_json['stream'] is not None:
                return True
            else:
                return False
    except Exception as e:
        print("Error checking user: ", e)
        print("error, but not live")
        return False


def on_connect(connection, event):
    if irc.client.is_channel(target):
        connection.join(target)
        return
    connection.reactor.scheduler.execute_every(period=10, func=poll_twitch)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', help="a nickname or channel")
    parser.add_argument('-p', '--port', default=6667, type=int)
    parser.add_argument('-h', '--host', default='irc.freenode.net', help="The IRC server hostname.")
    parser.add_argument('-u', '--user-id', help="Your twitch user id.")
    parser.add_argument('-c', '--client_id', help="The client ID of a Twitch app.")
    parser.add_argument('-s', '--secret', help="A sequence of characters given by twitch.tv")
    parser.add_argument(-)
    jaraco.logging.add_arguments(parser)
    return parser.parse_args()


def poll_twitch(connection, twitch_user_id):
    is_streaming = False
    while True:
        if not is_streaming:
            if isTwitchUserStreaming(twitch_user_id):
                connection.privmsg(
                    target, "@samsepi0l is now live at https://twitch.tv/br4vetrav3ler")
                is_streaming = True
        elif not isTwitchUserStreaming(twitch_user_id):
            is_streaming = False
            print("Not streaming :(")


def on_disconnect(connection, event):
    raise SystemExit()


def main():
    global target

    args = get_args()
    jaraco.logging.setup(args)
    target = args.target

    reactor = irc.client.Reactor()
    try:
        c = reactor.server().connect(args.server, args.port, args.nickname)
    except irc.client.ServerConnectionError:
        print(sys.exc_info()[1])
        raise SystemExit(1)

    c.add_global_handler("welcome", on_connect)
    c.add_global_handler("join", on_join)
    c.add_global_handler("disconnect", on_disconnect)

    reactor.process_forever()


if __name__ == '__main__':
    main()
