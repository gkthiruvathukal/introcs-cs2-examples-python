# Stack TUI

## Purpose

`data_structures/tui/stack_app.py` is an interactive terminal app for experimenting with a stack by pushing, popping, peeking, and viewing the current contents.

It uses the same core stack operations as the stack demo, but presents them in a Textual-based interface with:

- a visual stack panel
- a command log
- a command input box
- capped stack viewing with pinned-top scrolling
- batch push and random data generation commands
- session save/load commands
- convenience stack operations such as `at`, `dup`, `swap`, `rotate`, and `clear`
- snapshot-based `undo` and `redo`
- per-command timing in the log

## Running the App

Install dependencies first:

```bash
make install
```

Run the TUI:

```bash
make run-stack-app
```

You can also run the module directly:

```bash
.venv/bin/python -m data_structures.tui.stack_app
```

By default, the app shows up to 8 stack rows at a time.
The default type constraint is `int`.

## Command-Line Options

### `--max-size N`

Set the maximum number of items allowed in the stack.

Example:

```bash
.venv/bin/python -m data_structures.tui.stack_app --max-size 20
```

### `--view-top N`

Show at most `N` stack cells in the visual panel while keeping the true top item visible.

If the stack grows beyond `N`, the panel does not keep expanding vertically. Instead:

- the top item stays visible
- the remaining visible rows show older items below it
- you can scroll through older items without losing the top marker

Example:

```bash
.venv/bin/python -m data_structures.tui.stack_app --view-top 5
```

If you omit `--view-top`, the default is `8`.

### Random generation range options

These options control `/random` generation:

- `--int-min N`
- `--int-max N`
- `--float-min X`
- `--float-max X`

They are used when the current type is `int`, `float`, or `any`.
They do not affect `bool` or `str` random generation.

Example:

```bash
.venv/bin/python -m data_structures.tui.stack_app \
  --int-min 0 --int-max 100 \
  --float-min -10.0 --float-max 10.0
```

## Layout

The interface has three main parts:

1. A stack panel at the top that shows the current stack visually.
2. A log panel in the middle that records command results and errors.
3. An input box at the bottom where commands are entered.

The stack is displayed from top to bottom in three columns:

- an `offset` column showing the displacement from the real top
- a `value` column showing the stored element
- a `type` column showing the runtime type of the stored value

The first visible row is always labeled `top`.
If the stack has at least two elements, the last visible row is always the true `bottom`.
Rows in between are labeled `top-1`, `top-2`, and so on.
If the stack has exactly one element, that row is labeled `top=bottom`.
Because the default type is `int`, plain numeric pushes such as `/push 1 2 3` become integers unless you switch the type with `/type`.
If a displayed value is longer than 40 characters, the panel truncates it with `...`. The full value is still available through `/peek` or `/at`.

## How the Code Is Put Together

The implementation lives in [data_structures/tui/stack_app.py](/Volumes/Work/introcs-cs2-examples-python/data_structures/tui/stack_app.py:1). The main pieces are:

- `StackDemo`: the stack model, including push/pop/peek, capacity, and optional type conversion
- `parse_push_values(...)`, `build_random_values(...)`, `save_session(...)`, `load_session(...)`, `snapshot_stack(...)`, and `restore_stack(...)`: helpers for command parsing, random generation, persistence, and undo/redo
- `build_stack_view(...)`: a pure helper that decides which items are visible
- `StackPanel`: the widget that renders the ASCII stack view
- `StackDemoTUI`: the Textual app that wires widgets, commands, and scrolling together

### 1. The App Starts from a Small CLI Parser

The parser accepts size, viewport, and random-generation bounds, then passes them into the app:

```python
def build_parser() -> argparse.ArgumentParser:
    ...
    parser.add_argument("--view-top", type=positive_int, default=8, metavar="N")
    parser.add_argument("--int-min", type=int, default=INT32_MIN, metavar="N")
    parser.add_argument("--int-max", type=int, default=INT32_MAX, metavar="N")
    parser.add_argument("--float-min", type=float, default=FLOAT32_MIN, metavar="X")
    parser.add_argument("--float-max", type=float, default=FLOAT32_MAX, metavar="X")
    return parser
```

