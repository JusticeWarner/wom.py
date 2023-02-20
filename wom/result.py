# wom.py - An asynchronous wrapper for the Wise Old Man API.
# Copyright (c) 2023-present Jonxslays
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This module contains the [`Result`][wom.Result] variants returned by all
[`Client`][wom.Client] calls.
"""

from __future__ import annotations

import abc
import typing as t

from wom import errors

__all__ = ("Err", "Ok", "Result")

T = t.TypeVar("T")
E = t.TypeVar("E")


class Result(t.Generic[T, E], abc.ABC):
    """Represents a potential [`Ok`][wom.Ok] or [`Err`][wom.Err] result.

    !!! note

        This class cannot be instantiated, only its children can be.

    ??? Example

        ```py
        if result.is_ok:
            print(result.unwrap())
        else:
            print(result.unwrap_err())
        ```
    """

    __slots__ = ("_error", "_value")

    def __init__(self, value: T, error: E) -> None:
        # This is really only here because mypy cant infer from slots
        self._value = value
        self._error = error

    def __repr__(self) -> str:
        inner = self._value if self.is_ok else self._error
        return f"{self.__class__.__name__}({inner})"

    @property
    @abc.abstractmethod
    def is_ok(self) -> bool:
        """`True` if this result is the :obj:`Ok` variant."""

    @property
    @abc.abstractmethod
    def is_err(self) -> bool:
        """`True` if this result is the :obj:`Err` variant."""

    @abc.abstractmethod
    def unwrap(self) -> T:
        """Unwraps the result to produce the value.

        Returns:
            `T`: The unwrapped value.

        Raises:
            `UnwrapError`: If the result was an :obj:`Err`,
                and not :obj:`Ok`.
        """

    @abc.abstractmethod
    def unwrap_err(self) -> E:
        """Unwraps the result to produce the error.

        Returns:
            `E`: The unwrapped error.

        Raises:
            `UnwrapError`: If the result was an :obj:`Ok`,
                and not an :obj:`Err`.
        """


@t.final
class Ok(Result[T, E]):
    """The [`Ok`][wom.Ok] variant of a [`Result`][wom.Result]."""

    __slots__ = ()

    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_err(self) -> E:
        raise errors.UnwrapError(f"Called unwrap error on an non error value - {self._value}")


@t.final
class Err(Result[T, E]):
    """The [`Err`][wom.Err] variant of a [`Result`][wom.Result]."""

    __slots__ = ()

    def __init__(self, error: E) -> None:
        self._error = error

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def is_err(self) -> bool:
        return True

    def unwrap(self) -> T:
        raise errors.UnwrapError(f"Called unwrap on an error value - {self._error}")

    def unwrap_err(self) -> E:
        return self._error
