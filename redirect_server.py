import os
import json
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

# CDN file server info.
FILE_SERVER_SCHEME = 'https'
FILE_SERVER_HOST = 'cdn.bluearchive.me'
FILE_SERVER_PORT = 443

# List of extra server names (no leading slash)
SERVERS = ['db-example', 'commonpng', 'scenariovoice']

# Official resource servers.
BA_FS_HOSTS = [
    'prod-clientpatch.bluearchiveyostar.com'
]

# Cache directory for downloaded catalogs.
CACHE_DIR = "./cache"

def load_catalog(server: str):
    """
    Loads the catalog for the given server.
    If the catalog file exists in CACHE_DIR, read it;
    otherwise download from the CDN and save it.
    The catalog is expected to be a JSON list of allowed subpaths.
    """
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    cache_file = os.path.join(CACHE_DIR, f"{server}_catalog.json")
    # Try loading from the cache.
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                catalog = json.load(f)
                return catalog
        except Exception as e:
            print(f"Error loading cached catalog for {server}: {e}")
    # If cache is missing or broken, download the catalog.
    url = f"{FILE_SERVER_SCHEME}://{FILE_SERVER_HOST}:{FILE_SERVER_PORT}/{server}/latest/catalog.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            catalog = response.json()
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(catalog, f)
            return catalog
        else:
            print(f"Catalog for {server} returned status {response.status_code}")
    except requests.RequestException as e:
        print(f"Error downloading catalog for {server}: {e}")
    return None

def request(flow: http.HTTPFlow) -> None:
    # Check if the request is to one of the official BA resource servers.
    if flow.request.pretty_host in BA_FS_HOSTS:
        original_path = flow.request.path
        # For consistency with prior logic, remove the first two segments (which might include a version).
        # e.g. if original_path is "/v1/some/path/file.png", processed_path becomes "some/path/file.png"
        processed_path = '/'.join(original_path.split('/')[2:])
        
        # Iterate through each extra server.
        for server in SERVERS:
            catalog = load_catalog(server)
            if catalog is None:
                continue
            # Check if the processed path (or a subpath of it) is allowed.
            # This example uses a simple membership test – adjust as needed.
            if processed_path in catalog:
                # Rewrite the flow’s request to point to the extra server’s directory.
                # The new path is constructed as: /{server}/latest/{processed_path}
                new_path = f"/{server}/latest/{processed_path}"
                flow.request.scheme = FILE_SERVER_SCHEME
                flow.request.host = FILE_SERVER_HOST
                flow.request.port = FILE_SERVER_PORT
                flow.request.path = new_path
                print(f"Redirecting request to: {FILE_SERVER_SCHEME}://{FILE_SERVER_HOST}{new_path}")
                break
