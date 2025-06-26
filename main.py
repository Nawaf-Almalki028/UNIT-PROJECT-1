from        Functions.cli_operators   import      cli_analysis
from        colorama                  import      Fore
import      art
import      time

print(Fore.YELLOW)
art.tprint("TQ Hosting")

print(Fore.GREEN + """
-------------------------------------------

        This is only for testing!

-------------------------------------------
""")

while True:

  cli_command = input("==> ")

  cli_analysis(cli_command)



