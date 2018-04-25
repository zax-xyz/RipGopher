import socket
import datetime
import itertools
import time
import traceback

def current_time():
    t = datetime.datetime.now()
    return t.strftime("%y-%m-%d %H:%M:%S ")

def connect():
    global s
    print(current_time(), "CONNECTING")
    s = socket.socket()
    s.connect((Host, Port))
    s.send(bytes("PASS " + Pass + "\r\n", "UTF-8"))
    s.send(bytes("NICK " + Nick + "\r\n", "UTF-8"))
    s.send(bytes("JOIN #" + Channel + " \r\n", "UTF-8"))
    print(current_time(), "CONNECTED")
    while True:
        line = str(s.recv(1024))
        if "End of /NAMES list" in line:
            print(current_time(), f"Entered {Channel}'s chat")
            break

def auto_reconnect():
    if len(line) == 0:
        sec = 2
        for i in itertools.count():
            try:
                print(current_time(), f"Reconnecting in {str(secs)} seconds...")
                s.close()
                time.sleep(sec)
                if sec != 16 and i % 2 == 1:
                    sec *= 2
                connect()
                break
            except:
                traceback.print_exc()
                pass

def send_message(msg):
    s.send(bytes("PRIVMSG #" + Channel + " :" + msg + "\r\n", "UTF-8"))

def write(history):
    with open('kill_count.txt', 'w', encoding='utf-8') as kill_count_file:
        kill_count_file.write(f"{kill_count} {raw_count}")
    with open('kill_history.txt', 'a', encoding='utf-8') as kill_history_file:
        kill_history_file.write(f"{current_time()} {history} ({username})\n")
    print(current_time(), history, f"({username})")

def parse_commands():
    parts = line.split(':')
    if line.startswith('PING'):
        s.send(bytes("PONG\r\n", "UTF-8"))
    elif len(parts) > 2:
        message = ':'.join(parts[2:])
        username = parts[1].split("!")[0]
        m_parts = message.split()
        return message, username, m_parts
    return None, None, None

def handle_commands():
    global kill_count
    global raw_count
    if com == '!gopherkilled':
        kill_count += 1
        raw_count += 1
        write('Gopher killed')
        send_message(f"Ninten the vicious murderer has now killed gopher "
            f"a total of {raw_count} times. May he rest in peace. <3")
    elif com == '!gophersaved':
        kill_count -= 1
        write('Gopher death undone')
        send_message("Gopher has been freed from the depths of ninten's wrath.")
    elif com in ['!gopherdeaths', '!howmanytimesintotalhasnintenthevicious'
                 'murdererkilledgopherfromthehundredacrewood'
                 'basedonthechildrensshowwinniethepoohsofar']:
        send_message('Ninten the vicious murderer has killed gopher '
            f'a total of {raw_count} times. (K/S count of {kill_count})')
    elif com == '!setkillcount' and username == Owner:
        raw_count = m_parts[1]
        write('Gopher death_count set to raw_count}')
        send_message(f"Set gopher death count to {raw_count}.")
    elif com == '!setkscount' and username == Owner:
        kill_count = m_parts[1]
        write(f'Gopher death_count set to {kill_count}')
        send_message(f"Set gopher death count to {kill_count}.")

if __name__ == '__main__':
    Host = "irc.twitch.tv"
    Port = 6667
    Owner = 'zaxu__'  # Put username in lowercase

    with open("auth", "r", encoding='utf-8') as auth_file:
        line = auth_file.readline().split()
        Nick = line[0].lower()
        Pass = line[1]
        Channel = line[2]

    with open("kill_count.txt", "r", encoding='utf-8') as kill_file:
        line = kill_file.readline().strip()
        kill_count = int(line[0] or 0)
        raw_count = int(line[1] or kill_count)

    connect()

    while True:
        line = s.recv(1024).decode("utf-8")
        auto_reconnect()

        message, username, m_parts = parse_commands()
        if message:
            handle_commands()
