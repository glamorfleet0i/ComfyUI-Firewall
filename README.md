# ComfyUI Firewall
A very basic firewall-like middleware that restricts access to your ComfyUI server based on a list of specified IP addresses. As this is configured as middleware, the firewall will restrict both the web UI and any API endpoints.

## Configuration
Set the following environment variables to configure the firewall:
- `COMFYUI_FIREWALL_USE_CLOUDFLARE_IP`: If set to the string "true", the firewall will use the "Cf-Connecting-Ip" header from Cloudflare to determine the user's IP address. Otherwise, the firewall will use `aiohttp`'s remote value from the request object to determine the user's IP address.
- `COMFYUI_FIREWALL_WHITELISTED_IPS`: A comma-separated list of IP addresses that are allowed to access ComfyUI. Any IP addresses specified here are in addition to `127.0.0.1` (localhost). Leave blank to only allow localhost to access your ComfyUI server.