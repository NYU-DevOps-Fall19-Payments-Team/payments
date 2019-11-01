credit_card_schema = {
    "title": "credit_card",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "credit_card_number": {
            "type": "string",
            "required": True
        },
        "card_holder_name": {
            "type": "string",
            "required": True
        },
        "expiration_month": {
            "type": "number",
            "minimum": 1,
            "maximum": 12,
            "required": True
        },
        "expiration_year": {
            "type": "number",
            "minimum": 2020,
            "maximum": 2099,
            "required": True
        },
        "security_code": {
            "type": "string",
            "required": True
        }
    }
}