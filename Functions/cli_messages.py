from        colorama                            import          Fore
from        Functions.json_handlers             import          read_json,write_json

def menu_msg_handler(permission="guest"):
  
  data = read_json("menu_data")
  menu_msg = data[permission]
  menu_msg = menu_msg.replace("{#c}", Fore.CYAN)
  menu_msg = menu_msg.replace("{#y}", Fore.YELLOW)
  return menu_msg
