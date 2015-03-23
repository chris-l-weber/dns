from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

DNS = {
    'google.com': {'ip': '173.194.33.179'},
    'microsoft.com': {'ip': '134.170.188.221'},
    'urbanairship.com': {'ip': '216.223.21.212'},
}


def abort_if_name_doesnt_exist(name):
    if name not in DNS:
        abort(404, message="name {} doesn't exist".format(name))

def validIp(ip):
    try:
        parts = ip.split('.')
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except ValueError:
        return False # one of the 'parts' not convertible to integer
    except (AttributeError, TypeError):
        return False # `ip` isn't even a string

parser = reqparse.RequestParser()
parser.add_argument('ip', type=str)
parser.add_argument('name', type=str)


# ip
#   show a single item and lets you delete them
class dns(Resource):
    def get(self, name):
        abort_if_name_doesnt_exist(name)
        return DNS[name]

    def delete(self, name):
        abort_if_name_doesnt_exist(name)
        del DNS[name]
        return '', 204

    def post(self,name):
        abort(404, message="Post not Allowed")

    def put(self, name):
        args = parser.parse_args()
        abort_if_name_doesnt_exist(name)
        if (args['ip'] is None):
            abort(404,message="Ip required")

        ip = args['ip']
        if not validIp(ip):
            abort(404,message="Ip address Invalid:"+str(ip))

        ip = {'ip': args['ip']}
        DNS[name] = ip
        return ip, 201


# dnsList
#   shows a list of all Entries , and lets you POST to add new ips
class dnsList(Resource):
   
    def get(self):
        return DNS

    def delete(self,name):
        abort(404, message="DELETE not Allowed")

    def put(self,name):
        abort(404, message="PUT not Allowed")


    def post(self):
        args = parser.parse_args()
        
        if (args['name'] is None or args['ip'] is None):
            abort(404,message="Name and ip required")

        name = args['name']
        ip = args['ip']
        
        if not validIp(ip):
            abort(404,message="Ip address Invalid:"+str(ip))
        
        if name in DNS:
            abort(404,message="Item already exists name:"+str(name))

        DNS[name] = {'ip': ip}
        return DNS[name], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(dnsList, '/dns')
api.add_resource(dns, '/dns/<name>')


if __name__ == '__main__':
    app.run(debug=True)