This keeps the random-data policy configurable without changing the in-app command syntax.

### 2. The Stack Model Stays Separate from the Viewport Logic

The stack object is still just a stack. It does not know anything about scrolling or visible windows:

```python
class StackDemo:
    def __init__(self, max_size=1000):
        self.stack = []
        self.max_size = max_size
        self.element_type = int

    def push(self, item):
        return self.push_many([item])[0]

    def push_many(self, items):
        converted_items = [self._convert_item(item) for item in items]
        if len(self.stack) + len(converted_items) > self.max_size:
            raise OverflowError(f"Stack overflow: capacity is {self.max_size}")
        self.stack.extend(converted_items)
        return converted_items
```

That split keeps the design simple:

- `StackDemo` owns stack behavior
- `StackDemoTUI` owns viewport behavior

Batch pushes are validated before mutation, so a bad conversion or overflow does not partially update the stack.
Boolean conversion uses explicit parsing instead of Python's default truthiness rules, so values like `true`, `yes`, `1`, `false`, `no`, and `0` map to actual booleans.

### 3. Batch Input and Random Data Are Built with Helpers

`/push` now accepts multiple values and quoted strings because the argument is tokenized with `shlex`:

```python
def parse_push_values(arg: str):
    values = shlex.split(arg)
    if not values:
        raise ValueError("Usage: /push <value> [more values ...]")
    return values
```

`/random` generates values based on the current type:

```python
def build_random_values(...):
    if element_type is int:
        return [rng.randint(int_min, int_max) for _ in range(count)]
    if element_type is float:
        return [rng.uniform(float_min, float_max) for _ in range(count)]
    if element_type is str:
        return [rng.choice(words) for _ in range(count)]
    ...
```

Behavior by type:

- `int`: random integers in the configured integer range
- `float`: random floating-point values in the configured float range
- `str`: random English words from `data/words.txt`
- `bool`: random `True`/`False` values
- `any`: a mixed stream of integers, floats, booleans, and words

For `bool`, accepted push values include common forms such as `true`, `false`, `yes`, `no`, `1`, `0`, `on`, and `off`.

The app starts in `int` mode. Use `/type bool` for booleans or `/type any` if you want unconstrained values.

### 4. The Viewport Helper Computes What the Panel Should Show

The pinned-top behavior is implemented in `build_stack_view(...)`:

```python
def build_stack_view(stack_items, view_top=None, scroll_offset: int = 0):
    items = list(reversed(stack_items))
    if view_top is None or len(items) <= view_top:
        return {"visible_items": items, ...}

    if view_top == 1:
        return {"visible_items": items[:1], ...}

    older_items = items[1:]
    window_size = view_top - 1
    offset = clamp_scroll_offset(len(items), view_top, scroll_offset)
    visible_older = older_items[offset:offset + window_size]

    return {
        "visible_items": [items[0], *visible_older],
        ...
    }
```

Important details:

- `items[0]` is always the real stack top
- if the stack has at least two elements, the real bottom is also always visible
- only the middle rows between top and bottom are allowed to move
- `scroll_offset` changes which middle items are shown

This is the core of the new `--view-top` behavior.

### 5. The Panel Turns View Data into a Three-Column Stack Table

`StackPanel.refresh_stack(...)` asks for a view, then renders a header, hidden-item indicators, and a three-column table:

```python
view = build_stack_view(demo.stack, view_top=view_top, scroll_offset=scroll_offset)
items = view["visible_items"]

rendered_values = [format_display_value(item) for item in items]
type_labels = [type(item).__name__ for item in items]

lines.append(f"  ┌...┬...┬...┐")
lines.append(f"  │ offset │ value │ type │")
lines.append(f"  ├...┼...┼...┤")
for i, (item, rendered_value, type_label) in enumerate(...):
    label = self._format_offset_label(i, view)
    lines.append(f"  │ {label} │ {rendered_value} │ {type_label} │")
lines.append(f"  └...┴...┴...┘")
```

