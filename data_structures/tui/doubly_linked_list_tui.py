import argparse

from textual.app import ComposeResult
from textual.widgets import Footer, Header, Input, RichLog, Static

from data_structures.doubly_linked_list import DoublyLinkedList
from .tui_common import (
    BaseLinearStructureTUI,
    build_linear_parser,
    format_display_value,
    format_value_batch,
    get_type_name,
    nonnegative_int,
    parse_value_tokens,
)


def build_dll_snapshots(items, visible_indices, item_count):
    snapshots = []
    previous_index = None

    for item, index in zip(items, visible_indices):
        if previous_index is not None and index - previous_index > 1:
            hidden_count = index - previous_index - 1
            snapshots.append(
                {
                    "kind": "gap",
                    "hidden_count": hidden_count,
                }
            )

        snapshots.append(
            {
                "kind": "node",
                "index": index,
                "node_id": item["node_id"],
                "node_label": item["node_label"],
                "data": item["data"],
                "prev_label": item["prev_label"],
                "next_label": item["next_label"],
            }
        )
        previous_index = index

    return snapshots


def build_dll_cards(snapshots):
    cards = []
    for snapshot in snapshots:
        if snapshot["kind"] == "gap":
            hidden_text = f"{snapshot['hidden_count']} hidden"
            rows = ["...", hidden_text, "...", "..."]
            width = max(len(row) for row in rows)
            cards.append(
                [
                    f"┌{'─' * (width + 2)}┐",
                    *(f"│ {row:^{width}} │" for row in rows),
                    f"└{'─' * (width + 2)}┘",
                ]
            )
            continue

        data_text = format_display_value(snapshot["data"])
        rows = [
            f"id: {snapshot['node_label']}",
            f"data: {data_text}",
            f"prev: {snapshot['prev_label']}",
            f"next: {snapshot['next_label']}",
        ]
        width = max(len(row) for row in rows)
        cards.append(
            [
                f"┌{'─' * (width + 2)}┐",
                *(f"│ {row:<{width}} │" for row in rows),
                f"└{'─' * (width + 2)}┘",
            ]
        )
    return cards


def estimate_horizontal_width(cards):
    if not cards:
        return 0
    connector_width = len(" <-> ")
    return sum(len(card[0]) for card in cards) + connector_width * (len(cards) - 1)


