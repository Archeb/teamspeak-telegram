import requests
import threading
import traceback

from queue import Queue


class TelegramConnection:
    _send_queue = Queue()
    _recv_queue = Queue()
    _running = False
    _lastUpdate = 0

    def __init__(self, api, authToken, chatId):
        self._api = api + "bot" + authToken
        self._chatId = chatId

    def run(self):
        try:
            r = requests.get(self._api + "/getMe")
            if r.json()["ok"] == True:
                print("[Telegram] Connected to Telegram API")
                self._running = True
                self._recv_thread = threading.Thread(target=self.listen)
                self._recv_thread.start()
            else:
                print(r.json())
                print("[Telegram] Failed to get bot info, maybe wrong auth token?")
                return
        except:
            print("[Telegram] Failed to get bot info")
            print(traceback.format_exc())
            return

    def getUpdates(self):
        # print("[Telegram] Polling...")
        try:
            r = requests.get(self._api + "/getUpdates?timeout=100&offset=" + str(self._lastUpdate), stream=True)

            if r.encoding is None:
                r.encoding = 'utf-8'

            update = r.json()

            if(update["ok"] == True):
                print("[Telegram] Get new update")
                return update
            else:
                print(update)
                print("[Telegram] Failed to get update")
                return False

        except:
            print("[Telegram] Failed to get update")
            print(traceback.format_exc())
            return False

    def listen(self):
        while self._running:
            try:
                newUpdate = self.getUpdates()
                if newUpdate:
                    for update in newUpdate["result"]:
                        if "message" in update and "text" in update["message"]:
                            self._lastUpdate = update["update_id"] + 1
                            print(update)
                            if update["message"]["text"][0:10] == "/getchatid":
                                self.send_text(
                                    update["message"]["chat"]["id"],
                                    "chat_id: " + str(update["message"]["chat"]["id"]),"")
                            elif update["message"]["chat"]["id"] == self._chatId:
                                if(update["message"]["text"].startswith("/ts_") or update["message"]["text"].startswith("/ts ")):
                                    if "username" in update["message"]["from"]:
                                        displayname = update["message"]["from"]["username"]
                                    else:
                                        displayname = update["message"]["from"]["first_name"]
                                    self._recv_queue.put(
                                        ("GLOBALMSG", displayname,
                                         "Telegram",
                                         update["message"]["text"][4:]))
                                else:
                                    if "username" in update["message"]["from"]:
                                        displayname = update["message"]["from"]["username"]
                                    else:
                                        displayname = update["message"]["from"]["first_name"]
                                    self._recv_queue.put(
                                        ("MSG", displayname,
                                         "Telegram",
                                         update["message"]["text"]))
            except:
                print("[Telegram] Error while fetching updates from Telegram API")
                print(traceback.format_exc())

    def relay_message(self, user, msg):
        if user == "":
            # 系统消息
            self.send_text(self._chatId, msg, "MarkdownV2")
        else:
            # 用户消息
            self.send_text(self._chatId, user + ": " + msg, "")

    def send_text(self, chatid, text, parse_mode="MarkdownV2"):
        if not text or not self._running or not chatid:
            return

        data = {
            "text": text,
            "chat_id": chatid,
            "parse_mode": parse_mode
        }
        try:
            response = requests.post(self._api + "/sendMessage", data, timeout=1)
            print(response.json())
        except:
            print("[Telegram] Error while sending message to Telegram API")
            print(traceback.format_exc())

    def poll(self):
        if self._recv_queue.empty():
            return None

        return self._recv_queue.get()

    def disconnect(self):
        self._running = False

    def running(self):
        return self._running
