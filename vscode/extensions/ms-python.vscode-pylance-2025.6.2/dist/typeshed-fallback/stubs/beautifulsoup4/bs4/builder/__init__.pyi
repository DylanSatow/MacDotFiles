from typing import Any

class TreeBuilderRegistry:
    builders_for_feature: Any
    builders: Any
    def __init__(self) -> None: ...
    def register(self, treebuilder_class) -> None: ...
    def lookup(self, *features): ...

class TreeBuilder:
    NAME: str
    ALTERNATE_NAMES: Any
    features: Any
    is_xml: bool
    picklable: bool
    empty_element_tags: Any
    DEFAULT_CDATA_LIST_ATTRIBUTES: Any
    DEFAULT_PRESERVE_WHITESPACE_TAGS: Any
    DEFAULT_STRING_CONTAINERS: Any
    USE_DEFAULT: Any
    TRACKS_LINE_NUMBERS: bool
    soup: Any
    cdata_list_attributes: Any
    preserve_whitespace_tags: Any
    store_line_numbers: Any
    string_containers: Any
    def __init__(
        self, multi_valued_attributes=..., preserve_whitespace_tags=..., store_line_numbers=..., string_containers=...
    ) -> None: ...
    def initialize_soup(self, soup) -> None: ...
    def reset(self) -> None: ...
    def can_be_empty_element(self, tag_name): ...
    def feed(self, markup) -> None: ...
    def prepare_markup(
        self, markup, user_specified_encoding=None, document_declared_encoding=None, exclude_encodings=None
    ) -> None: ...
    def test_fragment_to_document(self, fragment): ...
    def set_up_substitutions(self, tag): ...

class SAXTreeBuilder(TreeBuilder):
    def feed(self, markup) -> None: ...
    def close(self) -> None: ...
    def startElement(self, name, attrs) -> None: ...
    def endElement(self, name) -> None: ...
    def startElementNS(self, nsTuple, nodeName, attrs) -> None: ...
    def endElementNS(self, nsTuple, nodeName) -> None: ...
    def startPrefixMapping(self, prefix, nodeValue) -> None: ...
    def endPrefixMapping(self, prefix) -> None: ...
    def characters(self, content) -> None: ...
    def startDocument(self) -> None: ...
    def endDocument(self) -> None: ...

class HTMLTreeBuilder(TreeBuilder):
    empty_element_tags: Any
    block_elements: Any
    DEFAULT_STRING_CONTAINERS: Any
    DEFAULT_CDATA_LIST_ATTRIBUTES: Any
    DEFAULT_PRESERVE_WHITESPACE_TAGS: Any
    def set_up_substitutions(self, tag): ...

class ParserRejectedMarkup(Exception):
    def __init__(self, message_or_exception) -> None: ...

class XMLParsedAsHTMLWarning(UserWarning): ...
