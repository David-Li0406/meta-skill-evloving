"""Platform-specific metadata normalization for Windows and macOS.

This module normalizes Windows UI Automation and macOS Accessibility API outputs
into unified ElementMetadata instances. It maps platform-specific control types
and AX roles to standardized role names.

Control Type Mappings:
----------------------

Windows UI Automation → Normalized Role:

| Windows Control Type | Normalized Role  | Common Examples           |
|---------------------|------------------|---------------------------|
| Button              | button           | Submit, OK, Cancel        |
| Edit                | text_field       | Username, Password input  |
| Text                | static_text      | Labels, non-editable text |
| Window              | window           | Application windows       |
| Image               | image            | Icons, photos             |
| CheckBox            | checkbox         | Agree to terms            |
| RadioButton         | radio_button     | Option selectors          |
| ComboBox            | combo_box        | Dropdowns                 |
| List                | list             | File lists, item lists    |
| ListItem            | list_item        | Individual list entries   |
| MenuItem            | menu_item        | File menu, Edit menu      |
| TabItem             | tab              | Tab controls              |
| Hyperlink           | link             | Web links, help links     |
| Pane                | pane             | Container panels          |
| Document            | document         | Text documents            |
| ProgressBar         | progress_bar     | Loading indicators        |
| Slider              | slider           | Volume controls           |
| ScrollBar           | scrollbar        | Scroll controls           |
| ToolBar             | toolbar          | Application toolbars      |
| StatusBar           | status_bar       | Status displays           |
| Tree                | tree             | Folder trees              |
| TreeItem            | tree_item        | Folder tree nodes         |
| Table               | table            | Data grids                |
| Header              | header           | Column headers            |
| DataItem            | data_item        | Table cells               |

macOS Accessibility API → Normalized Role:

| macOS AX Role       | Normalized Role  | Common Examples           |
|---------------------|------------------|---------------------------|
| AXButton            | button           | Submit, OK, Cancel        |
| AXTextField         | text_field       | Username, Password input  |
| AXStaticText        | static_text      | Labels, non-editable text |
| AXWindow            | window           | Application windows       |
| AXImage             | image            | Icons, photos             |
| AXCheckBox          | checkbox         | Agree to terms            |
| AXRadioButton       | radio_button     | Option selectors          |
| AXPopUpButton       | combo_box        | Dropdowns (popup)         |
| AXComboBox          | combo_box        | Dropdowns (combo)         |
| AXRow               | list_item        | List row entries          |
| AXCell              | list_item        | Table cells               |
| AXMenuItem          | menu_item        | File menu, Edit menu      |
| AXTabGroup          | tab              | Tab controls (group)      |
| AXRadioGroup        | tab              | Tab controls (radio)      |
| AXLink              | link             | Web links, help links     |
| AXGroup             | pane             | Container groups          |
| AXScrollArea        | scrollbar        | Scroll areas              |
| AXProgressIndicator | progress_bar     | Loading indicators        |
| AXSlider            | slider           | Volume controls           |
| AXToolbar           | toolbar          | Application toolbars      |
| AXTable             | table            | Data grids                |
| AXOutline           | tree             | Outline views             |
| AXSplitGroup        | pane             | Split panes               |

Examples:
    Normalize Windows UI Automation output:
        >>> ui_output = {
        ...     "control_type": "Button",
        ...     "name": "Submit",
        ...     "automation_id": "submitBtn",
        ...     "class_name": "Button",
        ...     "bounding_rectangle": {"x": 100, "y": 200, "width": 150, "height": 50}
        ... }
        >>> metadata = normalize_windows_metadata(ui_output)
        >>> print(metadata.role, metadata.platform)
        button windows

    Normalize macOS Accessibility API output:
        >>> ax_output = {
        ...     "AXRole": "AXButton",
        ...     "AXTitle": "Submit",
        ...     "AXIdentifier": "submitBtn",
        ...     "AXPosition": {"x": 100, "y": 200},
        ...     "AXSize": {"width": 150, "height": 50}
        ... }
        >>> metadata = normalize_macos_metadata(ax_output)
        >>> print(metadata.role, metadata.platform)
        button macos

    Calculate confidence score:
        >>> get_confidence_score(query_latency_ms=500, fallback_used=False)
        1.0
        >>> get_confidence_score(query_latency_ms=1500, fallback_used=True)
        0.7
        >>> get_confidence_score(
        ...     query_latency_ms=2000,
        ...     fallback_used=True,
        ...     permission_status="denied"
        ... )
        0.4
"""

