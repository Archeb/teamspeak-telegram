import config

from TelegramConnection import TelegramConnection
from TSConnection import TSConnection

TYPE = 0
FROM = 1
TEXT = 3

telegram = TelegramConnection(**config.telegram_config)
telegram.run()

ts = TSConnection(**config.teamspeak_config)
ts.run()


def build_message(event):
    print(event)

    if not event:
        return None

    if event[TYPE] == "MSG":
        return "<%s> %s" % (event[1], event[3])
    elif event[TYPE] == "ACTION":
        return "* %s %s" % (event[1], event[3])
    elif event[TYPE] == "CONNECT":
        return "* %s *进入了 TeamSpeak 服务器" % (event[1], )
    # 太吵了，关掉
    # elif event[TYPE] == "MOVE":
    #     return "* %s 从频道 [%s] 跑到了频道 [%s] *" % (event[1], event[2], event[3])
    elif event[TYPE] == "QUIT":
        return "* %s *离开了 TeamSpeak 服务器" % (event[1], )
    else:
        return None


while telegram.running() and ts.running():

    try:
        im = telegram.poll()
        tm = ts.poll()

        if (im and len(im[TEXT]) > 0):
            if(im[TYPE] == "MSG"):
                # print(im)
                ts.relay_message("(" + im[2] + ")",
                                 "<%s> %s" % (im[FROM], im[TEXT]))
            elif(im[TYPE == "GLOBALMSG"]):
                if(im[TEXT] == "getinfo"):
                    ts_user = ts.client_map()
                    ts_channel = ts.channel_map()
                    message = ""
                    for channel in ts_channel.items():
                        if len(channel[1]["members"]) > 0:
                            message += "\r\n" + ts.get_channel_name_with_relation(channel[1]) + ":"
                            for member in channel[1]["members"]:
                                message += " [" + ts.decode(ts_user[member]["client_nickname"]) + "]"

                    telegram.relay_message("服务器用户", message)
                    continue

                ts.relay_global_message(
                    "(" + im[2] + ")", "<%s> %s" % (im[FROM], im[TEXT]))
        if tm:
            if (tm[TYPE] == "MSG"):
                telegram.relay_message(tm[FROM], tm[TEXT])
            else:
                telegram.relay_message("", build_message(tm))

    except KeyboardInterrupt:
        telegram.disconnect()
        ts.disconnect()
