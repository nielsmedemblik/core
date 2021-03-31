"""Host API required for Work Files."""

from pathlib import Path
from typing import Dict, List, Optional, Text

import bpy


def open_file(filepath: Text) -> Optional[Text]:
    """Open the scene file in Blender."""

    preferences = bpy.context.preferences
    load_ui = preferences.filepaths.use_load_ui
    use_scripts = preferences.filepaths.use_scripts_auto_execute
    result = bpy.ops.wm.open_mainfile(
        filepath=filepath,
        load_ui=load_ui,
        use_scripts=use_scripts,
    )

    if result == {"FINISHED"}:
        return filepath
    return None


def save_file(filepath: Text, copy: bool = False) -> Optional[Text]:
    """Save the open scene file."""

    preferences = bpy.context.preferences
    compress = preferences.filepaths.use_file_compression
    relative_remap = preferences.filepaths.use_relative_paths
    result = bpy.ops.wm.save_as_mainfile(
        filepath=filepath,
        compress=compress,
        relative_remap=relative_remap,
        copy=copy,
    )

    if result == {"FINISHED"}:
        return filepath
    return None


def current_file() -> Optional[Text]:
    """Return the path of the open scene file."""

    current_filepath = bpy.data.filepath
    if Path(current_filepath).is_file():
        return current_filepath
    return None


def has_unsaved_changes() -> bool:
    """Does the open scene file have unsaved changes?"""

    return bpy.data.is_dirty


def file_extensions() -> List[Text]:
    """Return the supported file extensions for Blender scene files."""

    return [".blend"]


def work_root(session: Dict) -> Text:
    """Return the default root to browse for work files."""

    work_dir = session["AVALON_WORKDIR"]
    scene_dir = session.get("AVALON_SCENEDIR")
    if scene_dir:
        return str(Path(work_dir, scene_dir))
    return work_dir
