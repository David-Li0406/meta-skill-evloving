#!/usr/bin/env -S uv --script
# /// script
# dependencies = ["lxml>=5.3.0"]
# ///
"""Targeted XML edits with XPath. Minimal formatting changes."""

from __future__ import annotations

import argparse
from typing import Callable, List

from lib import (
    apply_attr_surgical,
    apply_delete,
    apply_insert,
    apply_replace,
    apply_text_surgical,
    child_tag_counts,
    decode_lines,
    decode_text,
    element_inner_xml,
    element_outer_xml,
    encode_text,
    ensure_elements,
    expand_paths,
    fail,
    limit,
    outline_lines,
    parse_doc,
    parse_ns,
    read_text_arg,
    read_xml_fragment,
    select,
    serialize,
    show_diff,
    summarize,
    truncate,
)


def common_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Targeted XML edits with XPath")
    p.add_argument("paths", nargs="+", help="XML file paths or glob patterns")
    p.add_argument("--xpath", required=True, help="XPath to select elements")
    p.add_argument("--ns", action="append", default=[], help="Namespace prefix=uri")
    p.add_argument("--limit", type=int, help="Limit matches per file")
    p.add_argument("--huge", action="store_true", help="Allow huge trees")
    p.add_argument("--recover", action="store_true", help="Recover from XML errors")
    return p


def mutate_files(
    args: argparse.Namespace,
    mutator: Callable[[List], int],
) -> int:
    ns_map = parse_ns(args.ns)
    paths = expand_paths(args.paths)
    if not paths:
        fail("no files matched")
    for path in paths:
        tree, original, has_decl, enc = parse_doc(path, args.huge, args.recover)
        items = select(tree, args.xpath, ns_map)
        items = limit(items, args.limit)
        elements = ensure_elements(items)
        changed = mutator(elements)
        updated = serialize(tree, has_decl, enc)
        wrote = False
        if changed and args.in_place:
            with open(path, "wb") as f:
                f.write(updated)
            wrote = True
        if args.diff and changed:
            show_diff(path, original, updated)
        summarize(path, len(elements), changed, wrote)
    return 0


