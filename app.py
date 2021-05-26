import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/<id>/<token>', methods=['POST'])
def valid(id, token):
    url = f"https://discordapp.com/api/webhooks/{id}/{token}"

    try:
        # Convert text to discord type
        embed = Discord(Json(request.json))

        if embed is None: return '', 204
    except Exception as e:
        # Error Embed
        embed = {
            "title": "Webhook Error",
            "description": f"**Full Response -** ```{request.data}```"
        }

    # Send Embed
    data = {
        "embeds": [embed],
    }
    r = requests.post(url, json=data)

    return r.content, r.status_code, r.headers.items()


def Discord(Json):
    """
    converts a heroku webhook payload to a discord webhook embed
    """
    # Data
    resource = Json['resource']
    title = f"[{Json['data:app:name']}] {resource}"
    description = None
    fields = []

    # Add Fields
    def field(name, names):
        fields.append({
            "name": name,
            "value": Json[names],
            "inline": True,
        })

    # detail for each event
    if resource == 'dyno':
        title += f" {Json['data:state']}"
        resource = f"{Json['data:state']}"

    elif resource == 'build':
        status = Json['data:status']
        if status == 'pending': status = "in progress"
        title += f" {status}"
        resource = f"{status}"

    elif resource == 'release':
        status = Json['data:status']
        if status == 'succeeded' and Json['action'] == 'update': return 
        title += f" {status}"
        resource = f"{status}"
        description = "`" + Json['data:description'] + "`"
        field("Version", 'data:version')
        field("Current", 'data:current')

    else:  # default
        title += f"-{Json['action']}"
        resurce = f"-{Json['action']}" 

    # Embed
    return {
        "color": color(resource),
        "author": {
            "name": "Heroku",
        },
        "title": title,
        "url": f"https://{Json['data:app:name']}.herokuapp.com",
        "description": description,
        "fields": fields,
        "timestamp": Json['created_at'],
    }


#  Invalid Requests

app.config['TRAP_HTTP_EXCEPTIONS'] = True


@app.errorhandler(Exception)
def invalid(e):
    return 'An Invalid request, for more information go to the <a href="https://github.com/aniket091/discord-webhook">GitHub page</a>', 404


#   Utils

class Json:
    def __init__(self, bJson):
        self.bJson = bJson

    def __getitem__(self, names):
        item = self.bJson
        for param in names.split(":"):
            if param in item:
                item = item[param]
            else:
                raise KeyError(f"-No '{param}' while getting '{names}'-")
        return item


def color(string):
    if string == "starting" or string == "succeeded"or string == "create":
        color = 0x00ff5b           # #00ff5b
    elif string == "crashed"or string == "down"or string == "destroy":
        color = 0xfa5c67           # #fa5c67 
    elif string == "up" or string == "in progress":
        color = 0x02c0d8           # #02c0d8     
    elif string == "update":
        color = 0xfaba7a           # #faba7a       
    else:
        color = 0x687fd4           # #687fd4  
    
    return color     

#      MAIN 

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
