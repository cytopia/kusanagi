"""Module to load a yaml template."""
from typing import Dict, List, Union, Any

import errno
import os
import yaml


class YamlLoader(object):
    """Read yaml template files."""

    @staticmethod
    def load(path: str) -> Dict[Any, Any]:
        """Return dict of a yaml template file by given path, validates it and adds defaults.

        Args:
            path (str): Path to yaml template file.

        Returns:
            Dict[Any, Any]: The loaded yaml file with valid keys and types.

        Raises:
            OSError: If file not found or no permission to read it.
            KeyError: If yaml is invalid, ha missing or wrong keys.
        """
        # payload: cmd        # cmd, code or file
        # direction: reverse  # reverse or bind
        # payloads:
        #   <key>:
        #     name: <key-name>
        #     desc: <key-desc>
        #     items: []
        data = YamlLoader.__load_yaml(path)
        if not isinstance(data, dict):
            raise KeyError(f"file must be of type dict: {path}")

        # payload
        if "payload" not in data:
            raise KeyError(f"file must contain payload key in: {path}")
        if not isinstance(data["payload"], str):
            raise KeyError(f"payload key must be of type str in: {path}")
        if data["payload"] not in ["cmd", "code", "file"]:
            raise KeyError(f"payload key must have a value of cmd, code or file in: {path}")

        # direction
        if "direction" not in data:
            raise KeyError(f"file must contain direction key in: {path}")
        if not isinstance(data["direction"], str):
            raise KeyError(f"direction key must be of direction str in: {path}")
        if data["direction"] not in ["reverse", "bind"]:
            raise KeyError(f"direction key must have a value of reverse or bind in: {path}")

        # payloads
        if "payloads" not in data:
            raise KeyError(f"file must contain payloads key in: {path}")
        if not isinstance(data["payloads"], dict):
            raise KeyError(f"payloads key must be of type dict in: {path}")

        valid_keys = ["direction", "payload", "payloads"]
        for toplevel_key in data:
            if toplevel_key not in valid_keys:
                raise KeyError(f"{toplevel_key} is a wrong top-level key in: {path}")

        for key, val in data["payloads"].items():
            for i in range(len(val["items"])):
                try:
                    YamlLoader.__validate_item(val["items"][i])
                except KeyError as error:
                    raise KeyError(f"[ERROR] payload.{key}: {error} in: {path}")
                data["payloads"][key]["items"][i] = YamlLoader.__add_item_defaults(
                    val["items"][i], data["payload"], data["direction"]
                )

        return data

    # --------------------------------------------------------------------------
    # Private functions
    # --------------------------------------------------------------------------
    @staticmethod
    def __add_item_defaults(
        item: Dict[str, Any], payload_type: str, payload_direction: str
    ) -> Dict[str, Any]:
        # filters:
        item["filters"]["direction"] = payload_direction
        item["filters"]["payload"] = payload_type

        # variables:
        #   - name: shell
        #     filters:
        #       shell: {VAR:shell}
        #     values:
        #       - val1
        #       - val2
        if "variables" not in item:
            item["variables"] = []

        for i in range(len(item["variables"])):
            if "filters" not in item["variables"][i]:
                item["variables"][i]["filters"] = {}

        # variations:
        #   - name: shell
        #     filters:
        #       obfuscated: true
        #     payload: $(echo {PAYLOAD}|base64)|{VAR:shell}
        if "variations" not in item:
            item["variations"] = []

        for i in range(len(item["variations"])):
            if "filters" not in item["variations"][i]:
                item["variations"][i]["filters"] = {}

        return item

    @staticmethod
    def __validate_item(item: Dict[str, Any]) -> None:
        """Validate yaml and throws a KeyError exception on wrong/missing keys."""
        # item = {
        #   name: payload-name
        #   desc: payload-desc
        #   filters: {}
        #   variables: []
        #   variations: []
        #   payload: nc -e /bin/sh {ADDR} {PORT}
        # }
        valid_keys = ["name", "desc", "filters", "variables", "variations", "payload"]

        if not isinstance(item, dict):
            raise KeyError("item must be of type dict")

        if "name" not in item:
            raise KeyError("name key is missing")
        if not item["name"]:
            raise KeyError("name key must not be empty")
        if not isinstance(item["name"], str):
            raise KeyError("name key must be a string")

        if "desc" not in item:
            raise KeyError("desc key is missing")
        if not item["desc"]:
            raise KeyError("desc key must not be empty")
        if not isinstance(item["desc"], str):
            raise KeyError("desc key must be a string")

        if "payload" not in item:
            raise KeyError("payload key is missing")
        if not item["payload"]:
            raise KeyError("payload key must not be empty")
        if not isinstance(item["payload"], str):
            raise KeyError("payload key must be a string")

        if "filters" not in item:
            raise KeyError("filters key is missing")

        # check for invalid keys
        for key in item:
            if key not in valid_keys:
                raise KeyError(f"Invalid key: {key}")

        # variables:
        #   - name: shell
        #     filters:
        #       shell: {VAR:shell}
        #     values:
        #       - val1
        #       - val2
        if "variables" in item:
            valid_keys = ["name", "filters", "values"]

            if not isinstance(item["variables"], list):
                raise KeyError("variables key must be a list")

            for i in range(len(item["variables"])):
                # Check name
                if "name" not in item["variables"][i]:
                    raise KeyError("name key is missing in variables")
                if not item["variables"][i]["name"]:
                    raise KeyError("name key must not be empty in variables")
                if not isinstance(item["variables"][i]["name"], str):
                    raise KeyError("name key must be a string in variables")
                # Check filters
                if "filters" in item["variables"][i]:
                    if not isinstance(item["variables"][i]["filters"], dict):
                        raise KeyError("filters key must be a dict in variables")
                # Check values
                if "values" not in item["variables"][i]:
                    raise KeyError("values key is missing in variables")
                if not item["variables"][i]["values"]:
                    raise KeyError("values key must not be empty in variables")
                if not isinstance(item["variables"][i]["values"], list):
                    raise KeyError("values key must be a list in variables")

                # check for invalid keys
                for key in item["variables"][i]:
                    if key not in valid_keys:
                        raise KeyError(f"Invalid key: {key} in variables")

        # variations:
        #   - name: shell
        #     filters:
        #       obfuscated: true
        #     payload: $(echo {PAYLOAD}|base64)|{VAR:shell}
        if "variations" in item:
            valid_keys = ["name", "filters", "payload"]

            if not isinstance(item["variations"], list):
                raise KeyError("variations key must be a list")

            for i in range(len(item["variations"])):
                # Check name
                if "name" not in item["variations"][i]:
                    raise KeyError("name key is missing in variations")
                if not item["variations"][i]["name"]:
                    raise KeyError("name key must not be empty in variations")
                if not isinstance(item["variations"][i]["name"], str):
                    raise KeyError("name key must be a string in variations")
                # Check filters
                if "filters" in item["variations"][i]:
                    if not isinstance(item["variations"][i]["filters"], dict):
                        raise KeyError("filters key must be a dict in variations")
                # Check payload
                if "payload" not in item["variations"][i]:
                    raise KeyError("payload key is missing in variations")
                if not item["variations"][i]["payload"]:
                    raise KeyError("payload key must not be empty in variations")
                if not isinstance(item["variations"][i]["payload"], str):
                    raise KeyError("payload key must be a list in variations")

                # check for invalid keys
                for key in item["variations"][i]:
                    if key not in valid_keys:
                        raise KeyError(f"Invalid key: {key} in variations")

    @staticmethod
    def __load_yaml(path: str) -> Dict[Any, Any]:
        """Load yaml file and return yaml dictionary.

        Args:
            path (str): Path to yaml file.

        Returns:
            dict: Python dict from yaml file.

        Raises:
            OSError: If file not found or yaml cannot be parsed.
        """
        try:
            file_p = open(path)
        except FileNotFoundError as err_file:
            error = os.strerror(errno.ENOENT)
            raise OSError(f"File does not exist: {path}\n{error}")
        except PermissionError as err_perm:
            error = os.strerror(errno.EACCES)
            raise OSError(f"No permission to load file form: {path}\n{error}")
        else:
            try:
                return dict(yaml.safe_load(file_p))
            except yaml.YAMLError as err_yaml:
                error = str(err_yaml)
                raise KeyError(f"[ERROR]: {path}\n{error}") from err_yaml
            finally:
                file_p.close()
