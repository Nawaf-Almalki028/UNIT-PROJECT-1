Overview
A command-line interface (CLI) application for managing a cloud hosting service, where users can:

Browse and purchase virtual servers (VPS/VDS) and game servers.

Manage their account, balance, and active services.

Interact with support via a ticketing system.

The system supports three user roles:

Guest – Can browse products and sign up.

Customer – Can purchase, manage services, and contact support.

Administrator – Can manage users, ban/unban, and view logs.

Features & User Stories
As a Guest, I should be able to do the following commands:

  Help- Available Commands:
  -> Products: products tree commands
       products vps
       products vds
       products gameserver
  -> Cart: cart tree commands
       cart show
       cart add
       cart remove
  -> Signup: Create a new account
  -> Signin: Sign in to your account


As a Customer, I should be able to do the following commands:

  Help - Available Commands:
  -> Dashboard: dashboard commands
       dashboard show
       dashboard services
       dashboard start
       dashboard stop
  -> Products: products commands
       products vps
       products vds
       products gameserver
  -> Cart: cart commands
       cart show
       cart add
       cart remove
       cart pay
  -> Tickets: ticket commands
       tickets create
       tickets show
       tickets reply
  -> Balance: balance commands
       balance show
       balance add
  -> Logs: View your logs
  -> Logout: Log out of your account


As a Administrator, I should be able to do the following commands:

  Help - Available Commands:
  -> AdminCMD: moderation commands
       admincmd ban
       admincmd unban
  -> Dashboard: dashboard commands
       dashboard show
       dashboard services
       dashboard start
       dashboard stop
  -> Products: products commands
       products vps
       products vds
       products gameserver
  -> Cart: cart commands
       cart show
       cart add
       cart remove
       cart pay
  -> Users: user management
       users promote
       users demote
  -> Logs: View customer or system logs
  -> Tickets: ticket commands
       tickets show
       tickets reply
       tickets close
  -> Balance: balance commands
       balance show
       balance add
  -> Logout: Log out of your account


You can use (help) commands to understand more!

accounts already to use:

customer permission
  name: customer
  password: 1234567

administrator permission
  name: admin
  password: 1234567