def cmd_select(args: argparse.Namespace) -> int:
    ns_map = parse_ns(args.ns)
    paths = expand_paths(args.paths)
    if not paths:
        fail("no files matched")
    for path in paths:
        tree, _, _, _ = parse_doc(path, args.huge, args.recover)
        items = select(tree, args.xpath, ns_map)
        items = limit(items, args.limit)
        print(f"{path}: {len(items)} match(es)")
        for idx, item in enumerate(items, 1):
            if hasattr(item, "tag"):
                tag = item.tag
                line = item.sourceline or 0
                print(f"  [{idx}] <{tag}> line {line}")
            else:
                print(f"  [{idx}] {item}")
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    ns_map = parse_ns(args.ns)
    paths = expand_paths(args.paths)
    if not paths:
        fail("no files matched")
    for path in paths:
        tree, _, _, _ = parse_doc(path, args.huge, args.recover)
        items = select(tree, args.xpath, ns_map)
        items = limit(items, args.limit)
        print(f"{path}:")
        for idx, item in enumerate(items, 1):
            if hasattr(item, "tag"):
                if args.attr:
                    print(f"  [{idx}] {item.get(args.attr, '')}")
                else:
                    print(f"  [{idx}] {item.text or ''}")
            else:
                print(f"  [{idx}] {item}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    ns_map = parse_ns(args.ns)
    paths = expand_paths(args.paths)
    if not paths:
        fail("no files matched")
    for path in paths:
        tree, _, _, _ = parse_doc(path, args.huge, args.recover)
        items = select(tree, args.xpath, ns_map)
        items = limit(items, args.limit)
        elements = ensure_elements(items)
        print(f"{path}: {len(elements)} match(es)")
        for idx, el in enumerate(elements, 1):
            if not args.no_header:
                line = el.sourceline or 0
                print(f"  [{idx}] <{el.tag}> line {line}")
            if args.inner:
                out = element_inner_xml(el, args.pretty)
            else:
                out = element_outer_xml(el, args.pretty)
            out = truncate(out, args.max_chars)
            print(out)
            if idx < len(elements):
                print("---")
    return 0


def cmd_children(args: argparse.Namespace) -> int:
    ns_map = parse_ns(args.ns)
    paths = expand_paths(args.paths)
    if not paths:
        fail("no files matched")
    for path in paths:
        tree, _, _, _ = parse_doc(path, args.huge, args.recover)
        items = select(tree, args.xpath, ns_map)
        items = limit(items, args.limit)
        elements = ensure_elements(items)
        print(f"{path}: {len(elements)} match(es)")
        for idx, el in enumerate(elements, 1):
            line = el.sourceline or 0
            print(f"  [{idx}] <{el.tag}> line {line}")
            if args.list:
                for child in el:
                    c_line = child.sourceline or 0
                    attrs = ""
                    if args.attrs and child.attrib:
                        attrs = " " + " ".join(
                            f"{k}={v!r}" for k, v in sorted(child.attrib.items())
                        )
                    print(f"    - <{child.tag}> line {c_line}{attrs}")
            else:
                for tag, count in child_tag_counts(el):
                    print(f"    {tag}: {count}")
    return 0


def cmd_outline(args: argparse.Namespace) -> int:
    ns_map = parse_ns(args.ns)
    paths = expand_paths(args.paths)
    if not paths:
        fail("no files matched")
    for path in paths:
        tree, _, _, _ = parse_doc(path, args.huge, args.recover)
        items = select(tree, args.xpath, ns_map)
        items = limit(items, args.limit)
        elements = ensure_elements(items)
        print(f"{path}: {len(elements)} match(es)")
        for idx, el in enumerate(elements, 1):
            line = el.sourceline or 0
            print(f"  [{idx}] <{el.tag}> line {line}")
            for out in outline_lines(
                el,
                args.depth,
                args.attr,
                args.max_children,
                args.max_nodes,
                include_root=False,
            ):
                print(f"    {out}")
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    ns_map = parse_ns(args.ns)
    paths = expand_paths(args.paths)
    if not paths:
        fail("no files matched")
    for path in paths:
        tree, original, _, enc = parse_doc(path, args.huge, args.recover)
        items = select(tree, args.xpath, ns_map)
        items = limit(items, args.limit)
        elements = ensure_elements(items)
        lines = decode_lines(original, enc)
        print(f"{path}: {len(elements)} match(es)")
        for idx, el in enumerate(elements, 1):
            line = el.sourceline or 0
            if line <= 0:
                print(f"  [{idx}] <{el.tag}> line unknown")
                continue
            start = max(1, line - args.before)
            end = min(len(lines), line + args.after)
            if not args.no_header:
                print(f"  [{idx}] <{el.tag}> lines {start}-{end}")
            for ln in range(start, end + 1):
                prefix = ">>" if ln == line else "  "
                print(f"{prefix} {ln:6d} | {lines[ln - 1]}")
            if idx < len(elements):
                print("---")
    return 0


def cmd_set_text(args: argparse.Namespace) -> int:
    value = read_text_arg(args.value, args.value_file)
    ns_map = parse_ns(args.ns)
    paths = expand_paths(args.paths)
    if not paths:
        fail("no files matched")
    for path in paths:
        tree, original, _, enc = parse_doc(path, args.huge, args.recover)
        items = select(tree, args.xpath, ns_map)
        items = limit(items, args.limit)
        elements = ensure_elements(items)
        text = decode_text(original, enc)
        updated_text, changed = apply_text_surgical(text, elements, value)
        updated = encode_text(updated_text, enc)
        wrote = False
        if changed and args.in_place:
            with open(path, "wb") as f:
                f.write(updated)
            wrote = True
        if args.diff and changed:
            show_diff(path, original, updated)
        summarize(path, len(elements), changed, wrote)
    return 0


def cmd_set_attr(args: argparse.Namespace) -> int:
    value = read_text_arg(args.value, args.value_file)
    ns_map = parse_ns(args.ns)
    paths = expand_paths(args.paths)
    if not paths:
        fail("no files matched")
    for path in paths:
        tree, original, _, enc = parse_doc(path, args.huge, args.recover)
        items = select(tree, args.xpath, ns_map)
        items = limit(items, args.limit)
        elements = ensure_elements(items)
        text = decode_text(original, enc)
        updated_text, changed = apply_attr_surgical(
            text, elements, args.name, value, True
        )
        updated = encode_text(updated_text, enc)
        wrote = False
        if changed and args.in_place:
            with open(path, "wb") as f:
                f.write(updated)
            wrote = True
        if args.diff and changed:
            show_diff(path, original, updated)
        summarize(path, len(elements), changed, wrote)
    return 0


def cmd_del_attr(args: argparse.Namespace) -> int:
    ns_map = parse_ns(args.ns)
    paths = expand_paths(args.paths)
    if not paths:
        fail("no files matched")
    for path in paths:
        tree, original, _, enc = parse_doc(path, args.huge, args.recover)
        items = select(tree, args.xpath, ns_map)
        items = limit(items, args.limit)
        elements = ensure_elements(items)
        text = decode_text(original, enc)
        updated_text, changed = apply_attr_surgical(
            text, elements, args.name, None, False
        )
        updated = encode_text(updated_text, enc)
        wrote = False
        if changed and args.in_place:
            with open(path, "wb") as f:
                f.write(updated)
            wrote = True
        if args.diff and changed:
            show_diff(path, original, updated)
        summarize(path, len(elements), changed, wrote)
    return 0


def cmd_insert(args: argparse.Namespace) -> int:
    if not args.reformat_ok:
        fail("insert reserializes XML and may reformat; pass --reformat-ok to proceed")
    nodes = read_xml_fragment(args.xml, args.xml_file)

    def mutator(elements: List) -> int:
        return apply_insert(elements, nodes, args.position, args.indent)

    return mutate_files(args, mutator)


def cmd_replace(args: argparse.Namespace) -> int:
    if not args.reformat_ok:
        fail("replace reserializes XML and may reformat; pass --reformat-ok to proceed")
    nodes = read_xml_fragment(args.xml, args.xml_file)

    def mutator(elements: List) -> int:
        return apply_replace(elements, nodes, args.indent)

    return mutate_files(args, mutator)


def cmd_delete(args: argparse.Namespace) -> int:
    if not args.reformat_ok:
        fail("delete reserializes XML and may reformat; pass --reformat-ok to proceed")
    def mutator(elements: List) -> int:
        return apply_delete(elements)

    return mutate_files(args, mutator)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Targeted XML edits with XPath")
    sub = parser.add_subparsers(dest="command", required=True)

    select_p = common_parser()
    select_p.set_defaults(func=cmd_select)
    sub.add_parser("select", parents=[select_p], add_help=False)

    get_p = common_parser()
    get_p.add_argument("--attr", help="Attribute name (defaults to text)")
    get_p.set_defaults(func=cmd_get)
    sub.add_parser("get", parents=[get_p], add_help=False)

    show_p = common_parser()
    show_p.add_argument("--inner", action="store_true", help="Show inner XML")
    show_p.add_argument("--pretty", action="store_true", help="Pretty print output")
    show_p.add_argument("--no-header", action="store_true", help="Omit match headers")
    show_p.add_argument("--max-chars", type=int, help="Truncate output per match")
    show_p.set_defaults(func=cmd_show)
    sub.add_parser("show", parents=[show_p], add_help=False)

    children_p = common_parser()
    children_p.add_argument("--list", action="store_true", help="List each child")
    children_p.add_argument("--attrs", action="store_true", help="Show child attrs")
    children_p.set_defaults(func=cmd_children)
    sub.add_parser("children", parents=[children_p], add_help=False)

    outline_p = common_parser()
    outline_p.add_argument(
        "--depth",
        type=int,
        default=2,
        help="Depth to print below each match",
    )
    outline_p.add_argument(
        "--attr",
        action="append",
        default=[],
        help="Attribute to include in outline (repeatable)",
    )
    outline_p.add_argument(
        "--max-children",
        type=int,
        help="Limit children per node",
    )
    outline_p.add_argument(
        "--max-nodes",
        type=int,
        help="Limit total nodes printed per match",
    )
    outline_p.set_defaults(func=cmd_outline)
    sub.add_parser("outline", parents=[outline_p], add_help=False)

    context_p = common_parser()
    context_p.add_argument(
        "--before",
        type=int,
        default=3,
        help="Lines before the match line",
    )
    context_p.add_argument(
        "--after",
        type=int,
        default=3,
        help="Lines after the match line",
    )
    context_p.add_argument("--no-header", action="store_true", help="Omit headers")
    context_p.set_defaults(func=cmd_context)
    sub.add_parser("context", parents=[context_p], add_help=False)

    set_text_p = common_parser()
    set_text_p.add_argument("--value")
    set_text_p.add_argument("--value-file")
    set_text_p.add_argument("--diff", action="store_true", help="Show unified diff")
    set_text_p.add_argument("--in-place", action="store_true", help="Write changes in place")
    set_text_p.set_defaults(func=cmd_set_text)
    sub.add_parser("set-text", parents=[set_text_p], add_help=False)

    set_attr_p = common_parser()
    set_attr_p.add_argument("--name", required=True)
    set_attr_p.add_argument("--value")
    set_attr_p.add_argument("--value-file")
    set_attr_p.add_argument("--diff", action="store_true", help="Show unified diff")
    set_attr_p.add_argument("--in-place", action="store_true", help="Write changes in place")
    set_attr_p.set_defaults(func=cmd_set_attr)
    sub.add_parser("set-attr", parents=[set_attr_p], add_help=False)

    del_attr_p = common_parser()
    del_attr_p.add_argument("--name", required=True)
    del_attr_p.add_argument("--diff", action="store_true", help="Show unified diff")
    del_attr_p.add_argument("--in-place", action="store_true", help="Write changes in place")
    del_attr_p.set_defaults(func=cmd_del_attr)
    sub.add_parser("del-attr", parents=[del_attr_p], add_help=False)

    insert_p = common_parser()
    insert_p.add_argument("--xml")
    insert_p.add_argument("--xml-file")
    insert_p.add_argument(
        "--position",
        choices=["before", "after", "inside-first", "inside-last"],
        default="after",
    )
    insert_p.add_argument("--indent", help="Override whitespace after inserted nodes")
    insert_p.add_argument(
        "--reformat-ok",
        action="store_true",
        help="Acknowledge that XML will be reserialized",
    )
    insert_p.add_argument("--diff", action="store_true", help="Show unified diff")
    insert_p.add_argument("--in-place", action="store_true", help="Write changes in place")
    insert_p.set_defaults(func=cmd_insert)
    sub.add_parser("insert", parents=[insert_p], add_help=False)

    replace_p = common_parser()
    replace_p.add_argument("--xml")
    replace_p.add_argument("--xml-file")
    replace_p.add_argument("--indent", help="Override whitespace after inserted nodes")
    replace_p.add_argument(
        "--reformat-ok",
        action="store_true",
        help="Acknowledge that XML will be reserialized",
    )
    replace_p.add_argument("--diff", action="store_true", help="Show unified diff")
    replace_p.add_argument("--in-place", action="store_true", help="Write changes in place")
    replace_p.set_defaults(func=cmd_replace)
    sub.add_parser("replace", parents=[replace_p], add_help=False)

    delete_p = common_parser()
    delete_p.add_argument(
        "--reformat-ok",
        action="store_true",
        help="Acknowledge that XML will be reserialized",
    )
    delete_p.add_argument("--diff", action="store_true", help="Show unified diff")
    delete_p.add_argument("--in-place", action="store_true", help="Write changes in place")
    delete_p.set_defaults(func=cmd_delete)
    sub.add_parser("delete", parents=[delete_p], add_help=False)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
