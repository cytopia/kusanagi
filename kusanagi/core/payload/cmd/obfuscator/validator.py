"""This file holds the payload yaml validator/definition template."""

VALIDATOR = {
    "specification": {
        "type": dict,
        "required": True,
        "childs": {
            "payload": {
                "type": str,
                "required": True,
                "allowed": "^(cmd)$",
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
            "meta": {
                "type": dict,
                "required": True,
                "childs": {
                    "author": {
                        "type": str,
                        "required": True,
                        "childs": {},
                    },
                    "editors": {
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
                        "allowed": "^([0-9]\\.[0-9]\\.[0-9])$",
                        "childs": {},
                    },
                },
            },
            "cmd": {
                "type": dict,
                "required": True,
                "childs": {
                    "requires": {
                        "type": dict,
                        "required": True,
                        "childs": {
                            "shell_env": {
                                "type": list,
                                "required": True,
                                "childs": {},
                            },
                            "commands": {
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
                    "overwrites": {
                        "type": dict,
                        "required": False,
                        "childs": {
                            "shell_env": {
                                "type": list,
                                "required": False,
                                "childs": {},
                            },
                        },
                    },
                },
            },
            "payload": {
                "type": str,
                "required": True,
                "allowed": "(.*__CMD__.*)",
                "childs": {},
            },
        },
    },
}
