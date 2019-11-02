payment_schema = {
    "title": "payment",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "order_id": {
            "type": "number",
            "minimum": 1,
            "required": True
        },
        "customer_id": {
            "type": "number",
            "minimum": 1,
            "required": True
        },
        "available": {
            "type": "boolean",
            "required": True
        },
        "payments_type": {
            "type": "string",
            "enum": ["credit card", "paypal"],
            "required": True
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
                            "required": True,
                            "additionalProperties": False,
                            "properties": {
                                "credit_card_number": {
                                    "type": "string",
                                    "maxLength": 30,
                                    "required": True
                                },
                                "card_holder_name": {
                                    "type": "string",
                                    "maxLength": 30,
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
                                    "maxLength": 4,
                                    "required": True
                                }
                            }
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
                            "required": True,
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
                                    "maxLength": 30,
                                    "required": True
                                }
                            },
                            "anyOf": [
                                {"required": ["email"]},
                                {"required": ["phone_number"]}
                            ]
                        }
                    }
                }
            }
        ]
    }
}
