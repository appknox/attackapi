import fcntl
import shlex
import socket
import struct
import subprocess
import sys


def get_ip(iface='wlo1'):
    ifreq = struct.pack(
        '16sH14s', iface.encode('utf-8'), socket.AF_INET, b'\x00'*14
    )
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockfd = sock.fileno()
        SIOCGIFADDR = 0x8915
        res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
    except:
        return None
    ip = struct.unpack('16sH2x4s8x', res)[2]
    return socket.inet_ntoa(ip)


def run_shell_command(cmd):
    pass
