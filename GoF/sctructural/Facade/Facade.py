# Огромное количество импортов уже намекает на возможную необходимость создания [1-inf] Фасадов
# Допустим, мы постоянно создаем какой-то однотипный хедер отправляем на однотипный адрес.
# Лучше заменим всю эту инициализацию Фасадом

import requests
import json
import os


class JSONCompiler:

    def __init__(self, path='', name='json'):
        self.path = path
        self.name = name

    # Тут могли бы быть геттеры и сеттеры, но опустим это...

    def return_string(self):
        with open(os.path.join(self.path, self.name + '.json')) as file:
            return json.dumps(json.load(file))


class AuthCompiler:

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def compile_auth(self):
        return {'login': self.login, 'password': self.password}


class PostRequester:

    def __init__(self, service):
        self.service = service
        self.auth_data = None
        self.status = None
        self.body = None

    def make_post_request(self):
        try:
            r = requests.post(self.service, headers=self.auth_data, json=self.body)
            self.status = str(r.status_code) + r.reason
        except Exception:
            self.status = 'Something went wrong...'


class StandardPoster:

    def __init__(self, auth: AuthCompiler, req: PostRequester, json_com: JSONCompiler):
        self.auth = auth
        self.req = req
        self.json_com = json_com

    def standard_init(self):
        log_pas = self.auth.compile_auth()
        self.json_com.name = 'data'
        body = self.json_com.return_string()
        self.req.auth_data = log_pas
        self.req.body = body
        self.req.make_post_request()
        print(self.req.status)


def demo():
    requester = PostRequester('http://localhost')
    auth_com = AuthCompiler('hello', 'world')
    json_com = JSONCompiler()

    facade = StandardPoster(auth=auth_com, req=requester, json_com=json_com)

    facade.standard_init()


if __name__ == "__main__":
    demo()
