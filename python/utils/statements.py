# standard packages
from abc import ABC, abstractmethod, abstractproperty
import json
from collections import defaultdict
import random


# third-party packages
import jsonschema

class AbstractStatements(ABC):
    """Abstract class for statements"""
    @abstractproperty
    def STATEMENTS_SCHEMA(self):
        pass

    @abstractproperty
    def PROBABILITIES_SCHEMA(self):
        pass

    def __init__(self):
        self.statements = []
        self.probabilities = {}
        self.actionable_keys = []
        self.group_label_keys = []
        self.statements_map = {}
        self.statement_list = []
        self.statement_uuid_list = []

    @abstractmethod
    def read_from_json(self):
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

    def validate_probability_keys(self):
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

    def validate_statements_and_probabilities(self):
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
        self.validate_probability_keys()
        total = 0
        for _, v in self.probabilities.items():
            total += v
        if total != 1:
            raise Exception("Probabilities must add up to 1")

    def extract_actionable_keys(self):
        """Extract the actionable keys"""
        keyset = set()
        for statement in self.statements:
            keyset.add(statement["actionable"].upper())
        self.actionable_keys = list(keyset)
        self.actionable_keys.sort()

    def extract_group_label_keys(self):
        """Extract the group label keys"""
        keyset = set()
        for statement in self.statements:
            keyset.add(statement["group_label"].upper())
        self.group_label_keys = list(keyset)
        self.group_label_keys.sort()

    def build_statements_map(self):
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
        with open(filename, 'r') as file:
            data = json.load(file)
        self.statements = data["statements"]
        self.probabilities = data["probabilities"]
        self.extract_actionable_keys()
        self.extract_group_label_keys()
        self.validate_statements_and_probabilities()
        self.build_statements_map()

    def select_statement(self, key):
        """Pick a statement from a statement set"""
        index = 0
        while self.statements_map[key][index]["uuid"] in self.statement_uuid_list:
            index += 1
        return self.statements_map[key][index]

    def build_statement_list(self, num_statements):
        """Generate a list of statements"""
        # TODO: code below works when num_statements is a multiple of 10
        # TODO: fix so it works for num_statements = 5 (pick 50/50)
        # TODO: fix so it works for num_statements = 3 (build list of 4) pick one
                # "YL": 0.1,
                # "YR": 0.1,
                # "*L": 0.1,
                # "*R": 0.1,
                # "YC": 0.2,
                # "*C": 0.2,
                # "**": 0.2
        #
        self.statement_list = []
        self.statement_uuid_list = []
        key_list = list(self.probabilities.keys())
        value_list = list(self.probabilities.values())
        statement_index = 0
        probability_index = 0
        probability_per_statement = 1 / num_statements
        elements = []
        weights = []
        while statement_index < num_statements:
            elements.append(key_list[probability_index])
            weights.append(value_list[probability_index])
            probability_index += 1
            sum_of_weights = sum(weights)
            remainder_key = None
            while sum_of_weights < probability_per_statement:
                probability_index += 1
                elements.append(key_list[probability_index])
                weights.append(value_list[probability_index])
                probability_index += 1
                sum_of_weights = sum(weights)
            if sum_of_weights > probability_per_statement:
                remainder_weight = sum_of_weights - probability_per_statement
                remainder_key = elements[-1]
                weights[-1] -= remainder_weight
            chosen_key = random.choices(elements, weights, k=1)[0]
            print(f"statement_index: {statement_index}; chosen_key: {chosen_key}; weights: {weights}; elements: {elements}")
            statement = self.select_statement(chosen_key)
            self.statement_list.append(statement)
            self.statement_uuid_list.append(statement["uuid"])
            statement_index += 1
            if remainder_key:
                elements = [remainder_key]
                weights = [remainder_weight]
            else:
                elements = []
                weights = []

# elements = ['a', 'b', 'c', 'd']
# weights = [0.1, 0.2, 0.3, 0.4]

# chosen_element = random.choices(elements, weights, k=1)[0]

if __name__ == "__main__":
    statements = Statements()
    statements.read_from_json("statements.json")
    print(statements.statements[0])
    print(statements.probabilities)
    statements.build_statement_list(5)
    statements.build_statement_list(10)
    statements.build_statement_list(11)
    statements.build_statement_list(4)
