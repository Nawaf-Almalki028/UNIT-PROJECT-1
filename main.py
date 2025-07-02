from        Classes.cli_operators   import      CliHandler
from        colorama                import      Fore
import      art
import      time

print(Fore.YELLOW)
art.tprint("TQ Hosting")

print(Fore.GREEN + """
-------------------------------------------
            TQ Hosting CLI
-------------------------------------------
""")

person_information = CliHandler('',"guest")

while True:
  cli_command = input(Fore.YELLOW + "==> ")
  person_information.command_entered = cli_command.lower()
  person_information.cli_analysis()



