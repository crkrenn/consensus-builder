"""
Module for statements
"""

# standard packages
from abc import ABC, abstractmethod, abstractproperty
import json
from collections import defaultdict
import random
import logging
import sys

# third-party packages
import jsonschema
import numpy as np

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

#@ TODO: separate user statement class and process statement class?
#@ TODO: cache statement sets?
#@ TODO: update votes in statement sets?

class AbstractStatements(ABC):
    """Abstract class for statements"""
    @abstractproperty
    def STATEMENTS_SCHEMA(self):
        pass

    @abstractproperty
    def PROBABILITIES_SCHEMA(self):
        pass

    def __init__(self):
        pass

    @abstractmethod
    def read_from_json(self):
        pass

    @abstractmethod
    def get_statement_list(self):
        pass

class Statements(AbstractStatements):
    """Class for statements"""
    STATEMENTS_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "actionable": {
                    "type": "string"
                },
                "group_label": {
                    "type": "string"
                },
                "votes": {
                    "type": ["string", "integer"],
                    "pattern": "^[0-9]+$"
                },
                "statement": {
                    "type": "string"
                },
                "uuid": {
                    "type": "string"
                }
            },
            "required": [
                "actionable",
                "group_label",
                "votes",
                "statement"
            ]
        }
    }

    PROBABILITIES_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "propertyNames": {
            "type": "string"
        },
        "additionalProperties": {
            "type": ["string", "number"],
            "pattern": "^[0-9.]+$"
        }
    }

    statements = []
    probabilities = {}
    actionable_keys = []
    group_label_keys = []
    statements_map = {}

    def __init__(self):
        super().__init__()
        self.filename = None
        self.statement_list = []
        self.statement_uuid_list = []

    def _validate_probability_keys(self):
        """Validate the probability keys"""
        keyset = set()
        for k in self.probabilities.keys():
            if k in keyset:
                raise Exception(f"Probability key ({k}) is duplicated")
            keyset.add(k)
            k = k.upper()
            if len(k) != 2:
                raise Exception("Probability keys must be of length 2")
            if k[0] != "*" and k[0] not in self.actionable_keys:
                raise Exception(f"Probability key ({k}) must start with {self.actionable_keys} or *")
            if k[1] != "*" and k[1] not in self.group_label_keys:
                raise Exception(f"Probability key ({k}) must end with {self.group_label_keys}, or *")

    def _validate_statements_and_probabilities(self):
        """Validate the statements and probabilities"""
        try:
            jsonschema.validate(
                instance=self.probabilities,
                schema=self.PROBABILITIES_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            print(f"Error: The probabilities are invalid: {str(e)}")
            raise e
        try:
            jsonschema.validate(
                instance=self.statements,
                schema=self.STATEMENTS_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            print(f"Error: The statements are invalid: {str(e)}")
            raise e
        self._validate_probability_keys()
        total = 0
        for _, v in self.probabilities.items():
            total += v
        if total != 1:
            raise Exception("Probabilities must add up to 1")

    def _extract_actionable_keys(self):
        """Extract the actionable keys"""
        keyset = set()
        for statement in self.statements:
            keyset.add(statement["actionable"].upper())
        self.actionable_keys = list(keyset)
        self.actionable_keys.sort()

    def _extract_group_label_keys(self):
        """Extract the group label keys"""
        keyset = set()
        for statement in self.statements:
            keyset.add(statement["group_label"].upper())
        self.group_label_keys = list(keyset)
        self.group_label_keys.sort()

    def _build_statements_map(self):
        """Build the statement sets"""
        self.statements_map = defaultdict(list)
        for statement in self.statements:
            actionable_key = statement["actionable"].upper()
            group_label_key = statement["group_label"].upper()
            key = actionable_key + group_label_key
            self.statements_map[key].append(statement)
            key = "*" + group_label_key
            self.statements_map[key].append(statement)
            key = actionable_key + "*"
            self.statements_map[key].append(statement)
            key = "**"
            self.statements_map[key].append(statement)
        for _, statement_set in self.statements_map.items():
            statement_set.sort(key=lambda x: x["votes"])

    def read_from_json(self, filename):
        """
        Read statements and probabilities from a JSON file

        Probabilities must add up to 1.

        Probability keys are in the following format:
            Y* = Yes, can be law/important
            N* = No, can't be law/not important
            *L = Left
            *R = Right
            *M = Middle

        Example JSON file:
            {
            "statements": [
                {
                "actionable": "n",
                "group_label": "l",
                "votes": "0",
                "statement": "Statement 0",
                },
                {"..."}
                {
                "actionable": "n",
                "group_label": "c",
                "votes": "0",
                "statement": "Statement N",
                }
            ],
            "probabilities": {
                "YL": 0.1,
                "YR": 0.1,
                "*L": 0.1,
                "*R": 0.1,
                "YM": 0.2,
                "*M": 0.2,
                "**": 0.2
            }
            }
        """
        if self.filename == filename:
            return
        self.filename = filename
        with open(filename, 'r') as file:
            data = json.load(file)
        self.statements = data["statements"]
        self.probabilities = data["probabilities"]
        self._extract_actionable_keys()
        self._extract_group_label_keys()
        self._validate_statements_and_probabilities()
        self._build_statements_map()

    def _clear_unique_statements_list(self):
        """Clear the list of previously selected statements"""
        self.statement_uuid_list = []
        return True  # Indicate that the list has been cleared successfully

    def _select_next_statement(self, key, previous_uuid_list=None):
        """
        Pick a new statement from a statement set

        Picks the first unused statement from the statement set, which is
        sorted elsewhere (e.g. by votes).

        Will pick an alternative key if the key is not found.
        First will look for same group_label, then same actionable, then any.
        """
        if previous_uuid_list is None:
            previous_uuid_list = []

        # Handle case if key is not in the statements_map
        if key not in self.statements_map:
            # Logic for key not found
            return None

        for statement in self.statements_map[key]:
            if statement["uuid"] not in self.statement_uuid_list and statement["uuid"] not in previous_uuid_list:
                self.statement_uuid_list.append(statement["uuid"])
                return statement

        # Handle case if no valid statement was found
        # Try alternative keys or return None depending on your logic

        # return statement that matches key if possible
        alternative_keys = [
            f'*{key[1]}',
            f'{key[0]}*',
            '**'
        ]
        for alt_key in alternative_keys:
            for statement in self.statements_map.get(alt_key, []):
                if statement["uuid"] not in self.statement_uuid_list and statement["uuid"] not in previous_uuid_list:
                    LOG.debug(f"{key} not available, using {alt_key} instead.")
                    self.statement_uuid_list.append(statement["uuid"])
                    return statement
        # return None if no statements available
        LOG.error("No more statements available.")
        return None

    def _build_statement_list(
            self,
            num_statements,
            previous_uuid_list=[],
            clear_unique_statements=True):
        """Generate a list of statements num_statements long"""
        self.statement_list = []
        if clear_unique_statements:
            self._clear_unique_statements_list()
        key_list = []
        while len(key_list) < num_statements:
            key_list.extend(np.random.choice(
                list(self.probabilities.keys()),
                size=len(self.probabilities),
                replace=False,
                p=list(self.probabilities.values())))
        key_list = key_list[:num_statements]
        for key in key_list:
            statement = self._select_next_statement(
                key,
                previous_uuid_list=previous_uuid_list)
            if statement is None:
                break
            self.statement_list.append(statement)

    def get_statement_list(self, num_statements):
        """Return a list of statements num_statements long"""
        self._build_statement_list(num_statements)
        return [s['statement'] for s in self.statement_list]
# class JS_Survey(

if __name__ == "__main__":
    # @TODO: move to tests
    LOG.setLevel(logging.DEBUG)
    statements = Statements()
    statements.read_from_json("statements.json")
    print(statements.statements[0])
    print(statements.probabilities)
    print('probabilities keys:', list(statements.probabilities.keys()))
    print('test')
    max_count = 10
    for _ in range(max_count):
        for key in list(statements.probabilities.keys()):
            print(f'key: {key}', end=': ')
            statement = statements._select_next_statement(key)
            if statement:
                print(f'{statement["actionable"]}{statement["group_label"]} {statement["statement"][:70]}')
            else:
                print('None')
                print('resetting statement list')
                statements._clear_unique_statements_list()

    element_lengths = [5, 4, 10, 6, 12, 50, 70]
    for element_length in element_lengths:
        print()
        print(f"building {element_length} unit statement list")
        statements._build_statement_list(element_length)
        # print('statement list:', statements.statement_list)
        # print('statement uuid list:', statements.statement_uuid_list)
        print()
        print(f"          element_length: {element_length}")
        print(f"length of statement list: {len(statements.statement_list)}")
        print('statement actionable list:', [s['actionable'] for s in statements.statement_list])
        print('statement group label list:', [s['group_label'] for s in statements.statement_list])
        print('statement votes list:', [s['votes'] for s in statements.statement_list])
    elements = 5
    print(f"{elements} unit statement list:")
    print(statements.get_statement_list(elements))