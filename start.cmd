@echo off
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /i "IPv4"') do (
    for /f "tokens=*" %%B in ("%%A") do (
        set LOCAL_IP=%%B
        goto :done
    )
)
:done
set LOCAL_IP=%LOCAL_IP: =%
@echo on
mitmweb -m wireguard --no-http2 -s redirect_server.py --set termlog_verbosity=warn --ignore-hosts %LOCAL_IP%