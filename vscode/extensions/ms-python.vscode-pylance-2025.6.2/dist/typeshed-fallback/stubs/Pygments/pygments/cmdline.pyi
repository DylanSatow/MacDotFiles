import argparse

def main_inner(parser, argns): ...

class HelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog, indent_increment: int = 2, max_help_position: int = 16, width=None) -> None: ...

def main(args=...): ...
