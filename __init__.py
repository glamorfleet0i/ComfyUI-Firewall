import os
import logging
from aiohttp import web

import server


SHOULD_USE_CLOUDFLARE_IP = os.environ.get("COMFYUI_FIREWALL_USE_CLOUDFLARE_IP", "false").lower() == "true"
USER_IP_WHITELIST = [ip.strip() for ip in os.environ.get("COMFYUI_FIREWALL_WHITELISTED_IPS", "").split(',')]
if not any(USER_IP_WHITELIST):
    USER_IP_WHITELIST = []
  
ALLOWED_IPS = ["127.0.0.1"]
ALLOWED_IPS.extend(USER_IP_WHITELIST)

prompt_server = server.PromptServer.instance
app = prompt_server.app

@web.middleware
async def request_handler(request: web.Request, handler):
    if SHOULD_USE_CLOUDFLARE_IP:
        ip_address = request.headers.get('Cf-Connecting-Ip')
    else:
        ip_address = request.remote.split(':')[0]
    
    if not ip_address:
        logging.warning(f'[Firewall] Could not find IP address. Rejecting request.')
        raise web.HTTPForbidden()
    
    if ip_address not in ALLOWED_IPS:
        logging.warning(f'[Firewall] Incoming request from non-whitelisted IP \"{ip_address}\" was rejected.')
        raise web.HTTPForbidden()
    
    return await handler(request)

logging.info('[Firewall] Initializing ComfyUI Firewall...')
app.middlewares.append(request_handler)
if len(USER_IP_WHITELIST) == 0:
    logging.warning('[Firewall] No IPs were found in the COMFYUI_FIREWALL_WHITELISTED_IPS environment variable. Nobody outside of localhost will be able to access ComfyUI!')
else:
    logging.info(f'[Firewall] The firewall is now active for {len(USER_IP_WHITELIST)} IP address(es).')
    
    header_source = "the Cloudflare header \"Cf-Connecting-Ip\"" if SHOULD_USE_CLOUDFLARE_IP else "the aiohttp remote"
    logging.info(f"[Firewall] Using {header_source} to determine user IP addresses.")

NODE_CLASS_MAPPINGS = {}
