"""This file holds the obfuscator yaml validator/definition template."""

VALIDATOR = {
    "type": {
        "type": str,
        "required": True,
        "allowed": "^(cmd|code|file)$",
        "childs": {},
    },
    "version": {
        "type": str,
        "required": True,
        "allowed": "^([0-9]+\\.[0-9]+\\.[0-9]+)$",
        "childs": {},
    },
    "obfuscators": {
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
            "meta": {
                "type": dict,
                "required": True,
                "childs": {
                    "authors": {
                        "type": list,
                        "required": True,
                        "childs": {},
                    },
                    "created": {
                        "type": str,
                        "required": True,
                        "allowed": "^([0-9]{4}-[0-9]{2}-[0-9]{2})$",
                        "childs": {},
                    },
                    "modified": {
                        "type": str,
                        "required": True,
                        "allowed": "^([0-9]{4}-[0-9]{2}-[0-9]{2})$",
                        "childs": {},
                    },
                    "version": {
                        "type": str,
                        "required": True,
                        "allowed": "^([0-9]+\\.[0-9]+\\.[0-9]+)$",
                        "childs": {},
                    },
                },
            },
            "filters": {
                "type": dict,
                "required": True,
                "childs": {
                    "shells": {
                        "type": list,
                        "required": True,
                        "childs": {},
                    },
                    "commands": {
                        "type": list,
                        "required": True,
                        "childs": {},
                    },
                    "encoders": {
                        "type": list,
                        "required": True,
                        "childs": {},
                    },
                },
            },
            "payload": {
                "type": str,
                "required": True,
                "allowed": "^(.+__PAYLOAD__|__PAYLOAD__.+|.+__PAYLOAD__.+)$",
                "childs": {},
            },
        },
    },
}
