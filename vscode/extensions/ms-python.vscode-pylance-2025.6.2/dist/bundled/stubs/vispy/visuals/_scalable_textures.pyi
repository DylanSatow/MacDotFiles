# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

import numpy as np
from numpy.typing import NDArray

from ..gloo import Texture2D, Texture3D

def get_default_clim_from_dtype(dtype): ...
def get_default_clim_from_data(data): ...

class _ScaledTextureMixin:
    def __init__(self, data: np.ndarray | tuple | None = None, **texture_kwargs): ...
    def init_scaling_texture(self, data=None, internalformat=None, **texture_kwargs): ...
    def _get_texture_format_for_data(self, data, internalformat): ...
    @property
    def clim(self): ...
    def set_clim(self, clim): ...
    @property
    def clim_normalized(self): ...
    @property
    def is_normalized(self): ...
    def normalize_value(self, val: NDArray | float, input_data_dtype: np.dtype): ...
    def _data_num_channels(self, data): ...
    def _create_rep_array(self, data): ...
    def check_data_format(self, data): ...
    def scale_and_set_data(self, data, offset=None, copy=False): ...

class CPUScaledTextureMixin(_ScaledTextureMixin):
    def __init__(self, data=None, **texture_kwargs): ...
    def _clim_outside_data_limits(self, cmin, cmax): ...
    def set_clim(self, clim): ...
    @property
    def clim_normalized(self): ...
    @staticmethod
    def _scale_data_on_cpu(data, clim, copy=True): ...
    def scale_and_set_data(self, data, offset=None, copy=True): ...

class GPUScaledTextureMixin(_ScaledTextureMixin):
    # dtype -> internalformat
    # 'r' will be replaced (if needed) with rgb or rgba depending on number of bands
    _texture_dtype_format: dict = ...
    # instance variable that will be used later on
    _auto_texture_format: bool = ...

    def _handle_auto_texture_format(self, texture_format, data): ...
    def _get_gl_tex_format(self, texture_format, num_channels): ...
    def _get_texture_format_for_data(self, data, internalformat): ...
    def _compute_clim(self, data): ...
    def _internalformat_will_change(self, data): ...
    def check_data_format(self, data): ...
    def _reformat_if_necessary(self, data): ...
    def scale_and_set_data(self, data, offset=None, copy=False): ...

class CPUScaledTexture2D(CPUScaledTextureMixin, Texture2D): ...
class GPUScaledTexture2D(GPUScaledTextureMixin, Texture2D): ...
class CPUScaledTexture3D(CPUScaledTextureMixin, Texture3D): ...
class GPUScaledTextured3D(GPUScaledTextureMixin, Texture3D): ...