from __future__ import annotations

from typing import Optional, Any

from .element_metadata import Rect, ElementMetadata

# Windows UI Automation control type mappings (14+ common types)
WINDOWS_CONTROL_TYPE_MAP: dict[str, str] = {
    # Core UI elements
    "Button": "button",
    "Edit": "text_field",
    "Text": "static_text",
    "Window": "window",
    "Image": "image",
    "CheckBox": "checkbox",
    "RadioButton": "radio_button",
    "ComboBox": "combo_box",
    "List": "list",
    "ListItem": "list_item",
    "MenuItem": "menu_item",
    "TabItem": "tab",
    "Hyperlink": "link",
    "Pane": "pane",
    "Document": "document",
    # Additional UI controls (10+ types)
    "ProgressBar": "progress_bar",
    "Slider": "slider",
    "ScrollBar": "scrollbar",
    "ToolBar": "toolbar",
    "StatusBar": "status_bar",
    "Tree": "tree",
    "TreeItem": "tree_item",
    "Table": "table",
    "Header": "header",
    "DataItem": "data_item",
    "MenuBar": "menu_bar",
    "Menu": "menu",
    "SplitButton": "split_button",
    "Spinner": "spinner",
    "Group": "group",
}

# macOS Accessibility API AX role mappings (12+ common types)
MACOS_AX_ROLE_MAP: dict[str, str] = {
    # Core UI elements
    "AXButton": "button",
    "AXTextField": "text_field",
    "AXStaticText": "static_text",
    "AXWindow": "window",
    "AXImage": "image",
    "AXCheckBox": "checkbox",
    "AXRadioButton": "radio_button",
    "AXPopUpButton": "combo_box",
    "AXComboBox": "combo_box",
    "AXRow": "list_item",
    "AXCell": "list_item",
    "AXMenuItem": "menu_item",
    "AXTabGroup": "tab",
    "AXRadioGroup": "tab",
    "AXLink": "link",
    # Additional UI controls (8+ types)
    "AXGroup": "pane",
    "AXScrollArea": "scrollbar",
    "AXProgressIndicator": "progress_bar",
    "AXSlider": "slider",
    "AXToolbar": "toolbar",
    "AXTable": "table",
    "AXOutline": "tree",
    "AXSplitGroup": "pane",
    "AXList": "list",
    "AXMenuBar": "menu_bar",
    "AXMenu": "menu",
    "AXTextArea": "text_field",
}


