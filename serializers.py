from marshmallow import Schema, fields

class WalletSchema(Schema):
    address = fields.Str(dump_only=True)
    payment_page_slug = fields.Str(dump_only=True)
    payment_page_id = fields.Str(dump_only=True)