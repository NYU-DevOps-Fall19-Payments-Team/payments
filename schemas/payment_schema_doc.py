# For documentation
payment_schema_doc = {
    "title": "payment",
    "type": "object",
    "properties": {
        "order_id": {
            "type": "number",
            "minimum": 0
        },
        "customer_id": {
            "type": "number",
            "minimum": 0
        },
        "available": {
            "type": "boolean"
        },
        "type": {
            "type": "string",
            "enum": ["credit card", "paypal"]
        },
        "info": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "credit_card_number": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 30
                },
                "card_holder_name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 30
                },
                "expiration_month": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 12
                },
                "expiration_year": {
                    "type": "number",
                    "minimum": 2020,
                    "maximum": 2099
                },
                "security_code": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 4
                }
            },
            "required": [
                "credit_card_number",
                "card_holder_name",
                "expiration_month",
                "expiration_year",
                "security_code"
            ]
        }
    },
    "required": [
        "order_id",
        "customer_id",
        "available",
        "type",
        "info"
    ]
}