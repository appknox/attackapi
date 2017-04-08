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


ignored_url_types = {
    'img', 'js', 'css', 'png', 'jpg', 'svg', 'gif',
}
ignored_hosts = {
    'facebook.com', 'insights.hotjar.com', 'youtube.com',
}


def can_ignore(request):
    url_type = request.path.split('.')[-1]
    host = request.host.strip('.www')
    is_ignored = url_type in ignored_url_types or host in ignored_hosts
    return is_ignored


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color_print(text, color):
    print(color + text + Colors.ENDC)
