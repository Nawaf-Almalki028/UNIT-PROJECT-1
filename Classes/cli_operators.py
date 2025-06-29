from        Functions.cli_messages          import      menu_msg_handler
from        Functions.similar_words         import      similar_words_handler
from        Functions.json_handlers         import      read_json,write_json
from        hashlib                         import      sha256
from        colorama                        import      Fore

class CliHandler():
  def __init__(self, command_entered, permission='guest', account_id="0"):

    self.command_entered = command_entered
    self.__permission = permission
    self.account_id = account_id
    self.cart = {}

    self.__commands = {
      "guest":["help","signin","signup","products","cart"],

      "customer":["help","dashboard","products","cart","mails",
                  "email","orders","support","logs","logout"],
                  
      "administrator":["help","dashboard","products","cart","mails",
                  "email","users","tickets","logs","logout"]
    }

  def cli_analysis(self):

    if "help" in self.command_entered:
      self.cmd_help_handlers()
      
    elif "signin" == self.command_entered and "signin" in self.__commands[self.__permission]:
      if self.auth_handler("signin"):
        print(f"{Fore.RED} AuthSystem:{Fore.GREEN} signin success!, welcome {Fore.YELLOW + self.username}")
      else:
        print(f"{Fore.RED} AuthSystem: signin failed!")
      
    elif "signup" == self.command_entered and "signup" in self.__commands[self.__permission]:
      if self.auth_handler("signup"):
        print(f"{Fore.RED} AuthSystem:{Fore.GREEN} signup success!, welcome {Fore.YELLOW + self.username}, please signin!")
      else:
        print(f"{Fore.RED} AuthSystem: signup failed!")
      
    elif "logout" == self.command_entered and "logout" in self.__commands[self.__permission]:
      self.auth_handler("logout")

    elif "products" in self.command_entered:
      self.cmd_products_handlers()

    elif "cart" == self.command_entered and "cart" in self.__commands[self.__permission]:
      print(f"{Fore.RED}type {Fore.WHITE}cart {Fore.CYAN}(add,remove,show,pay)")

    elif "cart show" == self.command_entered and "cart" in self.__commands[self.__permission]:
      self.cmd_cart_handlers("show")

    elif "cart add" == self.command_entered and "cart" in self.__commands[self.__permission]:
      self.cmd_cart_handlers("add")

    elif "cart remove" == self.command_entered and "cart" in self.__commands[self.__permission]:
      self.cmd_cart_handlers("remove")

    elif "cart pay" == self.command_entered and "cart" in self.__commands[self.__permission]:
      self.cmd_cart_handlers("pay")

    elif "dashboard" == self.command_entered and "cart" in self.__commands[self.__permission]:
      self.cmd_cart_handlers("pay")


    else:
      similar_word_process = similar_words_handler(self.command_entered,self.__commands[self.__permission])
      if similar_word_process[0] and similar_word_process[2] > 50:
        print(f"{Fore.BLUE}Assistant{Fore.CYAN}: do you mean {Fore.GREEN}{similar_word_process[1]} {Fore.CYAN}command?")
      else:
        print(f"{Fore.RED}there isn't any command like that")
        print(f"{Fore.RED}type {Fore.WHITE}(help) {Fore.RED}to see other commands")


  def cmd_cart_handlers(self,option):
    if option == 'show':
      all_cost = 0
      print(Fore.GREEN + f"You have this items: ")
      for category, items in self.cart.items():
        for item_name,info in items.items():
          print(f"🛒 - {category} / {item_name}: Quantity: {info['quantity']} Price ${info['price']}")
          all_cost = all_cost + (info['price'] * info['quantity'])
      print(Fore.CYAN + f"Total Price: {round(all_cost,2)}")

    elif option == 'add':
      cart_item = input(f"{Fore.GREEN}CartSystem: Enter item name to add: ")
      cart_item = cart_item.upper()
      items = read_json("products")
      categories = ["VPS","VDS","GAMESERVER"]
      for category in categories:
        if category in items:
          for item_name, item_info in items[category].items():
            if cart_item == item_name:
              if category not in self.cart:
                self.cart[category] = {}
              if item_name in self.cart[category]:
                self.cart[category][item_name]["quantity"] += 1
              else:
                self.cart[category][item_name] = {"price":item_info["price"],"quantity":1}

    elif option == 'remove':
      cart_item = input(f"{Fore.GREEN}CartSystem: Enter item name to remove: ")
      cart_item = cart_item.upper()
      for category in list(self.cart.keys()):
        if cart_item in self.cart[category]:
          if self.cart[category][cart_item]["quantity"] > 1:
            self.cart[category][cart_item]["quantity"] -= 1
          else:
            del self.cart[category][cart_item]

    elif option == 'pay':
      if self.__permission == 'guest':
        print(Fore.RED + "You need to signin first!")
      else:
        print(f"Payment Methods: \nVISA\nPayPal\nMada")
        servers = read_json("servers")
        last_server_number = 0
        if self.__user_id in servers["VServers"]:
            for server_id in servers["VServers"][self.__user_id]:
                last_server_number = int(server_id[-4:])
        last_server_number += 1
        new_server_id = f"VServer#{str(last_server_number)}"

        for type_server in self.cart:
          for value in self.cart[type_server]:
            print(value)
        # print(self.cart)

        # servers["VServers"][self.__user_id] = {
        #   new_server_id:{
        #     "type:"
        #   }
        # }
        
    # data["users"][user_id] = {
    #     "username":username,
    #     "firstname":firstname,
    #     "lastname":lastname,
    #     'permission':'customer',
    #     'date_of_create':1,
    #     "password":password1,
    #     'email':email}
    # "VServers":{
    #   "id_HT2":{
    #     "VServer#001": {
    #       "type": "VPS-S",
    #       "location": "EU",
    #       "core": 2,
    #       "threads": 4,
    #       "memory": 4,
    #       "storage":  50,
    #       "ip_addresses": 1,
    #       "date": "0",
    #       "status": true,
    #       "price": 5.99
    #     }
    #   }
    # }

  def cmd_help_handlers(self):

    if self.__permission == "administrator":
      print(menu_msg_handler("administrator"))

    elif self.__permission == "customer":
      print(menu_msg_handler("customer"))

    elif self.__permission == "guest":
      print(menu_msg_handler("guest"))

    else:
      print("Something went wrong contact us!")

  def cmd_products_handlers(self):
    products_data = read_json("products")
    if "vps" in self.command_entered:
      for vps in products_data["VPS"]:
        print(f"{Fore.CYAN}Plan: {vps}: Core: {products_data['VPS'][vps]['core']}, Memory: {products_data['VPS'][vps]['memory']}, Storage: {products_data['VPS'][vps]['storage']}GB, IP Address: {products_data['VPS'][vps]['ip_address']}, Price: ${products_data['VPS'][vps]['price']}.")
    elif "vds" in self.command_entered:
      for vds in products_data["VDS"]:
        print(f"{Fore.CYAN}Plan: {vds}: Core: {products_data['VDS'][vds]['core']}, Memory: {products_data['VDS'][vds]['memory']}, Storage: {products_data['VDS'][vds]['storage']}GB, IP Address: {products_data['VDS'][vds]['ip_address']}, Price: ${products_data['VDS'][vds]['price']}.")
    elif "gameserver" in self.command_entered:
      for gameserver in products_data["GameServer"]:
        print(f"{Fore.CYAN}Plan: {gameserver}: Players: {products_data['GameServer'][gameserver]['players']} Memory: {products_data['GameServer'][gameserver]['memory']}, Storage: {products_data['GameServer'][gameserver]['storage']}GB, Price: ${products_data['GameServer'][gameserver]['price']}.")

      
      game_server = products_data['GameServer']
    else:
      print(f"{Fore.RED}type {Fore.WHITE}products {Fore.CYAN}(vps,vds,gameserver)")


  def auth_hash_password(self,password_to_hash):
    return sha256(password_to_hash.encode()).hexdigest()
    

  def auth_handler(self,authentecation_option):
    data = read_json("accounts")
    if authentecation_option == "signin":
      entered_username = input(f"{Fore.RED} AuthSystem: Enter your username:{Fore.YELLOW} ")
      entered_password = input(f"{Fore.RED} AuthSystem: Enter your password:{Fore.YELLOW} ")
      hashed_password = self.auth_hash_password(entered_password)
      
      entered_username = entered_username.lower()

      for id in data['users']:
        if data['users'][id]['username'] == entered_username and data['users'][id]['password'] == hashed_password:
          self.username = entered_username
          self.firstname = data['users'][id]['firstname']
          self.lastname = data['users'][id]['lastname']
          self.__password = hashed_password
          self.__permission = data['users'][id]['permission']
          self.__email = data['users'][id]['email']
          self.__user_id = id
          self.date_of_create = data['users'][id]['date_of_create']
          return True
        else:
          continue

    elif authentecation_option == "signup":
      username = input(f"{Fore.RED} AuthSystem: Enter your username:{Fore.YELLOW} ")
      password1 = input(f"{Fore.RED} AuthSystem: Enter your password:{Fore.YELLOW} ")
      password2 = input(f"{Fore.RED} AuthSystem: Repeat your password:{Fore.YELLOW} ")

      if len(username) > 3:
        if username and username[0].isalpha():
          if password1 == password2 and len(password1) > 4:
            firstname = input(f"{Fore.RED} AuthSystem: Enter your firstname:{Fore.YELLOW} ")
            lastname = input(f"{Fore.RED} AuthSystem: Enter your lastname:{Fore.YELLOW} ")
            email = input(f"{Fore.RED} AuthSystem: Enter your email:{Fore.YELLOW} ")

            if email.endswith("@gmail.com") or email.endswith("@hotmail.com"):
              pass
            else:
              print(f"{Fore.RED} AuthSystem: we only support mails from gmail and hotmail")
              return False

            password1 = self.auth_hash_password(password1)

            for index,id in enumerate(data['users']):
              user_id = f'id_HT{index+1}'

            
            data["users"][user_id] = {
                "username":username,
                "firstname":firstname,
                "lastname":lastname,
                'permission':'customer',
                'date_of_create':1,
                "password":password1,
                'email':email}
            
            self.username = username
            
            write_json("accounts",data)
            return True
          else:
            print(f"{Fore.RED} AuthSystem: password dosen't match or two short!")
        else:
          print(f"{Fore.RED} AuthSystem: username should start with chars only")
      else:
        print(f"{Fore.RED} AuthSystem: username is two short need to be at least 4 chars")


    elif authentecation_option == "logout":
      sure_confirm = input(f"{Fore.RED} AuthSystem: Are you sure! (y:yes n:no):{Fore.YELLOW} ")
      if sure_confirm == 'y':
        self.username = None
        self.firstname = None
        self.lastname = None
        self.__password = None
        self.__permission = 'guest'
        self.__email = None
        self.__user_id = None
        self.date_of_create = None
        self.cart = {}
      else:
        print(f"{Fore.RED} AuthSystem:  You cancel it.")



  def basket_handler(self):
    print("this for basket")


  def payment_handler(self):
    print("this for payment")
