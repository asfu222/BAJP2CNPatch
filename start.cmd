mitmweb -m wireguard --no-http2 -s redirect_server.py --set termlog_verbosity=warn --allow-hosts prod-clientpatch.bluearchiveyostar.com:443 --allow-hosts mitm.it:* --set stream_large_bodies=2000
