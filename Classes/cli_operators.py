from        Functions.cli_messages          import      menu_msg_handler
from        Functions.similar_words         import      similar_words_handler
from        Functions.json_handlers         import      read_json,write_json
from        datetime                        import      datetime
from        hashlib                         import      sha256
from        colorama                        import      Fore
from        maskpass                        import      askpass

class CliHandler():
  def __init__(self, command_entered, permission='guest', account_id="0",balance = 0):

    self.command_entered = command_entered
    self.__permission = permission
    self.__account_id = account_id
    self.__balance = balance
    self.cart = {}

    self.__commands = {
      "guest": [
        "help", "signin", "signup",
        "products", "products vps", "products vds", "products gameserver",
        "cart", "cart show", "cart add", "cart remove", "cart pay"
      ],

      "customer": [
        "help","balance","balance show","balance add",
        "dashboard", "dashboard show", "dashboard services", "dashboard start", "dashboard stop",
        "products", "products vps", "products vds", "products gameserver",
        "cart", "cart show", "cart add", "cart remove", "cart pay",
        "tickets", "tickets create", "tickets show",
        "logs",
        "logout"
      ],

      "administrator": [
        "help", "admincmd", "admincmd ban", "admincmd unban","balance","balance show","balance add",
        "dashboard", "dashboard show", "dashboard services", "dashboard start", "dashboard stop",
        "products", "products vps", "products vds", "products gameserver",
        "cart", "cart show", "cart add", "cart remove", "cart pay",
        "users", "users promote", "users demote",
        "logs",
        "tickets", "tickets show", "tickets reply", "tickets close",
        "logout"
      ]
    }

  def cli_analysis(self):

    self.cmd_logs_saves(f"You typed this command: {self.command_entered}")

    match self.command_entered:
      case _ if "help" in self.command_entered:
          self.cmd_help_handlers()

      case "signin" if "signin" in self.__commands[self.__permission]:
          if self.auth_handler("signin"):
              print(f"{Fore.RED} AuthSystem:{Fore.GREEN} signin success!, welcome {Fore.YELLOW + self.username}")
          else:
              print(f"{Fore.RED} AuthSystem: signin failed!")

      case "signup" if "signup" in self.__commands[self.__permission]:
          if self.auth_handler("signup"):
              print(f"{Fore.RED} AuthSystem:{Fore.GREEN} signup success!, welcome {Fore.YELLOW + self.username}, please signin!")
          else:
              print(f"{Fore.RED} AuthSystem: signup failed!")

      case "logout" if "logout" in self.__commands[self.__permission]:
          self.auth_handler("logout")

      case _ if "products" in self.command_entered:
          self.cmd_products_handlers()

      case "cart" if "cart" in self.__commands[self.__permission]:
          print(f"{Fore.RED}type {Fore.WHITE}cart {Fore.CYAN}(add,remove,show,pay)")

      case "cart show" if "cart" in self.__commands[self.__permission]:
          self.cmd_cart_handlers("show")

      case "cart add" if "cart" in self.__commands[self.__permission]:
          self.cmd_cart_handlers("add")

      case "cart remove" if "cart" in self.__commands[self.__permission]:
          self.cmd_cart_handlers("remove")

      case "cart pay" if "cart" in self.__commands[self.__permission]:
          self.cmd_cart_handlers("pay")

      case "dashboard" if "dashboard" in self.__commands[self.__permission]:
          print(f"{Fore.RED}type {Fore.WHITE}dashboard {Fore.CYAN}(show,services,start,stop)")

      case "dashboard show" if "dashboard" in self.__commands[self.__permission]:
          self.cmd_dashboard_handlers("show")

      case "dashboard services" if "dashboard" in self.__commands[self.__permission]:
          self.cmd_dashboard_handlers("services")

      case "dashboard start" if "dashboard" in self.__commands[self.__permission]:
          self.cmd_dashboard_handlers("start")

      case "dashboard stop" if "dashboard" in self.__commands[self.__permission]:
          self.cmd_dashboard_handlers("stop")

      case "dashboard refund" if "dashboard" in self.__commands[self.__permission]:
          self.cmd_dashboard_handlers("refund")

      case "admincmd" if "admincmd" in self.__commands[self.__permission]:
          print(f"{Fore.RED}type {Fore.WHITE}admincmd {Fore.CYAN}(ban,unban)")

      case "admincmd ban" if "admincmd" in self.__commands[self.__permission]:
          self.cmd_admincmd_handlers("ban")

      case "admincmd unban" if "admincmd" in self.__commands[self.__permission]:
          self.cmd_admincmd_handlers("unban")

      case "balance" if "balance" in self.__commands[self.__permission]:
          print(f"{Fore.RED}type {Fore.WHITE}balance {Fore.CYAN}(show,add)")

      case "balance add" if "balance" in self.__commands[self.__permission]:
          self.cmd_balance_handlers("add")

      case "balance show" if "balance" in self.__commands[self.__permission]:
          self.cmd_balance_handlers("show")

      case "users" if "users" in self.__commands[self.__permission]:
          print(f"{Fore.RED}type {Fore.WHITE}users {Fore.CYAN}(promote,demote)")

      case "users promote" if "users" in self.__commands[self.__permission]:
          self.cmd_users_handlers("promote")

      case "users demote" if "users" in self.__commands[self.__permission]:
          self.cmd_users_handlers("demote")

      case "logs" if "logs" in self.__commands[self.__permission]:
          self.cmd_logs_handlers()

      case "tickets" if "tickets" in self.__commands[self.__permission]:
          print(f"{Fore.RED}type {Fore.WHITE}tickets {Fore.CYAN}(create,show)")

      case "tickets create" if "tickets" in self.__commands[self.__permission]:
          self.cmd_ticket_handlers("create")

      case "tickets show" if "tickets" in self.__commands[self.__permission]:
          self.cmd_ticket_handlers("show")

      case "tickets reply" if "tickets reply" in self.__commands[self.__permission]:
          self.cmd_ticket_handlers("reply")

      case _:
          similar_word_process = similar_words_handler(self.command_entered, self.__commands[self.__permission])
          if similar_word_process[0] and similar_word_process[2] > 50:
              print(f"{Fore.BLUE}Assistant{Fore.CYAN}: do you mean {Fore.GREEN}{similar_word_process[1]} {Fore.CYAN}command?")
          else:
              print(f"{Fore.RED}there isn't any command like that")
              print(f"{Fore.RED}type {Fore.WHITE}(help) {Fore.RED}to see other commands")

  def cmd_ticket_handlers(self,option):
    read_tickets = read_json("tickets")
    try:
        if option == "create":
            title = input("Enter the ticket title: ")
            message = input("Enter the ticket message: ")
            if self.__account_id not in read_tickets:
                read_tickets[self.__account_id] = {}
            ticket_id = f"ticket_{len(read_tickets[self.__account_id]) + 1}"
            read_tickets[self.__account_id][ticket_id] = {
                "title": title,
                "message": message,
                "reply": None
            }
            write_json("tickets", read_tickets)
            print("Ticket created.")
        elif option == "show" and self.__permission == "customer":
            if self.__account_id not in read_tickets:
                print("No tickets found.")
            else:
                for ticket_id, data in read_tickets[self.__account_id].items():
                    print(f"ID: {ticket_id}")
                    print(f"Title: {data['title']}")
                    print(f"Message: {data['message']}")
                    print(f"Reply: {data['reply'] or 'No reply'}\n")
        elif option == "show" and self.__permission == "administrator":
           for account_id,info in read_tickets.items():
              for ticket_id in info:
                print(f"{Fore.WHITE}Account ID: {account_id} , {Fore.CYAN}Ticket ID: {ticket_id} {Fore.GREEN}, Title: {read_tickets[account_id][ticket_id]['title']}, {Fore.YELLOW}Message: {read_tickets[account_id][ticket_id]['message']}, {Fore.RED}Reply: {read_tickets[account_id][ticket_id]['reply']}")
              # for ticket_id in read_tickets[account_id].items():
                # print(f"Account ID: {account_id}, Ticket ID: {ticket_id}, Title: {data}")
                # for ticket_id, data in read_tickets[self.__account_id].items():
                #     print(f"ID: {ticket_id}")
                #     print(f"Title: {data['title']}")
                #     print(f"Message: {data['message']}")
                #     print(f"Reply: {data['reply'] or 'No reply'}\n")
        elif option == "reply":
            user_id = input("enter the user id: ")
            if user_id not in read_tickets:
                print("No tickets for that user.")
            else:
                for ticket_id in read_tickets[user_id]:
                    print(f"- {ticket_id}: {read_tickets[user_id][ticket_id]['title']}")
                ticket_id = input("enter the ticket id: ")
                if ticket_id in read_tickets[user_id]:
                    reply = input("enter the reply: ")
                    read_tickets[user_id][ticket_id]["reply"] = reply
                    write_json("tickets", read_tickets)
                    print("reply done.")
                else:
                    print("wrong ticket id, or not found.")

        else:
            print("Invalid option. Use create, show, or reply.")

    except Exception as ex:
        print(f"Tickets Error: {ex}")
 
  def cmd_logs_saves(self,log):
    try:
      if self.__permission != "guest":
        date_now = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
        log_file = read_json("logs")
        if self.__account_id not in log_file:
           log_file[self.__account_id] = {}
        log_file[self.__account_id][date_now] = log
        write_json("logs", log_file)
      else:
         pass
    except Exception as ex:
      print(f"{Fore.RED}Error saving log: {ex}")

  def cmd_logs_handlers(self):
    logs_file = read_json("logs")
    if self.__permission != "administrator":
      for date,log in logs_file[self.__account_id].items():
         print(f"{Fore.YELLOW}#Log: {Fore.WHITE}Date: {date}, {Fore.RED}Comment: {log}.")
    else:
      entered_id = input("Enter user id: ")
      if entered_id in logs_file:
        for date,log in logs_file[entered_id].items():
          print(f"{Fore.YELLOW}#Log: {Fore.WHITE}Date: {date}, {Fore.RED}Comment: {log}.")
      else:
         print("Entered id not found!")
  
  def cmd_users_handlers(self,option):
     users_data = read_json("accounts")
     if option == "promote":
        user_id = input("Enter user id to promote: ")
        if user_id in users_data["users"]:
          users_data["users"][user_id]["permission"] = 'administrator'
          write_json("accounts", users_data)
          print("+++ User has Promoted +++")
          self.cmd_logs_saves(f"You promote {user_id}")
        else:
           print("there is no user like that")
     elif option == "demote":
        user_id = input("Enter user id to demote: ")
        if user_id in users_data["users"]:
          users_data["users"][user_id]["permission"] = 'customer'
          write_json("accounts", users_data)
          print("--- User has Demoted ---")
          self.cmd_logs_saves(f"You demote {user_id}")
        else:
           print("there is no user like that")
  
  def cmd_balance_handlers(self,option):
    try:
      read_account_data = read_json("accounts")
      yourbalance = read_account_data["users"][self.__account_id]["balance"]
      self.__balance = yourbalance
      if option == "show":
        self.cmd_logs_saves("You ask for showing your balance")
        print("========================")
        print(f"{Fore.GREEN} Your balance is: ${self.__balance}")
        print("========================")
      elif option == "add":
        self.cmd_logs_saves("You ask for add amount to your wallet")
        try:
          enter_balance_to_add = float(input(f"{Fore.YELLOW}Enter the amount: {Fore.GREEN}$"))
        except Exception as ex:
          print(f"{Fore.RED} Wrong Input! Error {ex} ")
        read_account_data["users"][self.__account_id]["balance"] += enter_balance_to_add
        write_json("accounts",read_account_data)
    except Exception as ex:
       print(f"{Fore.RED}Account data Error: {ex}")

  def cmd_admincmd_handlers(self,option):
    try:
      read_account = read_json("accounts")

      enter_userid = input(f"{Fore.RED}AdminCMD: Enter user_id: ")

      if option == "ban":
        reason = input(f"{Fore.RED}AdminCMD: Enter the reason: ")
        if enter_userid not in read_account["Blacklist"]:
          read_account["Blacklist"][enter_userid] = {
            "reason":reason
          }
          write_json("accounts",read_account)
      if option == "unban":
        if enter_userid in read_account["Blacklist"]:
          del read_account["Blacklist"][enter_userid]
          write_json("accounts",read_account)
    except Exception as ex:
       print(f"{Fore.RED}Admincmd data Error: {ex}")

  def cmd_dashboard_handlers(self,option):
    try:
      account_data = read_json("accounts")
      server_data = read_json("servers")
      if option == "show":
        print(f"""
  =============================
    {self.__permission} DASHBOARD
  =============================
  {Fore.CYAN}Welcome,  {Fore.WHITE}{self.username}
  {Fore.CYAN}Your ID:  {Fore.WHITE}{self.__account_id}
  {Fore.CYAN}Member since,  {Fore.WHITE}{self.date_of_create}
  {Fore.CYAN}Your Full Name: {Fore.WHITE}{account_data["users"][self.__account_id]["firstname"]}, {account_data["users"][self.__account_id]["lastname"]}
  {Fore.CYAN}Your Permission: {Fore.WHITE}{self.__permission}
  {Fore.CYAN}Your Email: {Fore.WHITE}{self.__email}
  {Fore.CYAN}Your Balance: {Fore.GREEN}${self.__balance}
  """
  )
      elif option == "services":
        if self.__account_id in server_data["VServers"]:
          for service in server_data["VServers"][self.__account_id]:
            data_short = server_data["VServers"][self.__account_id][service]
            status = "Stopped"
            print()
            if data_short['status']:
              status = 'Running'
            print(f"{service} Type: {data_short['type']}, Location {data_short['location']}, Status: {status}")
        else:
          print("you dont have services!")
      elif option == "start":
        server_id = input("Enter server id to start it: ")
        server_key = f"VServer#{server_id}"
        if server_key in server_data["VServers"][self.__account_id]:
            server_data["VServers"][self.__account_id][server_key]["status"] = True
            write_json("servers",server_data)
            print("Server is running now!")
        else:
          print("No server with this id")
      elif option == "stop":
        server_id = input("Enter server id to stop it: ")
        server_key = f"VServer#{server_id}"
        if server_key in server_data["VServers"][self.__account_id]:
            server_data["VServers"][self.__account_id][server_key]["status"] = False
            write_json("servers",server_data)
            print("Server is stopped now!")
        else:
          print("No server with this id")
    except Exception as ex:
       print(f"{Fore.RED}Dashboard Error: {ex}")
          

  def cmd_get_cart_cost(self):
    try:
      all_cost = 0
      for category, items in self.cart.items():
          for item_name,info in items.items():
            all_cost += (info['price'] * info['quantity'])
      return round(all_cost,2)
    except Exception as ex:
       print(f"{Fore.RED}Cart cost Error: {ex}")

  def cmd_cart_handlers(self,option):
    try:
      Servers = read_json("servers")
      if option == 'show':
        print(Fore.GREEN + f"You have this items: ")
        for category, items in self.cart.items():
          for item_name,info in items.items():
            print(f"🛒 - {category} / {item_name}: Quantity: {info['quantity']} Price ${info['price']}")
        print(Fore.CYAN + f"Total Price: ${self.cmd_get_cart_cost()}")
        print("==================================")
        print(Fore.GREEN + f"Your Balance ${self.__balance}")
        print("==================================")
        self.cmd_logs_saves("You showed your cart")

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
                  self.cmd_logs_saves("You added product from the cart")
                else:
                  self.cart[category][item_name] = {"price":item_info["price"],"quantity":1}

      elif option == 'remove':
        cart_item = input(f"{Fore.GREEN}CartSystem: Enter item name to remove: ")
        cart_item = cart_item.upper()
        for category in list(self.cart.keys()):
          if cart_item in self.cart[category]:
            if self.cart[category][cart_item]["quantity"] > 1:
              self.cart[category][cart_item]["quantity"] -= 1
              self.cmd_logs_saves("You remove product from the cart")
            else:
              del self.cart[category][cart_item]

      elif option == 'pay':
        if self.__permission == 'guest':
          print(Fore.RED + "You need to signin first!")
        else:
          if self.__balance >= self.cmd_get_cart_cost():
            servers = read_json("servers")
            products = read_json("products")
            last_server_number = 1
            if self.__account_id not in servers["VServers"]:
              servers["VServers"][self.__account_id] = {}
            try:
              for server_id in servers["VServers"][self.__account_id]:
                last_server_number = int(server_id[-4:])
            except:
              last_server_number = 1000
            date_now = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
            for product_name,product_info in self.cart.items():
              for name,info in product_info.items():
                for i in range(info["quantity"]):
                  last_server_number += 1
                  if product_name != "GAMESERVER":
                    for dedicated in servers["Dedicateds"]:
                      if (
                          servers["Dedicateds"][dedicated]["core"] > products[product_name][name]["core"] 
                          and servers["Dedicateds"][dedicated]["memory"] > products[product_name][name]["memory"] 
                          and servers["Dedicateds"][dedicated]["storage"] > products[product_name][name]["storage"]
                          and servers["Dedicateds"][dedicated]["ip_addresses"] > products[product_name][name]["ip_address"]
                          ):
                        servers["VServers"][self.__account_id][f"VServer#{last_server_number}"] = {
                          "type": name,
                          "location": servers["Dedicateds"][dedicated]["location"],
                          "core": products[product_name][name]["core"],
                          "memory": products[product_name][name]["memory"],
                          "storage": products[product_name][name]["storage"],
                          "ip_addresses": products[product_name][name]["ip_address"],
                          "date": date_now,
                          "status": True,
                          "price": products[product_name][name]["price"]
                        }
                        servers["Dedicateds"][dedicated]["core"] -= products[product_name][name]["core"] 
                        servers["Dedicateds"][dedicated]["memory"] -= products[product_name][name]["memory"] 
                        servers["Dedicateds"][dedicated]["storage"] -= products[product_name][name]["storage"]
                        servers["Dedicateds"][dedicated]["ip_addresses"] -= products[product_name][name]["ip_address"]

                        self.cmd_logs_saves("You bought gameserver")
                      else:
                        print("There is no space on the server!")
                  else:
                    servers["VServers"][self.__account_id][f"VServer#{last_server_number}"] = {
                      "type": name,
                      "location": "EU",
                      "players": products[product_name][name]["players"],
                      "memory": products[product_name][name]["memory"],
                      "storage": products[product_name][name]["storage"],
                      "date": date_now,
                      "status": True,
                      "price": products[product_name][name]["price"]
                    }
                    self.cmd_logs_saves("You bought virtual server")
            
            read_account_data = read_json("accounts")
            read_account_data["users"][self.__account_id]["balance"] -= self.cmd_get_cart_cost()
            new_balance = read_account_data["users"][self.__account_id]["balance"]
            self.cart = {}
            self.__balance = new_balance
            write_json("accounts",read_account_data)
            write_json("servers",servers)
          else:
            print(Fore.RED + "You dont have this amount!")
    except Exception as ex:
       print(f"{Fore.RED}Cart Handler Error: {ex}")

  def cmd_help_handlers(self):
    try:
      if self.__permission == "administrator":
        print(menu_msg_handler("administrator"))

      elif self.__permission == "customer":
        print(menu_msg_handler("customer"))

      elif self.__permission == "guest":
        print(menu_msg_handler("guest"))

      else:
        print("Something went wrong contact us!")
    except Exception as ex:
       print(f"{Fore.RED}CMD Help Error: {ex}")

  def cmd_products_handlers(self):
    try:
      products_data = read_json("products")
      if "vps" in self.command_entered:
        self.cmd_logs_saves("You visit the vps products")
        for vps in products_data["VPS"]:
          print(f"{Fore.CYAN}Plan: {vps}: Core: {products_data['VPS'][vps]['core']}, Memory: {products_data['VPS'][vps]['memory']}, Storage: {products_data['VPS'][vps]['storage']}GB, IP Address: {products_data['VPS'][vps]['ip_address']}, Price: ${products_data['VPS'][vps]['price']}.")
      elif "vds" in self.command_entered:
        for vds in products_data["VDS"]:
          print(f"{Fore.CYAN}Plan: {vds}: Core: {products_data['VDS'][vds]['core']}, Memory: {products_data['VDS'][vds]['memory']}, Storage: {products_data['VDS'][vds]['storage']}GB, IP Address: {products_data['VDS'][vds]['ip_address']}, Price: ${products_data['VDS'][vds]['price']}.")
          self.cmd_logs_saves("You visit the vds products")
      elif "gameserver" in self.command_entered:
        for gameserver in products_data["GAMESERVER"]:
          print(f"{Fore.CYAN}Plan: {gameserver}: Players: {products_data['GAMESERVER'][gameserver]['players']} Memory: {products_data['GAMESERVER'][gameserver]['memory']}, Storage: {products_data['GAMESERVER'][gameserver]['storage']}GB, Price: ${products_data['GAMESERVER'][gameserver]['price']}.")
          self.cmd_logs_saves("You visit the gameserver products")

      else:
        print(f"{Fore.RED}type {Fore.WHITE}products {Fore.CYAN}(vps,vds,gameserver)")
    except Exception as ex:
       print(f"{Fore.RED}Products Handler Error: {ex}")

  def auth_hash_password(self,password_to_hash):
    return sha256(password_to_hash.encode()).hexdigest()
    

  def auth_handler(self,authentecation_option):
    try:
      data = read_json("accounts")
      if authentecation_option == "signin":
        entered_username = input(f"{Fore.RED} AuthSystem: Enter your username:{Fore.YELLOW} ")
        entered_password = askpass(f"{Fore.RED} AuthSystem: Enter your password:{Fore.YELLOW} ")
        hashed_password = self.auth_hash_password(entered_password)
        
        entered_username = entered_username.lower()

        for id in data['users']:
          if data['users'][id]['username'] == entered_username and data['users'][id]['password'] == hashed_password:
            if id in data["Blacklist"]:
              reason = data["Blacklist"][id]["reason"]
              print(f"{Fore.RED} AuthSystem: You are Banned: Reason: {Fore.WHITE + reason}")
            elif id not in data["Blacklist"]:
              self.username = entered_username
              self.firstname = data['users'][id]['firstname']
              self.lastname = data['users'][id]['lastname']
              self.__password = hashed_password
              self.__permission = data['users'][id]['permission']
              self.__email = data['users'][id]['email']
              self.__account_id = id
              self.date_of_create = data['users'][id]['dateofcreate']
              self.__balance = data['users'][id]['balance']
              self.cmd_logs_saves("You signed in")
              return True
            else:
              print("something went wrong")

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

              date_now = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
              data["users"][user_id] = {
                  "username":username,
                  "firstname":firstname,
                  "lastname":lastname,
                  'permission':'customer',
                  'dateofcreate':date_now,
                  'balance': 0,
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
          self.cmd_logs_saves("You signed out")
          self.username = None
          self.firstname = None
          self.lastname = None
          self.__password = None
          self.__permission = 'guest'
          self.__email = None
          self.__account_id = None
          self.date_of_create = None
          self.__balance = 0
          self.cart = {}
        else:
          print(f"{Fore.RED} AuthSystem:  You cancel it.")
    except Exception as ex:
       print(f"{Fore.RED}Auth Error: {ex}")
