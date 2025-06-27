from        Functions.cli_operators   import      cli_analysis
from        colorama                  import      Fore
import      art
import      time

print(Fore.YELLOW)
art.tprint("TQ Hosting")

print(Fore.GREEN + """
-------------------------------------------
        you can use this cli as you like!
-------------------------------------------
""")

while True:

  cli_command = input(Fore.YELLOW + "==> ")
  cli_command = cli_command.lower()

  cli_analysis(cli_command,"guest")



