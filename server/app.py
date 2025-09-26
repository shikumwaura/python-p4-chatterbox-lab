from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Message
from flask_cors import CORS
import ipdb # Used for debugging, can be removed in final code

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

CORS(app) # Allow cross-origin requests

api = Api(app)

# Helper function to convert Message object to a dictionary for JSON response
def message_to_dict(message):
    return {
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at.isoformat(),
        'updated_at': message.updated_at.isoformat()
    }

class Messages(Resource):
    
    # GET /messages
    def get(self):
        messages = Message.query.order_by(Message.created_at.asc()).all()
        # Use a list comprehension to convert all messages to dictionaries
        messages_dict = [message_to_dict(m) for m in messages]
        return make_response(jsonify(messages_dict), 200)

    # POST /messages
    def post(self):
        # 1. Get data from the request body (as JSON)
        data = request.get_json()
        
        try:
            # 2. Create a new Message instance
            new_message = Message(
                body=data.get('body'),
                username=data.get('username')
            )
            
            # 3. Add to session and commit
            db.session.add(new_message)
            db.session.commit()
            
            # 4. Return the newly created message as JSON
            return make_response(message_to_dict(new_message), 201)
        
        except ValueError:
            # Handle potential validation errors (e.g., if body/username is missing/invalid)
            return make_response(jsonify({"errors": ["Validation errors"]}), 400)

class MessageByID(Resource):
    
    # PATCH /messages/<int:id>
    def patch(self, id):
        message = db.session.get(Message, id)
        
        if not message:
            return make_response(jsonify({"error": "Message not found"}), 404)
        
        # 1. Get data from the request body
        data = request.get_json()
        
        try:
            # 2. Update the 'body' attribute
            if 'body' in data:
                setattr(message, 'body', data['body'])
            
            # 3. Commit changes (updated_at will be automatically set by onupdate)
            db.session.commit()
            
            # 4. Return the updated message as JSON
            return make_response(message_to_dict(message), 200)
            
        except ValueError:
             # Handle potential validation errors
            return make_response(jsonify({"errors": ["Validation errors"]}), 400)
            
    # DELETE /messages/<int:id>
    def delete(self, id):
        message = db.session.get(Message, id)
        
        if not message:
            return make_response(jsonify({"error": "Message not found"}), 404)
            
        # 1. Delete the message
        db.session.delete(message)
        
        # 2. Commit the transaction
        db.session.commit()
        
        # 3. Return an empty response with status 204 (No Content)
        return make_response({}, 204)


# Add the routes to the API
api.add_resource(Messages, '/messages')
api.add_resource(MessageByID, '/messages/<int:id>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)