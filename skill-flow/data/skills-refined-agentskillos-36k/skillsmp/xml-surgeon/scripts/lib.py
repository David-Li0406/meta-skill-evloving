from __future__ import annotations

import copy
import difflib
import glob
import re
import sys
from io import BytesIO
from typing import Iterable, List, Tuple

from lxml import etree
from xml.sax.saxutils import escape as xml_escape


def fail(msg: str, code: int = 2) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def detect_decl_and_encoding(data: bytes) -> Tuple[bool, str | None]:
    m = re.match(br"\s*<\?xml\s+[^>]*\?>", data)
    has_decl = bool(m)
    enc = None
    if has_decl:
        m2 = re.search(br"encoding=[\"']([^\"']+)[\"']", data[:200])
        if m2:
            enc = m2.group(1).decode("ascii", "ignore")
    return has_decl, enc


def parser(huge: bool, recover: bool) -> etree.XMLParser:
    return etree.XMLParser(
        remove_blank_text=False,
        huge_tree=huge,
        recover=recover,
        resolve_entities=False,
    )


def parse_doc(path: str, huge: bool, recover: bool) -> Tuple[etree._ElementTree, bytes, bool, str | None]:
    data = read_bytes(path)
    has_decl, enc = detect_decl_and_encoding(data)
    try:
        tree = etree.parse(BytesIO(data), parser(huge=huge, recover=recover))
    except etree.XMLSyntaxError as exc:
        fail(f"XML parse failed for {path}: {exc}")
    return tree, data, has_decl, enc


def serialize(tree: etree._ElementTree, has_decl: bool, enc: str | None) -> bytes:
    docinfo = tree.docinfo
    encoding = enc or docinfo.encoding or "utf-8"
    doctype = docinfo.doctype if docinfo.doctype else None
    buf = BytesIO()
    tree.write(
        buf,
        encoding=encoding,
        xml_declaration=has_decl,
        pretty_print=False,
        doctype=doctype,
    )
    return buf.getvalue()


def expand_paths(raw_paths: Iterable[str]) -> List[str]:
    paths: List[str] = []
    for raw in raw_paths:
        if any(ch in raw for ch in "*?[]"):
            matches = glob.glob(raw, recursive=True)
            paths.extend(sorted(matches))
        else:
            paths.append(raw)
    seen = set()
    out = []
    for p in paths:
        if p in seen:
            continue
        seen.add(p)
        out.append(p)
    return out


def parse_ns(ns_items: List[str]) -> dict:
    ns_map = {}
    for item in ns_items:
        if "=" not in item:
            fail(f"namespace must be prefix=uri: {item}")
        prefix, uri = item.split("=", 1)
        if not prefix or not uri:
            fail(f"namespace must be prefix=uri: {item}")
        ns_map[prefix] = uri
    return ns_map


def select(tree: etree._ElementTree, xpath: str, ns_map: dict) -> List:
    try:
        return tree.xpath(xpath, namespaces=ns_map)
    except etree.XPathEvalError as exc:
        fail(f"XPath error: {exc}")


def ensure_elements(items: List) -> List[etree._Element]:
    elements = [x for x in items if isinstance(x, etree._Element)]
    if len(elements) != len(items):
        fail("XPath must select elements for this operation")
    return elements


def limit(items: List, limit_count: int | None) -> List:
    if limit_count is None:
        return items
    return items[:limit_count]


def read_text_arg(value: str | None, value_file: str | None) -> str:
    if value is None and value_file is None:
        fail("provide --value or --value-file")
    if value is not None and value_file is not None:
        fail("use only one of --value or --value-file")
    if value_file:
        with open(value_file, "r", encoding="utf-8") as f:
            return f.read()
    return value or ""


