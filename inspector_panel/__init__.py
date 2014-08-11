from django.conf import settings

__all__ = ["panels"]
from inspector_panel.panels.inspector import debug

DEBUG_INSPECTOR_PANEL_EXTEND_BUILTINS = getattr(settings, 'DEBUG_INSPECTOR_PANEL_EXTEND_BUILTINS', False)

if DEBUG_INSPECTOR_PANEL_EXTEND_BUILTINS:
    # ensure we're not overriding an existing builtin
    try:
        __builtins__['dj_debug']

        raise NameError('dj_debug is already in use as a builtin. Set DEBUG_INSPECTOR_PANEL_EXTEND_BUILTINS setting to False.')
    except KeyError as e:
        __builtins__['dj_debug'] = debug
