from typing import Any

ROOT: int
AND: int
OR: int
NOT: int
MATCH_APPROX: int
MATCH_GREATER_OR_EQUAL: int
MATCH_LESS_OR_EQUAL: int
MATCH_EXTENSIBLE: int
MATCH_PRESENT: int
MATCH_SUBSTRING: int
MATCH_EQUAL: int
SEARCH_OPEN: int
SEARCH_OPEN_OR_CLOSE: int
SEARCH_MATCH_OR_CLOSE: int
SEARCH_MATCH_OR_CONTROL: int

class FilterNode:
    tag: Any
    parent: Any
    assertion: Any
    elements: Any
    def __init__(self, tag=None, assertion=None) -> None: ...
    def __str__(self, pos: int = 0) -> str: ...
    def __repr__(self, pos: int = 0) -> str: ...
    def append(self, filter_node): ...

def evaluate_match(match, schema, auto_escape, auto_encode, validator, check_names): ...
def parse_filter(search_filter, schema, auto_escape, auto_encode, validator, check_names): ...
def compile_filter(filter_node): ...
def build_attribute_selection(attribute_list, schema): ...
def search_operation(
    search_base,
    search_filter,
    search_scope,
    dereference_aliases,
    attributes,
    size_limit,
    time_limit,
    types_only,
    auto_escape,
    auto_encode,
    schema=None,
    validator=None,
    check_names: bool = False,
): ...
def decode_vals(vals): ...
def decode_vals_fast(vals): ...
def attributes_to_dict(attribute_list): ...
def attributes_to_dict_fast(attribute_list): ...
def decode_raw_vals(vals): ...
def decode_raw_vals_fast(vals): ...
def raw_attributes_to_dict(attribute_list): ...
def raw_attributes_to_dict_fast(attribute_list): ...
def checked_attributes_to_dict(attribute_list, schema=None, custom_formatter=None): ...
def checked_attributes_to_dict_fast(attribute_list, schema=None, custom_formatter=None): ...
def matching_rule_assertion_to_string(matching_rule_assertion): ...
def filter_to_string(filter_object): ...
def search_request_to_dict(request): ...
def search_result_entry_response_to_dict(response, schema, custom_formatter, check_names): ...
def search_result_done_response_to_dict(response): ...
def search_result_reference_response_to_dict(response): ...
def search_result_entry_response_to_dict_fast(response, schema, custom_formatter, check_names): ...
def search_result_reference_response_to_dict_fast(response): ...
