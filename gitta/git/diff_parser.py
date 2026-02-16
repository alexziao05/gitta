# git/diff_parser.py
# Purpose: Parse and group unified diffs by file and module.
#
# Responsibilities:
#   - Split a raw unified diff into per-file chunks
#   - Group file diffs by top-level directory (module/scope)

import re
from dataclasses import dataclass, field
from pathlib import PurePosixPath


@dataclass
class FileDiff:
    file_path: str
    diff_text: str


@dataclass
class DiffGroup:
    scope: str
    files: list[str] = field(default_factory=list)
    combined_diff: str = ""


# Matches lines like: diff --git a/foo/bar.py b/foo/bar.py
DIFF_HEADER_RE = re.compile(r"^diff --git a/.+ b/(.+)$", re.MULTILINE)


def parse_diff_by_file(raw_diff: str) -> list[FileDiff]:
    """Split a unified diff string into per-file chunks.

    Each chunk includes the diff header and all hunks for that file.
    The file path is extracted from the 'b/' side of the header.
    """
    matches = list(DIFF_HEADER_RE.finditer(raw_diff))

    if not matches:
        return []

    file_diffs = []
    for i, match in enumerate(matches):
        file_path = match.group(1)
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw_diff)
        diff_text = raw_diff[start:end].rstrip("\n")
        file_diffs.append(FileDiff(file_path=file_path, diff_text=diff_text))

    return file_diffs


def _find_scope_depth(file_diffs: list[FileDiff]) -> int:
    """Find the best path depth for grouping.

    If all files share a common top-level directory, use the next level
    down for more meaningful grouping. Returns the 0-based index of the
    path component to use as scope.
    """
    if not file_diffs:
        return 0

    # Get top-level dirs for files that have subdirectories
    top_dirs = set()
    for fd in file_diffs:
        parts = PurePosixPath(fd.file_path).parts
        if len(parts) > 1:
            top_dirs.add(parts[0])

    # If all nested files share one top-level dir, go one level deeper
    if len(top_dirs) == 1:
        return 1

    return 0


def group_diffs_by_module(file_diffs: list[FileDiff]) -> list[DiffGroup]:
    """Group FileDiff objects by directory module.

    Automatically detects the best grouping depth. If all files share a
    common top-level directory (e.g., 'gitta/'), groups by the next level
    (e.g., 'cli', 'ai', 'core'). Files at root level get scope 'root'.
    Groups are returned sorted by scope name.
    """
    depth = _find_scope_depth(file_diffs)
    groups: dict[str, DiffGroup] = {}

    for fd in file_diffs:
        parts = PurePosixPath(fd.file_path).parts
        if len(parts) > depth + 1:
            scope = parts[depth]
        elif len(parts) > 1:
            scope = parts[0]
        else:
            scope = "root"

        if scope not in groups:
            groups[scope] = DiffGroup(scope=scope)

        groups[scope].files.append(fd.file_path)

        if groups[scope].combined_diff:
            groups[scope].combined_diff += "\n"
        groups[scope].combined_diff += fd.diff_text

    return sorted(groups.values(), key=lambda g: g.scope)
