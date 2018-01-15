# announcementbot
GroupMe announcement system that broadcasts messages to a list of configurable contacts over GroupMe Direct Message.

## How it works
A control group set up with an always-listening GroupMe bot makes for easy message broadcasting. Simply type 
or paste the desired message into the control group and the message is broadcast to all members on the
contact list via direct message. 
NOTE: The direct messages are not sent by the GroupMe bot but by a configured GroupMe user account. 

## Contact management
Contacts are managed via a web-based interface. 
Contacts can be viewed under the route `/contacts`.
The entire contacts list can also be reseeded from a selected GroupMe group via the route `/reseed`.

## Set Up:

### GroupMe Configuration:
You must register 
1. a GroupMe bot for listening and notifying the control group
  * set the callback url to your host at route `/listen`
2. a GroupMe application for authenticating contact reseeding requests
  * set the callback url to your host at route `/reseed/authenticate_result`
3. a valid GroupMe user account for sending the direct messages (GroupMe does not allow bots to
send DM's).

### Environment Variables:
The following env variables are required:
- BOT_ID (the id provided by GroupMe of the control group bot)
- ACCESS_TOK (the GroupMe user token of the account to send DM's)
- APP_REDIRECT (this is the redirect url provided by GroupMe upon registration of your GroupMe application)
- DATABASE_URL (URL for your postgres database)
- ADMIN_USER (Username for web-interface)
- ADMIN_PASS (Password for web-interface)