def normalize_windows_metadata(ui_automation_output: dict[str, Any]) -> ElementMetadata:
    """Normalize Windows UI Automation output to ElementMetadata.

    Extracts control_type, name, automation_id, class_name, bounding_rectangle
    from Windows UI Automation output and creates ElementMetadata instance.

    Args:
        ui_automation_output: Dict from Windows UI Automation with keys:
            - control_type: Control type string (e.g., "Button", "Edit")
            - name: Accessible name
            - automation_id: Optional automation ID
            - class_name: Optional window class name
            - bounding_rectangle: Dict with x, y, width, height
            - query_latency_ms: Optional query latency (default 0.0)
            - fallback_used: Optional fallback flag (default False)

    Returns:
        ElementMetadata with platform="windows"

    Examples:
        >>> ui_output = {
        ...     "control_type": "Edit",
        ...     "name": "Username",
        ...     "automation_id": "usernameInput",
        ...     "class_name": "TextBox",
        ...     "bounding_rectangle": {"x": 50, "y": 100, "width": 200, "height": 30}
        ... }
        >>> metadata = normalize_windows_metadata(ui_output)
        >>> print(metadata.role, metadata.windows_automation_id)
        text_field usernameInput
    """
    control_type = ui_automation_output.get("control_type", "")
    role = WINDOWS_CONTROL_TYPE_MAP.get(control_type, "unknown")

    # Extract bounding rectangle
    bounds_data = ui_automation_output.get("bounding_rectangle", {})
    bounds = Rect(
        x=bounds_data.get("x", 0),
        y=bounds_data.get("y", 0),
        width=bounds_data.get("width", 1),
        height=bounds_data.get("height", 1),
    )

    # Calculate confidence score
    query_latency_ms = ui_automation_output.get("query_latency_ms", 0.0)
    fallback_used = ui_automation_output.get("fallback_used", False)
    confidence_score = get_confidence_score(
        query_latency_ms=query_latency_ms,
        fallback_used=fallback_used,
        permission_status=None,
    )

    # Generate unique element_id
    automation_id = ui_automation_output.get("automation_id", "")
    element_id = (
        f"windows_{automation_id}"
        if automation_id
        else f"windows_{role}_{id(ui_automation_output)}"
    )

    return ElementMetadata(
        element_id=element_id,
        name=ui_automation_output.get("name", ""),
        role=role,
        bounds=bounds,
        confidence_score=confidence_score,
        platform="windows",
        windows_automation_id=automation_id or None,
        windows_class_name=ui_automation_output.get("class_name") or None,
        macos_ax_identifier=None,
        macos_ax_role=None,
        properties=ui_automation_output.get("properties", {}),
        query_latency_ms=query_latency_ms,
        permission_status=None,
        fallback_used=fallback_used,
    )


def normalize_macos_metadata(ax_api_output: dict[str, Any]) -> ElementMetadata:
    """Normalize macOS Accessibility API output to ElementMetadata.

    Extracts AXRole, AXTitle/AXDescription, AXIdentifier, AXPosition, AXSize
    from macOS Accessibility API output and creates ElementMetadata instance.

    Args:
        ax_api_output: Dict from macOS Accessibility API with keys:
            - AXRole: AX role string (e.g., "AXButton", "AXTextField")
            - AXTitle or AXDescription: Accessible name
            - AXIdentifier: Optional identifier
            - AXPosition: Dict with x, y
            - AXSize: Dict with width, height
            - query_latency_ms: Optional query latency (default 0.0)
            - permission_status: Optional permission status
            - fallback_used: Optional fallback flag (default False)

    Returns:
        ElementMetadata with platform="macos"

    Examples:
        >>> ax_output = {
        ...     "AXRole": "AXCheckBox",
        ...     "AXTitle": "Agree to terms",
        ...     "AXIdentifier": "termsCheckbox",
        ...     "AXPosition": {"x": 100, "y": 300},
        ...     "AXSize": {"width": 20, "height": 20}
        ... }
        >>> metadata = normalize_macos_metadata(ax_output)
        >>> print(metadata.role, metadata.macos_ax_identifier)
        checkbox termsCheckbox
    """
    ax_role = ax_api_output.get("AXRole", "")
    role = MACOS_AX_ROLE_MAP.get(ax_role, "unknown")

    # Extract position and size
    position = ax_api_output.get("AXPosition", {})
    size = ax_api_output.get("AXSize", {})
    bounds = Rect(
        x=position.get("x", 0),
        y=position.get("y", 0),
        width=size.get("width", 1),
        height=size.get("height", 1),
    )

    # Calculate confidence score
    query_latency_ms = ax_api_output.get("query_latency_ms", 0.0)
    fallback_used = ax_api_output.get("fallback_used", False)
    permission_status = ax_api_output.get("permission_status")
    confidence_score = get_confidence_score(
        query_latency_ms=query_latency_ms,
        fallback_used=fallback_used,
        permission_status=permission_status,
    )

    # Use AXTitle or AXDescription for name
    name = ax_api_output.get("AXTitle") or ax_api_output.get("AXDescription", "")

    # Generate unique element_id
    ax_identifier = ax_api_output.get("AXIdentifier", "")
    element_id = (
        f"macos_{ax_identifier}"
        if ax_identifier
        else f"macos_{role}_{id(ax_api_output)}"
    )

    return ElementMetadata(
        element_id=element_id,
        name=name,
        role=role,
        bounds=bounds,
        confidence_score=confidence_score,
        platform="macos",
        windows_automation_id=None,
        windows_class_name=None,
        macos_ax_identifier=ax_identifier or None,
        macos_ax_role=ax_role or None,
        properties=ax_api_output.get("properties", {}),
        query_latency_ms=query_latency_ms,
        permission_status=permission_status,
        fallback_used=fallback_used,
    )


