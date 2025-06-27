from        colorama                        import      Fore

help_messages = {
    "administrator": f"""{Fore.CYAN}
  {Fore.YELLOW}Help{Fore.CYAN} - Available Commands:

  -> {Fore.YELLOW}Dashboard{Fore.CYAN}: Show your dashboard overview
  -> {Fore.YELLOW}Products{Fore.CYAN}: List your E-Mail, VPS, VDS, and Game Server products
  -> {Fore.YELLOW}Cart{Fore.CYAN}: Show your cart
  -> {Fore.YELLOW}Mails{Fore.CYAN}: Check all customers' emails
  -> {Fore.YELLOW}Email{Fore.CYAN}: Open your email
  -> {Fore.YELLOW}Users{Fore.CYAN}: Manage user accounts
  -> {Fore.YELLOW}Logs{Fore.CYAN}: View customer or system logs
  -> {Fore.YELLOW}Reports{Fore.CYAN}: Generate system reports
  -> {Fore.YELLOW}Logout{Fore.CYAN}: Log out of your account
  """,

      "customer": f"""{Fore.CYAN}
  Help - Available Commands:

  -> {Fore.YELLOW}Dashboard{Fore.CYAN}: Show your dashboard
  -> {Fore.YELLOW}Products{Fore.CYAN}: List your E-Mail, VPS, VDS, and Game Server products
  -> {Fore.YELLOW}Cart{Fore.CYAN}: Show your cart
  -> {Fore.YELLOW}Mails{Fore.CYAN}: Check your emails
  -> {Fore.YELLOW}Email{Fore.CYAN}: Open your email
  -> {Fore.YELLOW}Orders{Fore.CYAN}: View your orders
  -> {Fore.YELLOW}Support{Fore.CYAN}: Contact support team
  -> {Fore.YELLOW}Logs{Fore.CYAN}: View your logs
  -> {Fore.YELLOW}Logout{Fore.CYAN}: Log out of your account
  """,

      "guest": f"""{Fore.CYAN}
  Help - Available Commands:

  -> {Fore.YELLOW}Products{Fore.CYAN}: View available E-Mail, VPS, VDS, and Game Server products
  -> {Fore.YELLOW}Cart{Fore.CYAN}: Show your cart
  -> {Fore.YELLOW}Signup{Fore.CYAN}: Create a new account
  -> {Fore.YELLOW}Signin{Fore.CYAN}: Sign in to your account
  """
  }
