from customer.modules import terminal_log
from config import config

# Important imports don't remove
from customer.controllers.router_auth import *
from customer.controllers.router_profile import *
from customer.controllers.router_register import *
from customer.controllers.router_portal import *

response = {}
app_name = config.APP_NAME


def callback(message: dict) -> dict:
    terminal_log.action_log(message, app_name)
    terminal_log.request_log(message, app_name)
    data = message.get(app_name, {})
    if action := data.get("action"):
        body = data.get("body", {})
        try:
            exec(f"global response; response['{app_name}'] = {action}(**{body})")
            return response
        except Exception as e:
            return {f"{app_name}": {"success": False, "status_code": 503, "error": f"{app_name}: {e}"}}
    else:
        return {f"{app_name}": {"success": False, "status_code": 501, "error": f"{app_name}: action not found"}}
