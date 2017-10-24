import socket
import datetime
import itertools


Host = "irc.twitch.tv"
Port = 6667

with open("auth", "r", encoding='utf-8') as auth_file:
    line = auth_file.readline().split()
    Nick = line[0]
    Pass = line[1]
    Channel = line[2]

with open("kill_count.txt", "r", encoding='utf-8') as kill_count_file:
    try:
        kill_count = int(kill_count_file.readline())
    except:
        kill_count = 0

def connect():
    global s
    global line
    print("CONNECTING")
    s = socket.socket()
    s.connect((Host, Port))
    s.send(bytes("PASS " + Pass + "\r\n", "UTF-8"))
    s.send(bytes("NICK " + Nick + "\r\n", "UTF-8"))
    s.send(bytes("JOIN #" + Channel + " \r\n", "UTF-8"))
    print("CONNECTED")
    while True:
        line = str(s.recv(1024))
        if "End of /NAMES list" in line:
            print("Entered " + Channel + "'s chat")
            break

connect()

def send_message(msg):
    s.send(bytes("PRIVMSG #" + Channel + " :" + msg + "\r\n", "UTF-8"))

def current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")


while True:
    line = s.recv(1024).decode("utf-8")
    if len(line) == 0:
        for i in itertools.count():
            try:
                sys_print_write("Reconnecting in " + str(sec) + " seconds...")
                s.close()
                time.sleep(sec * 1000)
                if sec != 16 and i % 2 == 1:
                    sec *= 2
                connect()
                sec = 2
                break
            except:
                pass
    parts = line.split(':')
    if line.startswith('PING'):
        print("---RECEIVED PONG---")
        s.send(bytes("PONG\r\n", "UTF-8"))
        print("---SENT PONG---")
    elif len(parts) > 2:
        message = ':'.join(parts[2:])
        username = parts[1].split("!")[0]
        m_parts = message.split()
        com = m_parts[0]

        if com == '!gopherkilled':
            kill_count += 1
            with open('kill_count.txt', 'w', encoding='utf-8') as kill_count_file, open('kill_history.txt', 'a', encoding='utf-8') as kill_history_file:
                kill_count_file.write(str(kill_count))
                kill_history_file.write('{} Gopher killed ({})\n'.format(current_time(), username))
                print('{} Gopher killed ({})'.format(current_time(), username))
            send_message("Ninten the vicious murderer has now killed gopher a total of {} times. May he rest in peace. <3".format(kill_count))
        elif com == '!gophersaved':
            kill_count -= 1
            with open('kill_count.txt', 'w', encoding='utf-8') as kill_count_file, open('kill_history.txt', 'a', encoding='utf-8') as kill_history_file:
                kill_count_file.write(str(kill_count))
                kill_history_file.write('{} Gopher death undone ({})\n'.format(current_time(), username))
                print('{} Gopher death undone ({})'.format(current_time(), username))
            send_message("Somebody has saved gopher from the depths of ninten's wrath. Welcome back to life, gopher. NamineHi")
        elif com == '!howmanytimesintotalhasnintentheviciousmurdererkilledgopherfromthehundredacrewoodbasedonthechildrensshowwinniethepoohsofar':
            send_message('Ninten the vicious murderer has killed gopher a total of {} times.'.format(kill_count))
        elif com == '!setkillcount' and username == 'zax_____':
            with open('kill_count.txt', 'w', encoding='utf-8') as kill_count_file, open('kill_history.txt', 'a', encoding='utf-8') as kill_history_file:
                kill_count = m_parts[1]
                kill_count_file.write(str(kill_count))
                kill_history_file.write('{} Gopher death_count set to {} ({})\n'.format(current_time(), kill_count, username))
                print('{} Gopher death_count set to {} ({})'.format(current_time(), kill_count, username))
            send_message("Set gopher death count to {}.".format(kill_count))