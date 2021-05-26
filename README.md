# Heroku to Discord webhook middleware

Send Heroku notifications to a Discord channel via webhook.

## Usage:
* Create a discord webhook (from a channel: edit channel->Webhooks->create). You should get a url with this format: `https://discordapp.com/api/webhooks/<id>/<key>` 
* Now go to Heroku and add the following webhook, changing the two last paths to the ones in your previously created webhook: `https://discord-web-hooks.herokuapp.com/<id>/<key>`.

For example, if your Discord webhook was  
 `https://discordapp.com/api/webhooks/123456789012345678/abcdefghijklmnopqrstuvwxyz`  
You should write  
 `https://discord-web-hooks.herokuapp.com/123456789012345678/abcdefghijklmnopqrstuvwxyz`  
This will use my deployed server as a middleware (details in 'Sample server'). If you want to deploy your own server check 'Deploy custom server'.

## Sample server
This app is hosted on Heroku, meaning you can follow the steps in 'Usage' to test directly. However note that the app is hosted on a free account, so it may take a few seconds to wake up, and also it may be abused in which case I will turn it off. Also note that although the app doesn't save/record any data (and I promise I will never do it), Heroku might save and keep a log of the petitions, so better not use it for sensible data. The sample server is: `https://discord-web-hooks.herokuapp.com/`

## Deploy custom server
If you want to deploy your own copy for personal use, just:
1) Fork the project.
1) Deploy your fork to Heroku or any other web service. The app is ready-to-deploy on Heroku, but it is just a Flask one-file app so other services should be fine.
1) Use your own url for the webhooks. In the second step of 'Usage' simply use your deployment url instead of mine.