def read_xml_fragment(xml: str | None, xml_file: str | None) -> List[etree._Element]:
    if xml is None and xml_file is None:
        fail("provide --xml or --xml-file")
    if xml is not None and xml_file is not None:
        fail("use only one of --xml or --xml-file")
    if xml_file:
        with open(xml_file, "r", encoding="utf-8") as f:
            xml = f.read()
    assert xml is not None
    wrapper = f"<_wrap>{xml}</_wrap>"
    try:
        root = etree.fromstring(wrapper.encode("utf-8"))
    except etree.XMLSyntaxError as exc:
        fail(f"XML fragment parse failed: {exc}")
    return list(root)


def ws_only(text: str | None) -> bool:
    return text is not None and text.strip() == ""


def infer_indent_from(text: str | None) -> str | None:
    if text is None or text == "":
        return None
    if not ws_only(text):
        return None
    if "\n" not in text:
        return None
    return text


def sibling_indent(target: etree._Element) -> str:
    if infer_indent_from(target.tail):
        return target.tail or "\n"
    parent = target.getparent()
    if parent is not None and infer_indent_from(parent.text):
        return parent.text or "\n"
    return "\n"


def child_indent(parent: etree._Element) -> str:
    if infer_indent_from(parent.text):
        return parent.text or "\n"
    if len(parent):
        last = parent[-1]
        if infer_indent_from(last.tail):
            return last.tail or "\n"
    return "\n"


def set_tails(nodes: List[etree._Element], tail: str | None) -> None:
    if tail is None:
        return
    for n in nodes:
        n.tail = tail


def apply_insert(
    elements: List[etree._Element],
    nodes: List[etree._Element],
    position: str,
    indent_override: str | None,
) -> int:
    changed = 0
    for el in elements:
        parent = el.getparent()
        if position in {"before", "after"}:
            if parent is None:
                fail("cannot insert before/after root element")
            idx = parent.index(el)
            if position == "after":
                idx += 1
            clones = [copy.deepcopy(n) for n in nodes]
            tail = indent_override or sibling_indent(el)
            set_tails(clones, tail)
            for n in clones:
                parent.insert(idx, n)
                idx += 1
            changed += len(clones)
        elif position in {"inside-first", "inside-last"}:
            clones = [copy.deepcopy(n) for n in nodes]
            tail = indent_override or child_indent(el)
            set_tails(clones, tail)
            if position == "inside-first":
                idx = 0
                for n in clones:
                    el.insert(idx, n)
                    idx += 1
            else:
                for n in clones:
                    el.append(n)
            changed += len(clones)
        else:
            fail(f"unknown insert position: {position}")
    return changed


def apply_replace(
    elements: List[etree._Element],
    nodes: List[etree._Element],
    indent_override: str | None,
) -> int:
    changed = 0
    for el in elements:
        parent = el.getparent()
        if parent is None:
            fail("cannot replace root element")
        idx = parent.index(el)
        clones = [copy.deepcopy(n) for n in nodes]
        tail = indent_override or sibling_indent(el)
        set_tails(clones, tail)
        for n in clones:
            parent.insert(idx, n)
            idx += 1
        parent.remove(el)
        changed += 1
    return changed


def apply_delete(elements: List[etree._Element]) -> int:
    changed = 0
    for el in elements:
        parent = el.getparent()
        if parent is None:
            fail("cannot delete root element")
        parent.remove(el)
        changed += 1
    return changed


def apply_set_text(elements: List[etree._Element], value: str) -> int:
    changed = 0
    for el in elements:
        if el.text != value:
            el.text = value
            changed += 1
    return changed


def apply_set_attr(elements: List[etree._Element], name: str, value: str) -> int:
    changed = 0
    for el in elements:
        if el.get(name) != value:
            el.set(name, value)
            changed += 1
    return changed


def apply_del_attr(elements: List[etree._Element], name: str) -> int:
    changed = 0
    for el in elements:
        if name in el.attrib:
            del el.attrib[name]
            changed += 1
    return changed


def summarize(path: str, matches: int, changed: int, wrote: bool) -> None:
    if changed == 0:
        print(f"{path}: {matches} match(es), no changes")
    else:
        action = "written" if wrote else "dry-run"
        print(f"{path}: {matches} match(es), {changed} change(s) ({action})")


