from customer.modules import terminal_log
from config import config
import customer.controllers as controller
from customer.helper.telegram_message import exception_handler

app_name = config.APP_NAME


def callback(message: dict) -> dict:
    terminal_log.action_log(message, app_name)
    terminal_log.request_log(message, app_name)
    data = message.get(app_name, {})
    if action := data.get("action"):
        body = data.get("body", {})
        try:
            func = getattr(controller, action)
            return {str(app_name): func(**body)}
        except Exception as e:
            exception_handler()
            return {f"{app_name}": {"success": False, "status_code": 503, "error": f"{app_name}: {e}"}}

    else:
        return {f"{app_name}": {"success": False, "status_code": 501, "error": f"{app_name}: action not found"}}