The label for each visible row is based on the true displacement from the top, not just the row position in the current viewport.

That means a scrolled view can show labels like `top-3`, `top-4`, and `bottom`, which makes both position and stack boundaries immediately clear.
Long values are truncated only for display; the underlying stored value is unchanged.

### 6. Textual Wires the Widgets Together in `compose()`

The app layout is declared in one place:

```python
def compose(self) -> ComposeResult:
    yield Header()
    yield StackPanel(id="panel")
    yield RichLog(id="log", highlight=True, markup=True)
    yield Input(
        placeholder="/help  /push <v...>  /random <n>  /pop  /peek  /at <index>  /dup  /swap  /rotate  /clear  /save <file>  /load <file>  /undo  /redo  /type [int|float|str|bool|any]  /quit"
    )
    yield Footer()
```

That corresponds directly to what you see on screen:

- header
- stack panel
- log
- command input
- footer

### 7. Commands Flow Through a Single Dispatcher

When the user presses Enter, Textual sends an `Input.Submitted` event:

```python
@on(Input.Submitted)
def handle_command(self, event: Input.Submitted) -> None:
    raw = event.value.strip()
    self.query_one(Input).clear()
    if raw:
        self._dispatch(raw)
        self._refresh_panel()
```

The command string then goes through `_dispatch(...)`, which handles verbs like `/push`, `/random`, `/save`, `/load`, `/undo`, `/redo`, `/show`, `/pop`, `/type`, and the viewport commands:

```python
if verb == "/push":
    pushed = self.demo.push_many(parse_push_values(arg))

elif verb == "/random":
    values = build_random_values(...)
    pushed = self.demo.push_many(values)

elif verb == "/save":
    save_session(path, self.demo)

elif verb == "/load":
    type_name, items = load_session(path)
    self.demo = restore_stack({"type": type_name, "items": items}, self.demo.max_size)

elif verb == "/undo":
    self._undo()

elif verb == "/redo":
    self._redo()

elif verb in ("/show", "/print"):
    ...
```

This keeps the app logic centralized instead of scattering command behavior across multiple widgets.

### 8. Keybindings Use the Same Scrolling Path

Keyboard navigation does not have separate viewport logic. The bound actions call the same helper:

```python
def action_scroll_up(self) -> None:
    self._scroll_by(1)

def action_page_up(self) -> None:
    self._scroll_by(self._page_size())
```

That means `/up` and the `Up` key behave the same way, and `/pageup` matches `PageUp`.

### 9. Viewport State Is Clamped Before Rendering

The app keeps the scroll state valid with two small helpers:

```python
def _clamp_scroll_offset(self) -> None:
    self.scroll_offset = clamp_scroll_offset(
        self.demo.size(),
        self.view_top,
        self.scroll_offset,
    )

def _refresh_panel(self) -> None:
    self._clamp_scroll_offset()
    self.query_one(StackPanel).refresh_stack(
        self.demo,
        view_top=self.view_top,
        scroll_offset=self.scroll_offset,
    )
```

This avoids invalid offsets after pushes, pops, or scrolling near the ends of the stack.

## Commands

Enter commands in the bottom input box.

| Command | Meaning |
|---|---|
| `/push <value> [more ...]` | Push one or more values onto the stack |
| `/push "hello world" foo bar` | Push quoted and unquoted string values in one command |
| `/random <n>` | Push `n` random values based on the current type constraint |
| `/pop` | Pop the top value |
| `/peek` | Show the current top value without removing it |
| `/at <index>` | Show the value at zero-based offset `0, 1, 2, ...` from the top |
| `/dup` | Duplicate the current top value |
| `/swap` | Swap the top two values |
| `/rotate` | Rotate the top three values so the third item becomes the new top |
| `/clear` | Remove all values from the stack |
| `/save <path>` | Save the current type constraint and stack contents to a session file |
| `/load <path>` | Load a saved session into a fresh stack, replacing the current stack |
| `/undo` | Restore the previous stack/type state |
| `/redo` | Reapply the most recently undone stack/type state |
| `/show` or `/print` | Print the stack contents in top-to-bottom order in the log |
| `/type` | Show the current type constraint |
| `/type int` | Convert future pushed values to `int` |
| `/type float` | Convert future pushed values to `float` |
| `/type str` | Convert future pushed values to `str` |
| `/type bool` | Convert future pushed values to `bool` |
| `/type any` | Remove the type constraint |
| `/up` | Scroll to older hidden items when `--view-top` is active |
| `/down` | Scroll back toward the newest visible window |
| `/pageup` | Scroll older items by one page |
| `/pagedown` | Scroll newer items by one page |
| `/home` | Reset the viewport to the newest visible window |
| `/help` | Show the command summary |
| `/quit` or `/exit` | Exit the app |

