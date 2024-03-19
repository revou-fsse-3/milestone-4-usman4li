from marshmallow import Schema, fields

class userSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()