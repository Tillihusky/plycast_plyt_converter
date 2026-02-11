#!/usr/bin/env python3
import os
import sys
import uuid
import argparse
import xml.etree.ElementTree as ET


def dash_guid(s: str) -> str:
    """Force 8-4-4-4-rest dash pattern."""
    s = (s or "").strip()
    a = s[:8]
    b = s[8:12]
    c = s[12:16]
    d = s[16:20]
    e = s[20:]
    return f"{a}-{b}-{c}-{d}-{e}"


def basename_any(path: str) -> str:
    path = (path or "").strip()
    return os.path.basename(path.replace("\\", os.sep).replace("/", os.sep))


def is_comment_item(attrs: dict) -> bool:
    path = (attrs.get("ply_path") or "").strip().lower()
    module = (attrs.get("ply_module") or "").strip().lower()
    return path.endswith("comment.plyevent") or module in ("true", "1", "yes", "on")


def parse_category(ply_cats: str) -> str:
    s = (ply_cats or "").strip()
    if not s:
        return ""
    return s.split(";", 1)[0].strip()


def make_guid(old_id: str, mode: str) -> str:
    if mode == "keep":
        return dash_guid(old_id)
    return str(uuid.uuid4())


def convert_file(in_path: str, out_path: str, guid_mode: str) -> None:
    tree = ET.parse(in_path)
    root = tree.getroot()

    if root.tag != "Template":
        raise ValueError(f"Expected <Template>, got <{root.tag}> in {in_path}")

    playstate = root.attrib.get("playlist_playstate", "False")
    out_root = ET.Element("PlyList", {"PlayState": playstate})

    for it in root.findall("./item"):
        a = it.attrib

        ply_id = a.get("ply_id", "")
        ply_title = a.get("ply_title", "")
        ply_path = a.get("ply_path", "")
        ply_in = a.get("ply_in", "00:00:00.000")
        ply_out = a.get("ply_out", "00:00:00.000")
        ply_duration = a.get("ply_duration", "00:00:00.000")
        ply_start = a.get("ply_start", "2000-01-01 00:00:00.000")
        ply_end = a.get("ply_end", "2000-01-01 00:00:00.000")
        ply_state = (a.get("ply_state", "follow") or "follow").strip().upper()
        ply_logo = a.get("ply_logo", "") or ""
        ply_cg = a.get("ply_cg", "") or ""
        ply_cats = a.get("ply_cats", "") or ""
        ply_plugin = a.get("ply_pluginoption", "") or ""

        comment = is_comment_item(a)

        if comment:
            clip_path = "[COMMENT]"
            clip_name = ply_title.strip()
            tc_in = "00:00:00.000"
            tc_out = "00:00:00.000"
            tc_dur = "00:00:00.000"
            start_time = ply_start
            end_time = ply_end
            category = ""
            clip_logo = ""
            clip_cg = ""
            plugin_data = ""
        else:
            clip_path = ply_path
            clip_name = basename_any(ply_path)
            tc_in = ply_in
            tc_out = ply_out
            tc_dur = ply_duration
            start_time = ply_start
            end_time = ply_end
            category = parse_category(ply_cats)
            clip_logo = "" if ply_logo.strip() == "," else ply_logo
            clip_cg = ply_cg
            plugin_data = ply_plugin

        attrs = {
            "GUID": make_guid(ply_id, guid_mode),
            "TC_IN": tc_in,
            "TC_OUT": tc_out,
            "ORIGINAL_TC_OUT": tc_out,
            "TC_DURATION": tc_dur,
            "StartTime": start_time,
            "EndTime": end_time,
            "ClipPath": clip_path,
            "ClipName": clip_name,
            "ClipState": ply_state,
            "FixState": "False",
            "ClipLogo": clip_logo,
            "ClipCG": clip_cg,
            "Category": category,
            "CategoryGuid": "",
            "PluginData": plugin_data,
        }

        ET.SubElement(out_root, "PlyItem", attrs)

    ET.ElementTree(out_root).write(out_path, encoding="UTF-8", xml_declaration=True)


def main():
    ap = argparse.ArgumentParser(description="Convert old PlyCast .plyt playlists to new format.")
    ap.add_argument("input", help="Input .plyt file or folder")
    ap.add_argument("output", nargs="?", help="Output .plyt file or folder (optional)")
    ap.add_argument("--guid", choices=("random", "keep"), default="random",
                    help="GUID handling: random (default) or keep old ply_id")
    args = ap.parse_args()

    in_path = args.input

    if os.path.isdir(in_path):
        out_dir = args.output or (in_path.rstrip("/\\") + "_new")
        os.makedirs(out_dir, exist_ok=True)

        for name in os.listdir(in_path):
            if not name.lower().endswith(".plyt"):
                continue
            src = os.path.join(in_path, name)
            dst = os.path.join(out_dir, os.path.splitext(name)[0] + "_new.plyt")
            convert_file(src, dst, args.guid)
            print(f"Converted: {src} -> {dst}")
    else:
        out_path = args.output or (os.path.splitext(in_path)[0] + "_new.plyt")
        convert_file(in_path, out_path, args.guid)
        print(f"Converted: {in_path} -> {out_path}")


if __name__ == "__main__":
    main()
