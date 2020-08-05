# Best practices for the Python part
1. If you add any requirement, remember to add it (with its version) to `requirements.txt`.
1. If you add any configurable setting, *especially mandatory ones*,
    1. ensure the code has a fall-back, if the setting has a reasonable default,
    1. *always* document it in `README.md`.
1. When possible, use the builtin `typing` module for type annotations. Together with a linter it prevents many
 mistakes.

# Code style guidelines for the Python part
1. Generally, follow PEP8. Use an IDE or linter that encourages you towards that end.
1. Run `black .` before committing to have a more uniform formatting. (`pip install black`)
1. Keep lines roughly below 90 columns.
1. Indentation is 4 spaces. If you use tabs, ensure *black* or your IDE converts it into spaces.
1. Docstrings: see below.
1. Either British or American spelling is fine.
1. Use Python 3 conventions: we don't need support for Python 2 (e.g. no need to inherit from `object` explicitly).
1. For string interpolation, prefer fstrings:
    ```python
    some_var = 123
    my_string = f"This is an fstring and the number is {some_var}."
    ```
 since they're faster and more readable. If the expression inside {} is complicated, split it in its own variable or
 use `"".format()`.
1. For long collections, put a trailing comma on the last line (this way, adding stuff doesn't require editing existing
 code):
    ```python
    some_list = [
        1,
        2,
        3,
    ]
    ```
1. For long function calls, break at the parentheses and put arguments on their own line:
    ```python
    some_long_method(
        "with",
        "a",
        "long",
        "signature",
    )
    ```

## Docstrings
1. Prefer comments on their own line *above* the code, instead of on the same line as the code.
    ```python
    # This is a good comment.
    some_method()
    ```
1. Optionally, indent multiple lines of the same block to show that they should be read together.
    ```python
    # As an example,
    #  this is one comment, and
    #  as you can see it's easier to follow
    #  when it's slightly indented and properly punctuated.
    # As opposed to another adjacent block, which is clearly
    #  separate because it resets indentation and starts with a capital.
    ```
1. If your comment is about a specific identifier, use a docstring instead (see below).

### Modules
Add a docstring at the top of each module to briefly explain what it contains. Follow
 the same style as for classes (below).

### Classes
```python
class SomeClass:
    """One-liners have quotes on the same line."""

    # And one empty line.


class SomeOtherClass:
    """Docs on
    multiple
    lines
    end with quotes on a separate line.
    """
```

### Methods and functions
```python
def some_method():
    """One-liners on one line."""
    # But no extra whitespace.

def some_other_method():
    """Multiple lines
    of docs
    behave as for classes.
    """

    # Including the empty line.
```

### Other identifiers
```python
class SomeClass:
    an_attribute = "hello"
    """Using docstrings on attributes is really useful with IDEs that can show them
    on the fly (e.g. ctrl-q on PyCharm when cursor is on an_attribute would show this).
    """

    def some_method(self):
        my_var = 123
        """This can also be annotated. Do it instead of a comment if it's about my_var."""
```
