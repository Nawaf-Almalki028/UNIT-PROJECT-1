import      Functions.cli_messages          as          msg
from        rapidfuzz                       import      process

def cli_analysis(cli_command,permission = "guest"):

  if "help" in cli_command:
    cmd_help_handlers(permission)

  elif "product" in cli_command:
    
    cmd_products_handlers(permission)

  else:
    print("type (help) to see other commands")


def cmd_help_handlers(permission = "guest"):
  if permission == "administrator":
    print(msg.help_messages["administrator"])
  elif permission == "customer":
    print(msg.help_messages["customer"])
  elif permission == "guest":
    print(msg.help_messages["guest"])
  else:
    print("Something went wrong contact us!")

def cmd_products_handlers(permission = "guest"):
  print("you have these products")


def authentecation_handler(permission = "guest"):
  print("this for authentecation")


def basket_handler(permission = "guest"):
  print("this for basket")


def payment_handler(permission = "guest"):
  print("this for payment")
