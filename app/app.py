from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import uuid

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Fruit API',
    description='A simple Fruit API',
)

ns = api.namespace('fruits', description='Fruit operations')

fruit = api.model('Fruit', {
    'id': fields.String(readonly=True, description='The fruit unique identifier'),
    'name': fields.String(required=True, description='The fruit name'),
    'qty': fields.Integer(required=True, description='The quantity of the fruit'),
    'price': fields.Float(required=True, description='The price of the fruit')
})


class FruitDAO(object):
    def __init__(self):
        self.fruits = []

    def get(self, id):
        for fruit in self.fruits:
            if fruit['id'] == id:
                return fruit
        api.abort(404, "Fruit {} doesn't exist".format(id))

    def create(self, data):
        fruit = data
        fruit['id'] = str(uuid.uuid4())  # generate a new UUID for each fruit
        self.fruits.append(fruit)
        return fruit

    def update(self, id, data):
        fruit = self.get(id)
        fruit.update(data)
        return fruit

    def delete(self, id):
        fruit = self.get(id)
        self.fruits.remove(fruit)


DAO = FruitDAO()
DAO.create({'name': 'Apple', 'qty': 10, 'price': 0.5})
DAO.create({'name': 'Banana', 'qty': 20, 'price': 0.3})
DAO.create({'name': 'Cherry', 'qty': 100, 'price': 0.05})

@ns.route('/')
class FruitList(Resource):
    '''Shows a list of all fruits, and lets you POST to add new fruits'''
    @ns.doc('list_fruits')
    @ns.marshal_list_with(fruit)
    def get(self):
        '''List all fruits'''
        return DAO.fruits

    @ns.doc('create_fruit')
    @ns.expect(fruit)
    @ns.marshal_with(fruit, code=201)
    def post(self):
        '''Create a new fruit'''
        return DAO.create(api.payload), 201


@ns.route('/<string:id>')
@ns.response(404, 'Fruit not found')
@ns.param('id', 'The fruit identifier')
class Fruit(Resource):
    '''Show a single fruit item and lets you delete them'''
    @ns.doc('get_fruit')
    @ns.marshal_with(fruit)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_fruit')
    @ns.response(204, 'Fruit deleted')
    def delete(self, id):
        '''Delete a fruit given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(fruit)
    @ns.marshal_with(fruit)
    def put(self, id):
        '''Update a fruit given its identifier'''
        return DAO.update(id, api.payload), 200


if __name__ == '__main__':
    app.run(debug=True)