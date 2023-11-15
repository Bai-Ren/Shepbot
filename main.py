import websocket
import _thread
import time
import rel

def on_message(ws, message):
    print("Got message")
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    file = open("oauth.txt")
    oauth = file.readline()
    nick = file.readline()
    channel = file.readline()
    file.close()
    ws.send("PASS oauth:" + oauth)
    ws.send("NICK " + nick)
    ws.send("JOIN #" + channel)

if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