Every submitted command also logs its execution time using an automatically scaled unit such as `ns`, `us`, `ms`, or `s`.

## Keybindings

These keybindings work in addition to slash commands:

| Key | Meaning |
|---|---|
| `Ctrl+D` | Quit |
| `Up` | Scroll to older items |
| `Down` | Scroll to newer items |
| `PageUp` | Scroll older items by one page |
| `PageDown` | Scroll newer items by one page |
| `Home` | Reset to the newest visible window |

The scroll keys only matter when `--view-top` is active and the stack has more items than can be shown at once.

## How Pinned-Top Viewing Works

The default viewport size is 8. When `--view-top N` is used:

- the panel shows at most `N` stack entries
- the top item is always visible
- if the stack has at least two elements, the bottom item is also always visible
- the remaining rows are used for middle items between top and bottom
- if there are hidden middle items, the panel shows hidden-item indicators
- the header reports the current visible older-item range

For example, suppose the stack from top to bottom is:

```text
[9, 8, 7, 6, 5, 4]
```

With `--view-top 3`, the default visible window is:

```text
offset  value  type
top       9    int
top-1     8    int
bottom    4    int
```

If you scroll older items once page-by-page or row-by-row, the top remains pinned and the older rows move:

```text
offset  value  type
top       9    int
top-2     7    int
bottom    4    int
```

Scrolling never changes which elements are the true stack top and bottom. It only changes which middle elements are shown between them.

## Typical Session

Example workflow:

```text
/push 10 20 30
/at 1
/dup
/swap
/rotate
/save session.json
/peek
/clear
/load session.json
/undo
/redo
/random 3
/pop
/type int
/push 40 50 60
/show
```

Expected behavior:

- the stack panel updates after each command
- `/at 1` inspects the value one level below the top
- `/dup`, `/swap`, and `/rotate` perform classic stack-manipulation operations
- `/save session.json` writes the current type constraint and stack contents to disk
- `/load session.json` replaces the current stack with the saved session
- `/undo` restores the previous state and `/redo` reapplies an undone state
- `/peek` reports the top value in the log
- `/random 3` pushes three values suitable for the current type
- `/pop` removes the top value and logs it
- `/type int` makes future pushed values convert to integers
- `/show` prints the stack in top-to-bottom order
- `/undo` and `/redo` restore both stack contents and the current type constraint

## Errors and Edge Cases

- Popping or peeking an empty stack raises an underflow-style message in the log.
- `/at` requires a non-negative index and reports out-of-range access clearly.
- `dup` on an empty stack raises an underflow-style message in the log.
- `swap` requires at least two stack items.
- `rotate` requires at least three stack items.
- `/load` restores into a fresh stack rather than merging with existing contents.
- A saved session stores the current type constraint and stack contents.
- Pushing past `--max-size` raises an overflow-style message in the log.
- `dup` can also overflow if the stack is already full.
- Pushing a value that cannot be converted under the current type constraint raises a type error in the log.
- Batch pushes are atomic: the whole `/push` fails if one value is invalid or the stack would overflow.
- `/random <n>` requires a positive integer count.
- `/redo` only reapplies a state that was previously undone; it does not repeat the last command by itself.
- Any new mutating command after an undo clears the redo history.
- `--view-top` must be a positive integer.

## Verification Notes

The viewport-selection and argument-parsing logic are covered by `tests/test_stack_app.py`.

The app also runs under the local project virtual environment created by `make install`.