def show_diff(path: str, original: bytes, updated: bytes) -> None:
    try:
        orig_text = original.decode("utf-8")
        new_text = updated.decode("utf-8")
    except UnicodeDecodeError:
        print(f"{path}: binary diff (non-utf8)")
        return
    diff = difflib.unified_diff(
        orig_text.splitlines(),
        new_text.splitlines(),
        fromfile=f"{path}:before",
        tofile=f"{path}:after",
        lineterm="",
    )
    print("\n".join(diff))


def element_outer_xml(el: etree._Element, pretty: bool) -> str:
    return etree.tostring(
        el,
        encoding="unicode",
        pretty_print=pretty,
        with_tail=False,
    )


def element_inner_xml(el: etree._Element, pretty: bool) -> str:
    parts: List[str] = []
    if el.text:
        parts.append(el.text)
    for child in el:
        parts.append(
            etree.tostring(
                child,
                encoding="unicode",
                pretty_print=pretty,
                with_tail=True,
            )
        )
    return "".join(parts)


def child_tag_counts(el: etree._Element) -> List[Tuple[str, int]]:
    counts: dict[str, int] = {}
    for child in el:
        tag = str(child.tag)
        counts[tag] = counts.get(tag, 0) + 1
    return sorted(counts.items())


def truncate(text: str, max_chars: int | None) -> str:
    if max_chars is None or len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}..."


def decode_lines(data: bytes, enc: str | None) -> List[str]:
    encoding = enc or "utf-8"
    try:
        text = data.decode(encoding)
    except UnicodeDecodeError:
        text = data.decode(encoding, errors="replace")
    return text.splitlines()


def format_attrs(el: etree._Element, attr_names: List[str]) -> str:
    if not attr_names:
        return ""
    parts = []
    for name in attr_names:
        if name in el.attrib:
            parts.append(f"{name}={el.attrib[name]!r}")
    if not parts:
        return ""
    return " " + " ".join(parts)


def outline_lines(
    el: etree._Element,
    max_depth: int,
    attr_names: List[str],
    max_children: int | None,
    max_nodes: int | None,
    include_root: bool = True,
) -> List[str]:
    lines: List[str] = []
    count = 0

    def emit(node: etree._Element, depth: int) -> bool:
        nonlocal count
        if max_nodes is not None and count >= max_nodes:
            return False
        indent = "  " * depth
        attr_str = format_attrs(node, attr_names)
        lines.append(f"{indent}<{node.tag}>{attr_str}")
        count += 1
        if depth >= max_depth:
            return True
        children = list(node)
        if max_children is not None and len(children) > max_children:
            visible = children[:max_children]
            extra = len(children) - max_children
        else:
            visible = children
            extra = 0
        for child in visible:
            if not emit(child, depth + 1):
                return False
        if extra:
            lines.append(f"{indent}  ... (+{extra} more)")
        return True

    if include_root:
        emit(el, 0)
    else:
        for child in list(el):
            if not emit(child, 0):
                break

    return lines


def decode_text(data: bytes, enc: str | None) -> str:
    encoding = enc or "utf-8"
    try:
        return data.decode(encoding)
    except UnicodeDecodeError:
        return data.decode(encoding, errors="replace")


def encode_text(text: str, enc: str | None) -> bytes:
    encoding = enc or "utf-8"
    return text.encode(encoding)


def line_starts(text: str) -> List[int]:
    starts = [0]
    for idx, ch in enumerate(text):
        if ch == "\n":
            starts.append(idx + 1)
    return starts


