
def cli_analysis(cli_command):

  if cli_command == "help":
    print("""
    You have the following commands:
        products
        buy
        return
        accounts
        sign_in
        sign_up
        forget_password
    """)

  elif cli_command == "products":
    products_list_handler()


def products_list_handler():
  print("you have these products")


def authentecation_handler():
  print("this for authentecation")


def basket_handler():
  print("this for basket")


def payment_handler():
  print("this for payment")