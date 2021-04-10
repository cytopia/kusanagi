"""This file holds the payload yaml validator/definition template."""

VALIDATOR = {
    "type": {
        "type": str,
        "required": True,
        "allowed": "^(cmd|code|file)$",
        "childs": {},
    },
    "command": {
        "type": str,
        "required": True,
        "allowed": "^(.+)$",
        "childs": {},
    },
    "version": {
        "type": str,
        "required": True,
        "allowed": "^([0-9]+\\.[0-9]+\\.[0-9]+)$",
        "childs": {},
    },
    "payloads": {
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
                    "cmd_exe": {
                        "type": str,
                        "required": True,
                        "allowed": "^(.+)$",
                        "childs": {},
                    },
                    "cmd_shell": {
                        "type": str,
                        "required": True,
                        "allowed": "^(.+)$",
                        "childs": {},
                    },
                    "shell": {
                        "type": str,
                        "required": True,
                        "allowed": "^(.+)$",
                        "childs": {},
                    },
                    "shells": {
                        "type": list,
                        "required": True,
                        "childs": {},
                    },
                    "os": {
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
                    "proto": {
                        "type": str,
                        "required": True,
                        "allowed": "^(tcp|udp)$",
                        "childs": {},
                    },
                    "direction": {
                        "type": str,
                        "required": True,
                        "allowed": "^(reverse|bind)$",
                        "childs": {},
                    },
                },
            },
            "variables": {
                "type": list,
                "required": True,
                "childs": {
                    "name": {
                        "type": str,
                        "required": True,
                        "allowed": "^(.+)$",
                        "childs": {},
                    },
                    "values": {
                        "type": list,
                        "required": True,
                        "childs": {
                            "value": {
                                "type": str,
                                "required": True,
                                "allowed": "^(.*)$",
                                "childs": {},
                            },
                            "filters": {
                                "type": dict,
                                "required": False,
                                "childs": {
                                    "cmd_exe": {
                                        "type": str,
                                        "required": False,
                                        "allowed": "^(.+)$",
                                        "childs": {},
                                    },
                                    "cmd_shell": {
                                        "type": str,
                                        "required": False,
                                        "allowed": "^(.+)$",
                                        "childs": {},
                                    },
                                    "shell": {
                                        "type": str,
                                        "required": False,
                                        "allowed": "^(.+)$",
                                        "childs": {},
                                    },
                                    "shells": {
                                        "type": list,
                                        "required": False,
                                        "childs": {},
                                    },
                                    "os": {
                                        "type": list,
                                        "required": False,
                                        "childs": {},
                                    },
                                    "commands": {
                                        "type": list,
                                        "required": False,
                                        "childs": {},
                                    },
                                    "encoders": {
                                        "type": list,
                                        "required": False,
                                        "childs": {},
                                    },
                                    "proto": {
                                        "type": str,
                                        "required": False,
                                        "allowed": "^(tcp|udp)$",
                                        "childs": {},
                                    },
                                    "direction": {
                                        "type": str,
                                        "required": False,
                                        "allowed": "^(reverse|bind)$",
                                        "childs": {},
                                    },
                                },
                            },
                        },
                    },
                },
            },
            "payload": {
                "type": str,
                "required": True,
                "allowed": "^(.*__ADDR__.*__PORT__.*|.*__PORT__.*__ADDR__.*|.*__CODE__.*)$",
                "childs": {},
            },
        },
    },
}
