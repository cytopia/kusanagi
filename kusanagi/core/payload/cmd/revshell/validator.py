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
                "allowed": "^(revshell|bindshell)$",
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
            "rating": {
                "type": int,
                "required": True,
                "allowed": "^([0-9])$",
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
                    "executable": {
                        "type": str,
                        "required": True,
                        "allowed": "^(.+)$",
                        "childs": {},
                    },
                    "requires": {
                        "type": dict,
                        "required": True,
                        "childs": {
                            "commands": {
                                "type": list,
                                "required": True,
                                "childs": {},
                            },
                            "shell_env": {
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
            "revshell": {
                "type": dict,
                "required": True,
                "childs": {
                    "proto": {
                        "type": str,
                        "required": True,
                        "allowed": "^(tcp|udp)$",
                        "childs": {},
                    },
                    "shell": {
                        "type": str,
                        "required": True,
                        "allowed": "^(.+)$",
                        "childs": {},
                    },
                    "command": {
                        "type": (str, type(None)),
                        "required": True,
                        "allowed": "^(.+)$",
                        "childs": {},
                    },
                },
            },
            "payload": {
                "type": str,
                "required": True,
                "allowed": "(.*__ADDR__.*__PORT__.*|.*__PORT__.*__ADDR__.*)",
                "childs": {},
            },
        },
    },
}