def local_tag(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def find_start_tag_span(text: str, line_start: int, tag: str) -> tuple[int, int] | None:
    needle = f"<{tag}"
    start = text.find(needle, line_start)
    if start == -1:
        start = text.find("<", line_start)
    if start == -1:
        return None
    in_quote = None
    i = start
    while i < len(text):
        ch = text[i]
        if ch in "\"'":
            if in_quote is None:
                in_quote = ch
            elif in_quote == ch:
                in_quote = None
        elif ch == ">" and in_quote is None:
            return start, i
        i += 1
    return None


def escape_attr(value: str, quote: str) -> str:
    if quote == "\"":
        return xml_escape(value, {"\"": "&quot;"})
    return xml_escape(value, {"'": "&apos;"})


def set_attr_in_tag(tag_text: str, name: str, value: str) -> tuple[str, bool]:
    pattern = re.compile(rf'(\s+{re.escape(name)}\s*=\s*)(["\'])(.*?)\2')
    match = pattern.search(tag_text)
    if match:
        quote = match.group(2)
        escaped = escape_attr(value, quote)
        replacement = f"{match.group(1)}{quote}{escaped}{quote}"
        return pattern.sub(replacement, tag_text, count=1), True
    insert = f" {name}=\"{escape_attr(value, chr(34))}\""
    if tag_text.rstrip().endswith("/>"):
        idx = tag_text.rfind("/>")
        return tag_text[:idx] + insert + tag_text[idx:], True
    if tag_text.rstrip().endswith(">"):
        idx = tag_text.rfind(">")
        return tag_text[:idx] + insert + tag_text[idx:], True
    return tag_text, False


def del_attr_in_tag(tag_text: str, name: str) -> tuple[str, bool]:
    pattern = re.compile(rf'\s+{re.escape(name)}\s*=\s*(["\'])(.*?)\1')
    match = pattern.search(tag_text)
    if not match:
        return tag_text, False
    return pattern.sub("", tag_text, count=1), True


def apply_attr_surgical(
    text: str,
    elements: List[etree._Element],
    name: str,
    value: str | None,
    set_value: bool,
) -> tuple[str, int]:
    starts = line_starts(text)
    edits: List[tuple[int, int, str]] = []
    seen = set()

    for el in elements:
        line = el.sourceline or 0
        if line <= 0 or line > len(starts):
            continue
        tag = local_tag(str(el.tag))
        span = find_start_tag_span(text, starts[line - 1], tag)
        if not span:
            continue
        start, end = span
        if start in seen:
            continue
        seen.add(start)
        tag_text = text[start : end + 1]
        if set_value:
            new_tag, changed = set_attr_in_tag(tag_text, name, value or "")
        else:
            new_tag, changed = del_attr_in_tag(tag_text, name)
        if changed and new_tag != tag_text:
            edits.append((start, end, new_tag))

    for start, end, new_tag in sorted(edits, key=lambda x: x[0], reverse=True):
        text = text[:start] + new_tag + text[end + 1 :]

    return text, len(edits)


def apply_text_surgical(
    text: str, elements: List[etree._Element], value: str
) -> tuple[str, int]:
    starts = line_starts(text)
    edits: List[tuple[int, int, str]] = []
    seen = set()

    for el in elements:
        if len(el):
            fail("set-text only supports elements without child elements in surgical mode")
        line = el.sourceline or 0
        if line <= 0 or line > len(starts):
            continue
        tag = local_tag(str(el.tag))
        span = find_start_tag_span(text, starts[line - 1], tag)
        if not span:
            continue
        start, end = span
        if start in seen:
            continue
        seen.add(start)
        tag_text = text[start : end + 1]
        if re.search(r"/\s*>\s*$", tag_text):
            replacement = re.sub(
                r"/\s*>\s*$",
                f">{xml_escape(value)}</{tag}>",
                tag_text,
            )
            edits.append((start, end, replacement))
            continue
        end_tag = f"</{tag}>"
        end_tag_idx = text.find(end_tag, end + 1)
        if end_tag_idx == -1:
            continue
        edits.append((end + 1, end_tag_idx, xml_escape(value)))

    for start, end, new_text in sorted(edits, key=lambda x: x[0], reverse=True):
        text = text[:start] + new_text + text[end:]

    return text, len(edits)
