import fcntl
import socket
import struct


IGNORED_URL_TYPES = {
    'img', 'js', 'css', 'png', 'jpg', 'svg', 'gif', 'ico', 'otf', 'woff',
    'woff2',
}

IGNORED_HOSTS = {
    'facebook.com', 'insights.hotjar.com', 'youtube.com',
    'gstatic.com', 'decide.mixpanel.com',
    'android.clients.google.com',
}


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


def can_ignore(request):
    path_without_query = request.path.split('?')[0]
    url_type = path_without_query.split('.')[-1].lower()
    host = request.host.strip('.www')
    is_ignored = url_type in IGNORED_URL_TYPES or host in IGNORED_HOSTS
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