def get_confidence_score(
    query_latency_ms: float = 0,
    fallback_used: bool = False,
    permission_status: Optional[str] = None,
) -> float:
    """Calculate confidence score based on query quality indicators.

    Scoring:
    - Base score: 1.0
    - -0.1 if query_latency_ms > 1000 (slow query, may be timeout)
    - -0.2 if fallback_used (visual analysis fallback was used)
    - -0.3 if permission_status == "denied" (accessibility permission denied)
    - Minimum: 0.0 (clamped)

    Args:
        query_latency_ms: Query latency in milliseconds (default 0)
        fallback_used: Whether visual analysis fallback was used (default False)
        permission_status: macOS accessibility permission status (default None)

    Returns:
        Confidence score in [0.0, 1.0]

    Examples:
        >>> get_confidence_score()
        1.0
        >>> get_confidence_score(query_latency_ms=1500)
        0.9
        >>> get_confidence_score(fallback_used=True)
        0.8
        >>> get_confidence_score(permission_status="denied")
        0.7
        >>> get_confidence_score(
        ...     query_latency_ms=1500,
        ...     fallback_used=True,
        ...     permission_status="denied"
        ... )
        0.4
    """
    score = 1.0

    if query_latency_ms > 1000:
        score -= 0.1

    if fallback_used:
        score -= 0.2

    if permission_status == "denied":
        score -= 0.3

    return max(0.0, score)


def dict_to_element_metadata(legacy_dict: dict[str, Any]) -> ElementMetadata:
    """Convert legacy dict format to ElementMetadata (compatibility shim).

    Supports migration from existing code that returns dicts with keys:
    name, type, bounds, confidence, source.

    Args:
        legacy_dict: Dict with keys: name, type, bounds, confidence, source

    Returns:
        ElementMetadata instance

    Examples:
        >>> legacy = {
        ...     "name": "Submit",
        ...     "type": "button",
        ...     "bounds": {"x": 100, "y": 200, "width": 150, "height": 50},
        ...     "confidence": 0.95,
        ...     "source": "visual"
        ... }
        >>> metadata = dict_to_element_metadata(legacy)
        >>> print(metadata.role, metadata.fallback_used)
        button True
    """
    bounds_data = legacy_dict.get("bounds", {})
    bounds = Rect(
        x=bounds_data.get("x", 0),
        y=bounds_data.get("y", 0),
        width=bounds_data.get("width", 1),
        height=bounds_data.get("height", 1),
    )

    # Determine platform and fallback from source
    source = legacy_dict.get("source", "unknown")
    fallback_used = source == "visual"

    # Default to "unknown" platform for legacy data
    platform = legacy_dict.get("platform", "windows")  # Assume Windows if not specified
    if platform not in ("windows", "macos"):
        platform = "windows"

    return ElementMetadata(
        element_id=f"legacy_{id(legacy_dict)}",
        name=legacy_dict.get("name", ""),
        role=legacy_dict.get("type", "unknown"),
        bounds=bounds,
        confidence_score=legacy_dict.get("confidence", 0.5),
        platform=platform,  # type: ignore
        properties={},
        fallback_used=fallback_used,
    )
