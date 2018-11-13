import falcon
import tornado.wsgi
import json
from user_model import User
from db_user_repository import DbUserRepository

class CreateUserResource:
    def __init__(self, repository):
        self.repository = repository

    def on_post(self, req, resp):
        body = req.stream.read()
        decoded_body = body.decode('utf-8')
        data = json.loads(decoded_body)
        name = data["name"]
        self.repository.create({"name":name})
        resp.body = "OK"
        resp.status = falcon.HTTP_200

class UsersResource:
    def __init__(self,repository):
        self.repository = repository

    def on_get(self, req, resp, user_id):
        resp.body = json.dumps(self.repository.get(user_id))
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, user_id):
        body = req.stream.read()
        decoded_body = body.decode('utf-8')
        data = json.loads(decoded_body)
        name = data["name"]
        self.repository.set(user_id,{"name":name})
        resp.body = "OK"
        resp.status = falcon.HTTP_201

def run():
    api = falcon.API()
    repository = DbUserRepository('sqlite:///test.db')
    api.add_route('/users', CreateUserResource(repository))
    api.add_route('/users/{user_id:int}', UsersResource(repository))

    container = tornado.wsgi.WSGIContainer(api)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__=="__main__":
    run()
