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

        if (im):
            if(im[TYPE] == "MSG" and len(im[TEXT]) > 0):
                print("(" + im[2] + ")",
                                 "<%s> %s" % (im[FROM], im[TEXT]))
                ts.relay_message("(" + im[2] + ")",
                                 "<%s> %s" % (im[FROM], im[TEXT]))
            elif(im[TYPE == "LISTUSER"]):
                ts_user = ts.client_map()
                message = "\n"
                for user in ts_user.items():
                    message += user[1]["client_nickname"] + "\n"

                telegram.relay_message("服务器用户", message)
                continue

        if tm:
            if (tm[TYPE] == "MSG"):
                telegram.relay_message(tm[FROM], tm[TEXT])
            else:
                telegram.relay_message("", build_message(tm))

    except KeyboardInterrupt:
        telegram.disconnect()
        ts.disconnect()
