from mitmproxy import http
import requests
import socket
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

# 文件服务器
FILE_SERVER_SCHEME = 'http' # 服务器网络协议（通常是http或https）
FILE_SERVER_HOST = get_local_ip() # 服务器网址
FILE_SERVER_PORT = 8000 # 服务器端口`

# 官方资源服务器
BA_FS_HOSTS = [
'prod-clientpatch.bluearchiveyostar.com'
]

def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_host in BA_FS_HOSTS:
        file_server_url = f'http://{FILE_SERVER_HOST}:{FILE_SERVER_PORT}{flow.request.path}'
        try:
            response = requests.head(file_server_url, timeout=5)
            if response.status_code == 200:
                # 拦截官方资源服务器下载请求，并修改至上面的文件服务器网址
                flow.request.scheme = FILE_SERVER_SCHEME
                flow.request.host = FILE_SERVER_HOST
                flow.request.port = FILE_SERVER_PORT
        except requests.RequestException:
            pass