def render_horizontal_dll(cards):
    if not cards:
        return ["(empty)"]

    connector = " <-> "
    total_width = estimate_horizontal_width(cards)
    starts = []
    cursor = 0
    for card in cards:
        starts.append(cursor)
        cursor += len(card[0]) + len(connector)

    label_line = [" "] * total_width
    head = "head"
    tail = "tail"
    head_start = max(starts[0] + (len(cards[0][0]) - len(head)) // 2, 0)
    for i, char in enumerate(head):
        if head_start + i < total_width:
            label_line[head_start + i] = char
    tail_start = max(starts[-1] + (len(cards[-1][0]) - len(tail)) // 2, 0)
    for i, char in enumerate(tail):
        if tail_start + i < total_width:
            label_line[tail_start + i] = char

    lines = ["".join(label_line).rstrip()]
    connector_row = len(cards[0]) // 2
    for row_index in range(len(cards[0])):
        parts = []
        for card_index, card in enumerate(cards):
            parts.append(card[row_index])
            if card_index < len(cards) - 1:
                parts.append(connector if row_index == connector_row else " " * len(connector))
        lines.append("".join(parts))
    return lines


def gap_card(hidden_count):
    hidden_text = f"{hidden_count} hidden"
    rows = ["...", hidden_text, "...", "..."]
    width = max(len(row) for row in rows)
    return [
        f"┌{'─' * (width + 2)}┐",
        *(f"│ {row:^{width}} │" for row in rows),
        f"└{'─' * (width + 2)}┘",
    ]


def build_horizontal_dll_view(items, available_width: int, scroll_offset: int, anchor_target: int = 2):
    item_count = len(items)
    if item_count == 0:
        return {
            "visible_items": [],
            "visible_indices": [],
            "hidden_before": 0,
            "hidden_after": 0,
            "scroll_offset": 0,
            "item_count": 0,
            "render_width": 0,
            "middle_window_size": 0,
        }

    full_cards = build_dll_cards(build_dll_snapshots(items, list(range(item_count)), item_count))
    total_full_width = estimate_horizontal_width(full_cards)
    if total_full_width <= available_width:
        return {
            "visible_items": list(items),
            "visible_indices": list(range(item_count)),
            "hidden_before": 0,
            "hidden_after": 0,
            "scroll_offset": 0,
            "item_count": item_count,
            "render_width": total_full_width,
            "middle_window_size": max(item_count - 4, 0),
        }

    for anchor_count in (anchor_target, 1):
        left_count = min(anchor_count, item_count)
        right_count = min(anchor_count, max(item_count - left_count, 0))
        middle_start_min = left_count
        middle_end_max = item_count - right_count
        middle_count = max(middle_end_max - middle_start_min, 0)

        if middle_count <= 0:
            visible_indices = list(range(item_count))
            visible_items = list(items)
            render_width = estimate_horizontal_width(build_dll_cards(build_dll_snapshots(visible_items, visible_indices, item_count)))
            if render_width <= available_width:
                return {
                    "visible_items": visible_items,
                    "visible_indices": visible_indices,
                    "hidden_before": 0,
                    "hidden_after": 0,
                    "scroll_offset": 0,
                    "item_count": item_count,
                    "render_width": render_width,
                    "middle_window_size": 0,
                }
            continue

        max_middle_len = middle_count
        clamped_offset = min(max(scroll_offset, 0), max(middle_count - 1, 0))
        middle_start = middle_start_min + clamped_offset

        for middle_len in range(max_middle_len, -1, -1):
            middle_end = min(middle_start + middle_len, middle_end_max)
            left_hidden = max(middle_start - middle_start_min, 0)
            right_hidden = max(middle_end_max - middle_end, 0)

            visible_indices = list(range(left_count))
            visible_items = [items[index] for index in visible_indices]

            if left_hidden > 0:
                visible_indices.append(middle_start - 1)
                visible_items.append({"kind": "gap", "hidden_count": left_hidden})

            middle_indices = list(range(middle_start, middle_end))
            visible_indices.extend(middle_indices)
            visible_items.extend(items[index] for index in middle_indices)

            if right_hidden > 0:
                visible_indices.append(middle_end)
                visible_items.append({"kind": "gap", "hidden_count": right_hidden})

            tail_indices = list(range(item_count - right_count, item_count))
            visible_indices.extend(tail_indices)
            visible_items.extend(items[index] for index in tail_indices)

            snapshots = []
            for item, index in zip(visible_items, visible_indices):
                if isinstance(item, dict) and item.get("kind") == "gap":
                    snapshots.append(item)
                else:
                    snapshots.extend(build_dll_snapshots([item], [index], item_count))

            cards = build_dll_cards(snapshots)
            render_width = estimate_horizontal_width(cards)
            if render_width <= available_width:
                actual_visible_items = [item for item in visible_items if not (isinstance(item, dict) and item.get("kind") == "gap")]
                actual_visible_indices = [index for item, index in zip(visible_items, visible_indices) if not (isinstance(item, dict) and item.get("kind") == "gap")]
                return {
                    "visible_items": actual_visible_items,
                    "visible_indices": actual_visible_indices,
                    "hidden_before": left_hidden,
                    "hidden_after": right_hidden,
                    "scroll_offset": clamped_offset,
                    "item_count": item_count,
                    "render_width": render_width,
                    "middle_window_size": max(len(middle_indices), 1),
                }

    return {
        "visible_items": [items[0], items[-1]] if item_count > 1 else [items[0]],
        "visible_indices": [0, item_count - 1] if item_count > 1 else [0],
        "hidden_before": 0,
        "hidden_after": max(item_count - 2, 0),
        "scroll_offset": 0,
        "item_count": item_count,
        "render_width": available_width,
        "middle_window_size": 1,
    }


class DoublyLinkedListPanel(Static):
    def refresh_doubly_linked_list(self, *, header: str, items, view_top=None, scroll_offset: int = 0) -> None:
        available_width = max(self.size.width - 4, 20)
        view = build_horizontal_dll_view(items, available_width, scroll_offset)
        snapshots = build_dll_snapshots(view["visible_items"], view["visible_indices"], view["item_count"])
        cards = build_dll_cards(snapshots)
        render_width = estimate_horizontal_width(cards)

        rendered_header = header
        if view["hidden_before"] > 0 or view["hidden_after"] > 0:
            rendered_header += f"  visible nodes: {len(view['visible_items'])}/{view['item_count']}"
        rendered_header += f"  render-width: {render_width}"

        lines = render_horizontal_dll(cards)
        self.last_render_width = render_width
        self.last_middle_window_size = view["middle_window_size"]
        self.last_hidden_before = view["hidden_before"]
        self.last_hidden_after = view["hidden_after"]
        self.last_scroll_offset = view["scroll_offset"]
        self.update(rendered_header + "\n" + "\n".join(f"  {line}" for line in lines))


class DoublyLinkedListTUI(BaseLinearStructureTUI):
    CSS = """
    DoublyLinkedListPanel {
        height: auto;
        min-height: 10;
        border: solid $primary;
        padding: 0 1;
        margin-bottom: 1;
    }
    RichLog {
        height: 1fr;
        border: solid $panel;
    }
    Input {
        margin-top: 1;
    }
    """

    STRUCTURE_NAME = "Doubly Linked List"
    START_LABEL = "head"
    END_LABEL = "tail"

    def __init__(self, **kwargs):
        self.demo = DoublyLinkedList()
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        yield DoublyLinkedListPanel(id="panel")
        yield RichLog(id="log", highlight=True, markup=True)
        yield Input(placeholder=self.placeholder_text())
        yield Footer()

    def get_items(self) -> list:
        return self.demo.to_list()

    def append_values(self, values) -> None:
        if self.structure_size() + len(values) > self.max_size:
            raise OverflowError(f"Doubly linked list overflow: capacity is {self.max_size}")
        for value in values:
            self.demo.insert(value)

    def clear_structure(self) -> None:
        self.demo.clear()

    def replace_items(self, items) -> None:
        self.demo = DoublyLinkedList()
        self.append_values(self._convert_many(items))

    def _snapshot_state(self) -> dict:
        return {
            "type": get_type_name(self.element_type),
            "nodes": self.demo.node_snapshots(),
            "items": list(self.get_items()),
        }

    def _restore_snapshot(self, snapshot: dict) -> None:
        self.set_type(snapshot["type"])
        node_snapshots = snapshot.get("nodes")
        if node_snapshots is not None:
            self.demo = DoublyLinkedList()
            self.demo.restore_from_snapshots(node_snapshots)
        else:
            self.replace_items(snapshot["items"])
        self.scroll_offset = 0

    def show_state_text(self) -> str:
        items = self.get_items()
        if not items:
            return "None <- head/tail -> None"
        return "None <- " + " <-> ".join(repr(item) for item in items) + " -> None"

    def placeholder_text(self) -> str:
        return "/help  /append <v...>  /insert-at <i> <v>  /insert-after <id> <v>  /insert-before <id> <v>  /remove-at <i>  /remove-node <id>  /remove-value <v>  /search <v>  /at <i>  /show-backward  /quit"

    def help_lines(self) -> list[str]:
        return [
            "  [cyan]/append[/cyan] VALUE [VALUE ...]            add one or more values at the tail",
            "  [cyan]/insert-at[/cyan] INDEX VALUE               insert before position (0 = new head)",
            "  [cyan]/insert-after[/cyan] NODE-ID VALUE          insert after the node with that id",
            "  [cyan]/insert-before[/cyan] NODE-ID VALUE         insert before the node with that id",
            "  [cyan]/remove-at[/cyan] INDEX                     remove the node at position index",
            "  [cyan]/remove-node[/cyan] NODE-ID                 remove the node with that id",
            "  [cyan]/remove-value[/cyan] VALUE                  remove the first matching node",
            "  [cyan]/search[/cyan] VALUE                        search for a value",
            "  [cyan]/at[/cyan] INDEX                            inspect 0,1,2,... relative to the head",
            "  [cyan]/show-backward[/cyan]                       display values from tail to head",
        ]

    def handle_structure_command(self, verb: str, arg: str | None, log: RichLog) -> bool:
        if verb == "/append":
            if arg is None:
                log.write("[red]Usage: /append <value> [more values ...][/red]")
                return True
            try:
                self._record_undo_state()
                values = self._convert_many(parse_value_tokens(arg, "Usage: /append <value> [more values ...]"))
                self.append_values(values)
                self.scroll_offset = 0
                log.write(
                    f"[green]append({len(values)} values) added {format_value_batch(values)}  "
                    f"{self.show_state_text()}  size={self.structure_size()}[/green]"
                )
            except (OverflowError, TypeError, ValueError) as e:
                label = "Overflow" if isinstance(e, OverflowError) else "TypeError" if isinstance(e, TypeError) else None
                log.write(f"[red]{f'{label}: ' if label else ''}{e}[/red]")
            return True

        if verb == "/insert-at":
            if arg is None:
                log.write("[red]Usage: /insert-at <index> <value>[/red]")
                return True
            try:
                tokens = parse_value_tokens(arg, "Usage: /insert-at <index> <value>", 2, 2)
                index = nonnegative_int(tokens[0])
                value = self._convert_item(tokens[1])
                self._record_undo_state()
                self.demo.insert_at(index, value)
                self.scroll_offset = 0
                log.write(f"[green]insert-at({index}, {value!r})  {self.show_state_text()}  size={self.structure_size()}[/green]")
            except (IndexError, OverflowError, TypeError, ValueError, argparse.ArgumentTypeError) as e:
                log.write(f"[red]{e}[/red]")
            return True

        if verb == "/insert-after":
            if arg is None:
                log.write("[red]Usage: /insert-after <node-id> <value>[/red]")
                return True
            try:
                tokens = parse_value_tokens(arg, "Usage: /insert-after <node-id> <value>", 2, 2)
                node_id = nonnegative_int(tokens[0])
                value = self._convert_item(tokens[1])
                self._record_undo_state()
                self.demo.insert_after(node_id, value)
                self.scroll_offset = 0
                log.write(f"[green]insert-after(node-{node_id}, {value!r})  {self.show_state_text()}  size={self.structure_size()}[/green]")
            except (OverflowError, TypeError, ValueError, argparse.ArgumentTypeError) as e:
                log.write(f"[red]{e}[/red]")
            return True

        if verb == "/insert-before":
            if arg is None:
                log.write("[red]Usage: /insert-before <node-id> <value>[/red]")
                return True
            try:
                tokens = parse_value_tokens(arg, "Usage: /insert-before <node-id> <value>", 2, 2)
                node_id = nonnegative_int(tokens[0])
                value = self._convert_item(tokens[1])
                self._record_undo_state()
                self.demo.insert_before(node_id, value)
                self.scroll_offset = 0
                log.write(f"[green]insert-before(node-{node_id}, {value!r})  {self.show_state_text()}  size={self.structure_size()}[/green]")
            except (OverflowError, TypeError, ValueError, argparse.ArgumentTypeError) as e:
                log.write(f"[red]{e}[/red]")
            return True

        if verb == "/remove-at":
            if arg is None:
                log.write("[red]Usage: /remove-at <index>[/red]")
                return True
            try:
                index = nonnegative_int(arg)
                self._record_undo_state()
                self.demo.remove_at(index)
                self.scroll_offset = 0
                log.write(f"[green]remove-at({index})  {self.show_state_text()}  size={self.structure_size()}[/green]")
            except (IndexError, argparse.ArgumentTypeError, ValueError) as e:
                log.write(f"[red]{e}[/red]")
            return True

        if verb == "/remove-node":
            if arg is None:
                log.write("[red]Usage: /remove-node <node-id>[/red]")
                return True
            try:
                node_id = nonnegative_int(arg)
                self._record_undo_state()
                self.demo.remove_by_node_id(node_id)
                self.scroll_offset = 0
                log.write(f"[green]remove-node(node-{node_id})  {self.show_state_text()}  size={self.structure_size()}[/green]")
            except (argparse.ArgumentTypeError, ValueError) as e:
                log.write(f"[red]{e}[/red]")
            return True

        if verb == "/remove-value":
            if arg is None:
                log.write("[red]Usage: /remove-value <value>[/red]")
                return True
            try:
                value = self._convert_many(parse_value_tokens(arg, "Usage: /remove-value <value>", 1, 1))[0]
                self._record_undo_state()
                self.demo.remove(value)
                log.write(f"[green]remove-value({value!r})  {self.show_state_text()}  size={self.structure_size()}[/green]")
            except (ValueError, TypeError) as e:
                label = "TypeError" if isinstance(e, TypeError) else None
                log.write(f"[red]{f'{label}: ' if label else ''}{e}[/red]")
            return True

        if verb == "/search":
            if arg is None:
                log.write("[red]Usage: /search <value>[/red]")
                return True
            try:
                value = self._convert_many(parse_value_tokens(arg, "Usage: /search <value>", 1, 1))[0]
                result = self.demo.find(value)
                if result is None:
                    log.write(f"[cyan]search({value!r}) → not found[/cyan]")
                else:
                    index, node_id = result
                    log.write(f"[cyan]search({value!r}) → found at index {index}  node-id: {node_id}[/cyan]")
            except TypeError as e:
                log.write(f"[red]TypeError: {e}[/red]")
            return True

        if verb == "/at":
            if arg is None:
                log.write("[red]Usage: /at <non-negative-index>[/red]")
                return True
            try:
                index = nonnegative_int(arg)
                items = self.get_items()
                if index >= len(items):
                    raise IndexError(f"At index {index} is out of range for list size {len(items)}")
                log.write(f"[cyan]at({index}) → {items[index]!r}[/cyan]")
            except (argparse.ArgumentTypeError, ValueError) as e:
                log.write(f"[red]{e}[/red]")
            except IndexError as e:
                log.write(f"[red]RangeError: {e}[/red]")
            return True

        if verb == "/show-backward":
            log.write(f"[cyan]tail → head: {self.demo.display_backward()!r}[/cyan]")
            return True

        return False

    def _refresh_panel(self) -> None:
        self._clamp_scroll_offset()
        header = f"{self.STRUCTURE_NAME} ({self.structure_size()}/{self.max_size})  type: {get_type_name(self.element_type)}"
        panel = self.query_one(DoublyLinkedListPanel)
        panel.refresh_doubly_linked_list(
            header=header,
            items=self.demo.node_snapshots(),
            view_top=self.view_top,
            scroll_offset=self.scroll_offset,
        )
        if self.is_mounted:
            self._log_render_metrics()

    def _clamp_scroll_offset(self) -> None:
        if not self.is_mounted:
            self.scroll_offset = 0
            return
        panel = self.query_one(DoublyLinkedListPanel)
        available_width = max(panel.size.width - 4, 20)
        view = build_horizontal_dll_view(self.demo.node_snapshots(), available_width, self.scroll_offset)
        self.scroll_offset = view["scroll_offset"]

    def _can_scroll(self) -> bool:
        if not self.is_mounted:
            return False
        panel = self.query_one(DoublyLinkedListPanel)
        available_width = max(panel.size.width - 4, 20)
        view = build_horizontal_dll_view(self.demo.node_snapshots(), available_width, self.scroll_offset)
        return (view["hidden_before"] + view["hidden_after"]) > 0

    def _page_size(self) -> int:
        if not self.is_mounted:
            return 1
        panel = self.query_one(DoublyLinkedListPanel)
        available_width = max(panel.size.width - 4, 20)
        view = build_horizontal_dll_view(self.demo.node_snapshots(), available_width, self.scroll_offset)
        return max(view["middle_window_size"], 1)

    def _log_render_metrics(self) -> None:
        panel = self.query_one(DoublyLinkedListPanel)
        log = self.query_one(RichLog)
        render_width = getattr(panel, "last_render_width", 0)
        hidden_before = getattr(panel, "last_hidden_before", 0)
        hidden_after = getattr(panel, "last_hidden_after", 0)
        log.write(
            f"[dim]render width: {render_width} chars  hidden-left: {hidden_before}  hidden-right: {hidden_after}[/dim]"
        )


def main() -> None:
    parser = build_linear_parser("Interactive Doubly Linked List Demo")
    args = parser.parse_args()
    if args.int_min > args.int_max:
        parser.error("--int-min must be less than or equal to --int-max")
    if args.float_min > args.float_max:
        parser.error("--float-min must be less than or equal to --float-max")
    DoublyLinkedListTUI(
        max_size=args.max_size,
        view_top=args.view_top,
        int_min=args.int_min,
        int_max=args.int_max,
        float_min=args.float_min,
        float_max=args.float_max,
    ).run()


if __name__ == "__main__":
    main()
