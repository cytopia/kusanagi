"""This file holds the payload yaml validator/definition template."""

VALIDATOR = {
    "specification": {
        "type": dict,
        "required": True,
        "childs": {
            "payload": {
                "type": str,
                "required": True,
                "allowed": "^(code)$",
                "childs": {},
            },
            "type": {
                "type": str,
                "required": True,
                "allowed": "^(obfuscator)$",
                "childs": {},
            },
            "version": {
                "type": str,
                "required": True,
                "allowed": "^([0-9]\\.[0-9]\\.[0-9])$",
                "childs": {},
            },
        },
    },
    "items": {
        "type": list,
        "required": True,
        "childs": {
            "name": {
                "type": str,
                "required": True,
                "allowed": "^(.+)$",
                "childs": {},
            },
            "desc": {
                "type": str,
                "required": True,
                "allowed": "^(.+)$",
                "childs": {},
            },
            "info": {
                "type": list,
                "required": True,
                "childs": {},
            },
            "code": {
                "type": dict,
                "required": True,
                "childs": {
                    "language": {
                        "type": str,
                        "required": True,
                        "allowed": "^(.+)$",
                        "childs": {},
                    },
                    "requires": {
                        "type": dict,
                        "required": True,
                        "childs": {
                            "version": {
                                "type": list,
                                "required": True,
                                "childs": {},
                            },
                            "commands": {
                                "type": list,
                                "required": True,
                                "childs": {},
                            },
                            "functions": {
                                "type": list,
                                "required": True,
                                "childs": {},
                            },
                            "modules": {
                                "type": list,
                                "required": True,
                                "childs": {},
                            },
                            "os": {
                                "type": list,
                                "required": True,
                                "childs": {},
                            },
                        },
                    },
                },
            },
            "payload": {
                "type": str,
                "required": True,
                "allowed": "(.*__CODE__.*)",
                "childs": {},
            },
        },
    },
}
