import os
import logging
from aiohttp import web

import server


COMFYUI_IP_WHITELIST = [ip.strip() for ip in os.environ.get("COMFYUI_IP_WHITELIST", "").split(',')]
if not any(COMFYUI_IP_WHITELIST):
    COMFYUI_IP_WHITELIST = []
  

prompt_server = server.PromptServer.instance
app = prompt_server.app

@web.middleware
async def request_handler(request: web.Request, handler):
    ip_address = request.remote.split(':')[0]
    if ip_address not in COMFYUI_IP_WHITELIST:
        logging.warn(f'[Firewall] Incoming request from non-whitelisted IP \"{ip_address}\" was rejected.')
        raise web.HTTPForbidden()
    return await handler(request)

logging.info('[Firewall] Initializing ComfyUI Firewall...')
app.middlewares.append(request_handler)
if len(COMFYUI_IP_WHITELIST) == 0:
    logging.warn('[Firewall] No IPs were found in the COMFYUI_IP_WHITELIST environment variable. Nobody will be able to access ComfyUI!')
else:
    logging.info(f'[Firewall] The firewall is now active for {len(COMFYUI_IP_WHITELIST)} IP address(es).')
