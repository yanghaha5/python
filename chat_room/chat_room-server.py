"""
【5】 扩展功能：服务器可以向所有用户发送公告:管理员消息： xxxxxxxxx
"""

from socket import *
import os, sys


addr_port = ("0", 8080)  # 服务器地址
dict_info = {}  # 不写全局变量,传入参数时亦可


def do_request(socketfd):
    while True:
        data, addr = socketfd.recvfrom(2048)
        msg = data.decode().split(" ")
        # print(msg)
        # print(msg[0])
        # print(msg[1])

        if msg[0] == "L":
            do_login(addr, msg[1], socketfd)
        elif msg[0] == "C":
            msg = " ".join(msg[2:])
            # print(msg)
            do_chat(msg[1], msg, socketfd)

        # if result_login == "-1":
        elif msg[0] == "Q":
            if msg[1] not in dict_info:
                socketfd.sendto(b"exit",addr)
                continue
            do_quit(socketfd, msg[1])
        # print(dict_info)


def do_quit(s, name):
    msg = "退出聊天%s" % name
    for i in dict_info:
        if i != name:

            s.sendto(msg.encode(), dict_info[i])
        else:
            s.sendto(b"EXIT", dict_info[i])

    del dict_info[name]


def do_login(addr, name, socketfd):
    if name in dict_info or "管理员" in name:
        socketfd.sendto("已经存在".encode(), addr)
        return
    socketfd.sendto("ok".encode(), addr)

    # 通知全体
    send_2_everyone(name, socketfd)
    dict_info[name] = addr


def send_2_everyone(name, socketfd):
    msg = "欢迎%s进入聊天室" % name
    for i in dict_info:
        socketfd.sendto(msg.encode(), i[name])


def do_chat(name, msg, socketfd):
    msg = name + ":" + msg
    for i in dict_info:
        if i != name:
            socketfd.sendto(msg.encode(), dict_info[i])


def main():  # 创建网络链接
    # 创建udp网络套接字
    socketfd = socket(AF_INET, SOCK_DGRAM)
    socketfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    socketfd.bind(addr_port)

    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            msg = input("管理员消息:")
            msg = "C 管理员消息 " + msg
            socketfd.sendto(msg.encode(), addr_port)
    else:
        do_request(socketfd)  # 处理客户请求

    # socketfd.close()


if __name__ == "__main__":
    main()
