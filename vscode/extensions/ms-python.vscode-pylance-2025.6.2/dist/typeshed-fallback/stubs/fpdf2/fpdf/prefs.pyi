from typing import Literal

from .enums import Duplex, PageBoundaries, PageMode, TextDirection

class ViewerPreferences:
    hide_toolbar: bool
    hide_menubar: bool
    hide_window_u_i: bool
    fit_window: bool
    center_window: bool
    def __init__(
        self,
        hide_toolbar: bool = False,
        hide_menubar: bool = False,
        hide_window_u_i: bool = False,
        fit_window: bool = False,
        center_window: bool = False,
        display_doc_title: bool = False,
        non_full_screen_page_mode: PageMode | str | None = ...,
        num_copies: int | None = None,
        print_page_range: list[int] | None = None,
        direction: TextDirection | str | None = None,
        duplex: Duplex | str | None = None,
        view_area: PageBoundaries | None = None,
        view_clip: PageBoundaries | None = None,
        print_area: PageBoundaries | None = None,
        print_clip: PageBoundaries | None = None,
        print_scaling=None,
    ) -> None: ...
    @property
    def non_full_screen_page_mode(self) -> PageMode | None: ...
    @non_full_screen_page_mode.setter
    def non_full_screen_page_mode(self, page_mode: PageMode | str | None) -> None: ...
    @property
    def num_copies(self) -> int | None: ...
    @num_copies.setter
    def num_copies(self, num_copies: int | None) -> None: ...
    @property
    def print_page_range(self) -> list[int] | None: ...
    @print_page_range.setter
    def print_page_range(self, print_page_range: list[int] | None) -> None: ...
    @property
    def direction(self) -> TextDirection | None: ...
    @direction.setter
    def direction(self, direction: TextDirection | str | None) -> None: ...
    @property
    def display_doc_title(self) -> bool: ...
    @display_doc_title.setter
    def display_doc_title(self, display_doc_title: bool) -> None: ...
    @property
    def duplex(self) -> Duplex | None: ...
    @duplex.setter
    def duplex(self, duplex: Duplex | str | None) -> None: ...
    @property
    def view_area(self) -> PageBoundaries | None: ...
    @view_area.setter
    def view_area(self, view_area: PageBoundaries | str | None) -> None: ...
    @property
    def view_clip(self) -> PageBoundaries | None: ...
    @view_clip.setter
    def view_clip(self, view_area: PageBoundaries | str | None) -> None: ...
    @property
    def print_area(self) -> PageBoundaries | None: ...
    @print_area.setter
    def print_area(self, view_area: PageBoundaries | str | None) -> None: ...
    @property
    def print_clip(self) -> PageBoundaries | None: ...
    @print_clip.setter
    def print_clip(self, view_area: PageBoundaries | str | None) -> None: ...
    @property
    def print_scaling(self) -> Literal["None", "AppDefault"] | None: ...
    @print_scaling.setter
    def print_scaling(self, print_scaling: Literal["None", "AppDefault"] | None) -> None: ...
    def serialize(self) -> str: ...
