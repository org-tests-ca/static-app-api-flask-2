from flask import Flask, send_from_directory, request
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

# Dados de exemplo
items = [
    {"id": 1, "title": "Item 1", "description": "Descrição do Item 1"},
    {"id": 2, "title": "Item 2", "description": "Descrição do Item 2"},
]

# Definição dos recursos
class ItemList(Resource):
    def get(self):
        return items

    def post(self):
        # Adiciona um novo item com os dados fornecidos
        data = request.get_json()
        new_item = {
            "id": data["id"],
            "title": data["title"],
            "description": data["description"]
        }
        items.append(new_item)
        return new_item, 201  # Retorna o novo item com o código de status 201 (Created)

class Item(Resource):
    def get(self, item_id):
        for item in items:
            if item['id'] == item_id:
                return item
        return {'message': 'Item não encontrado'}, 404

    def put(self, item_id):
        data = request.get_json()
        for item in items:
            if item['id'] == int(item_id):
                item.update(data)
                return item
        return {'message': 'Item não encontrado'}, 404

    def delete(self, item_id):
        global items
        items = [item for item in items if item['id'] != item_id]
        return {'message': 'Item excluído com sucesso'}, 200

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<int:item_id>')

# Rota para servir o arquivo swagger.json
@app.route('/docs/<path:path>')
def serve_docs(path):
    return send_from_directory('docs', path)

# Configuração do Swagger
SWAGGER_URL = '/swagger'
API_URL = '/docs/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Minha API Flask"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
