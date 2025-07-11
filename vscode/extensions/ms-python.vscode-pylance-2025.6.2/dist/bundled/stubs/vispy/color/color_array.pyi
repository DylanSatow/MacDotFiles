from collections.abc import Sequence
from copy import deepcopy
from typing import Literal

import numpy as np

from ..util import logger
from ._color_dict import _color_dict
from .color_space import (  # noqa
    _hex_to_rgba,
    _hsv_to_rgb,
    _lab_to_rgb,
    _rgb_to_hex,
    _rgb_to_hsv,  # noqa
    _rgb_to_lab,
)

# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

###############################################################################
# User-friendliness helpers

def _string_to_rgb(color): ...
def _user_to_rgba(color, expand=True, clip=False): ...
def _array_clip_val(val): ...

###############################################################################
# Color Array

class ColorArray:
    def __init__(
        self,
        color: str | tuple | Sequence = ...,
        alpha: None | float = None,
        clip: bool = False,
        color_space: Literal["hsv", "rgb"] = "rgb",
    ): ...

    ###########################################################################
    # Builtins and utilities
    def copy(self): ...
    @classmethod
    def _name(cls): ...
    def __len__(self): ...
    def __repr__(self): ...
    def __eq__(self, other): ...

    ###########################################################################
    def __getitem__(self, item): ...
    def __setitem__(self, item, value): ...
    def extend(self, colors: ColorArray): ...

    # RGB(A)
    @property
    def rgba(self): ...
    @rgba.setter
    def rgba(self, val): ...
    @property
    def rgb(self): ...
    @rgb.setter
    def rgb(self, val): ...
    @property
    def RGBA(self): ...
    @RGBA.setter
    def RGBA(self, val): ...
    @property
    def RGB(self): ...
    @RGB.setter
    def RGB(self, val): ...
    @property
    def alpha(self): ...
    @alpha.setter
    def alpha(self, val): ...

    ###########################################################################
    # HEX
    @property
    def hex(self): ...
    @hex.setter
    def hex(self, val): ...

    ###########################################################################
    # HSV
    @property
    def hsv(self): ...
    @hsv.setter
    def hsv(self, val): ...
    @property
    def _hsv(self): ...
    @property
    def value(self): ...
    @value.setter
    def value(self, val): ...
    def lighter(self, dv: float = 0.1, copy: bool = True) -> ColorArray: ...
    def darker(self, dv: float = 0.1, copy: bool = True) -> ColorArray: ...

    ###########################################################################
    # Lab
    @property
    def lab(self): ...
    @lab.setter
    def lab(self, val): ...

class Color(ColorArray):
    def __init__(
        self,
        color: str | tuple = "black",
        alpha: None | float = None,
        clip: bool = False,
    ): ...
    @ColorArray.rgba.getter  # type: ignore[attr-defined] # python/mypy#5936
    def rgba(self): ...
    @ColorArray.rgb.getter  # type: ignore[attr-defined] # python/mypy#5936
    def rgb(self): ...
    @ColorArray.RGBA.getter  # type: ignore[attr-defined] # python/mypy#5936
    def RGBA(self): ...
    @ColorArray.RGB.getter  # type: ignore[attr-defined] # python/mypy#5936
    def RGB(self): ...
    @ColorArray.alpha.getter  # type: ignore[attr-defined] # python/mypy#5936
    def alpha(self): ...
    @ColorArray.hex.getter  # type: ignore[attr-defined] # python/mypy#5936
    def hex(self): ...
    @ColorArray.hsv.getter  # type: ignore[attr-defined] # python/mypy#5936
    def hsv(self): ...
    @ColorArray.value.getter  # type: ignore[attr-defined] # python/mypy#5936
    def value(self): ...
    @ColorArray.lab.getter  # type: ignore[attr-defined] # python/mypy#5936
    def lab(self): ...
    @property
    def is_blank(self): ...
    def __repr__(self): ...
