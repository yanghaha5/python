"""
【1】 有人进入聊天室需要输入姓名，姓名不能重复
【2】 有人进入聊天室时，其他人会收到通知：xxx 进入了聊天室
【3】 一个人发消息，其他人会收到：xxx ： xxxxxxxxxxx
【4】 有人退出聊天室，则其他人也会收到通知:xxx退出了聊天室
 1 搭建网络链接
 2 进入聊天室
 3 聊天
 4 退出聊天室
 5 管理员消息
"""

from socket import *
import os, sys
import time

addr_port = ("172.40.91.188", 8888)


# 搭建网络链接
def main():
    socketfd = socket(AF_INET, SOCK_DGRAM)
    socketfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    name = sign_in(socketfd)  # 注册
    chatting(name, socketfd)  # 聊天
    exit_chat()

    socketfd.close()


def exit_chat():
    pass


def chatting(name, socketfd):
    pid = os.fork()
    if pid < 0:
        sys.exit("error")
    elif pid == 0:
        sent_msg(name, socketfd)
    else:
        recv_msg(socketfd)


def recv_msg(socketfd):
    while True:
        data, addr = socketfd.recvfrom(1024)
        if data.decode() == "EXIT":
            sys.exit()
        print(data.decode() + "\n", end="")


def sent_msg(name, socketfd):
    while True:
        try:
            input_msg = input("\n请输入聊天内容:")
        except KeyboardInterrupt:
            input_msg = "quit"
        if input_msg == "quit":
            msg = "Q" + name
            socketfd.sendto(msg.encode(), addr_port)
            sys.exit()
        msg = "C %s %s" % (name,input_msg)  #C " + name + " " + input_msg  # c name text
        # msg = "C " + name + " " + input_msg
        # print(msg)
        socketfd.sendto(msg.encode(), addr_port)


def sign_in(socketfd):  # 进入聊天室
    while True:
        str_name = input("\ninput your name >>")
        msg = "L " + str_name
        # if not str_name:
        #     break
        socketfd.sendto(msg.encode(), addr_port)
        data, addr = socketfd.recvfrom(2048)
        if data.decode() == "ok":
            print("\n您已经进入聊天室")
            break
        else:
            print(data.decode())


if __name__ == '__main__':
    main()
