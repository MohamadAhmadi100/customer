from customer.modules import terminal_log
from config import config

# Important import...please do not remove this at home
import customer.controllers.main_controller as controller

app_name = config.APP_NAME


def callback(message: dict) -> dict:
    terminal_log.action_log(message, app_name)
    terminal_log.request_log(message, app_name)
    data = message.get(app_name, {})
    if action := data.get("action"):
        body = data.get("body", {})
        try:
            func = getattr(controller, action)
            response = {str(app_name): func(**body)}
            return response
        except Exception as e:
            return {f"{app_name}": {"success": False, "status_code": 503, "error": f"{app_name}: {e}"}}
    else:
        return {f"{app_name}": {"success": False, "status_code": 501, "error": f"{app_name}: action not found"}}
