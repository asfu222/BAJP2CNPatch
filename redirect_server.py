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
FILE_SERVER_SCHEME = 'https' # 服务器网络协议（通常是http或https）
# FILE_SERVER_SCHEME = 'http' 本地服务器
FILE_SERVER_HOST = 'asfu222.github.io' # 服务器网址
# FILE_SERVER_HOST = get_local_ip() # 本地服务器
FILE_SERVER_EXTRA_PATH = '/BACNLocalizationResources/shale' # 附加路径，可不填。这里作者填作者的资源地址，可选: shale(国服), ourplay 或 beicheng 汉化包
FILE_SERVER_PORT = 443 # 服务器端口
# FILE_SERVER_PORT = 8000 # 本地服务器

# 官方资源服务器
BA_FS_HOSTS = [
'prod-clientpatch.bluearchiveyostar.com'
]

def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_host in BA_FS_HOSTS:
        new_path = flow.request.path
        if True: # 如果不知道BA版本号/服务器没有版本号，请把这个改成True。<请注意> 如果这个改成True，且作者/服务器主没更新latest资源包，会出现游戏内没有文字显现的bug （汉化落后与日服最新资源包）
            new_path = '/latest/' + '/'.join(new_path.split('/')[2:])
        new_path = FILE_SERVER_EXTRA_PATH + new_path
        file_server_url = f'{FILE_SERVER_SCHEME}://{FILE_SERVER_HOST}:{FILE_SERVER_PORT}{new_path}'
        try:
            response = requests.head(file_server_url, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                # 拦截官方资源服务器下载请求，并修改至上面的文件服务器网址
                flow.request.scheme = FILE_SERVER_SCHEME
                flow.request.host = FILE_SERVER_HOST
                flow.request.port = FILE_SERVER_PORT
                flow.request.path = new_path
        except requests.RequestException as e:
            print(e)
            pass
