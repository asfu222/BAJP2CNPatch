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
FILE_SERVER_SCHEME = 'https'
FILE_SERVER_HOST = 'cdn.bluearchive.me'
FILE_SERVER_PORT = 443
EXTRA_PATHS = ['/beicheng', '/new']  # 尝试的附加路径顺序

# 官方资源服务器
BA_FS_HOSTS = [
    'prod-clientpatch.bluearchiveyostar.com'
]

def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_host in BA_FS_HOSTS:
        original_path = flow.request.path
        if True:  # 保留版本号处理逻辑
            processed_path = '/latest/' + '/'.join(original_path.split('/')[2:])
        else:
            processed_path = original_path

        for extra_path in EXTRA_PATHS:
            current_new_path = extra_path + processed_path
            file_server_url = f'{FILE_SERVER_SCHEME}://{FILE_SERVER_HOST}:{FILE_SERVER_PORT}{current_new_path}'
            try:
                response = requests.head(file_server_url, allow_redirects=True, timeout=5)
                if response.status_code == 200:
                    flow.request.scheme = FILE_SERVER_SCHEME
                    flow.request.host = FILE_SERVER_HOST
                    flow.request.port = FILE_SERVER_PORT
                    flow.request.path = current_new_path
                    break
            except requests.RequestException as e:
                print(e)
                continue
            
