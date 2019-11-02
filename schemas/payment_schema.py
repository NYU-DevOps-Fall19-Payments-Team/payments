payment_schema = {
    "title": "payment",
    "type": "object",
    "properties": {
        "order_id": {
            "type": "number",
            "minimum": 1
        },
        "customer_id": {
            "type": "number",
            "minimum": 1
        },
        "available": {
            "type": "boolean"
        },
        "payments_type": {
            "type": "string",
            "enum": ["credit card", "paypal"]
        }
    },
    "allOf": [
        {
            "if": {
                "properties": {
                    "payments_type": {"const": "credit card"}
                }
            },
            "then": {
                "properties": {
                    "info": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "credit_card_number": {
                                "type": "string",
                                "maxLength": 30
                            },
                            "card_holder_name": {
                                "type": "string",
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
                }
            }
        },
        {
            "if": {
                "properties": {
                    "payments_type": {"const": "paypal"}
                }
            },
            "then": {
                "properties": {
                    "info": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "email": {
                                "type": "string",
                                "maxLength": 30,
                            },
                            "phone_number": {
                                "type": "string",
                                "maxLength": 20,
                            },
                            "token": {
                                "type": "string",
                                "maxLength": 30
                            }
                        },
                        "anyOf": [
                            {"required": ["email"]},
                            {"required": ["phone_number"]}
                        ],
                        "required": ["token"]
                    }
                }
            }
        }
    ],
    "required": [
        "order_id",
        "customer_id",
        "available",
        "payments_type",
        "info"
    ]
}
