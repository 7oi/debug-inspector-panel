from django.conf import settings
from django.template.loader import render_to_string
from debug_toolbar.panels import Panel
from debug_toolbar.utils import ThreadCollector
from console_utils import console_debug
import inspect
try:
    import threading
except ImportError:
    threading = None

class DebugCollector(ThreadCollector):
    def collect(self, item, thread=None):
        super(DebugCollector, self).collect(item, thread)

collector = DebugCollector()

class DebugRecord(object):
    def __init__(self, *args, **kwargs):
        pass 

def log_record(record):
    collector.collect(record)


def debug_class(the_class, record):
    """ Adds class and module information
    """
    record.class_name = the_class.__name__
    record.docs = the_class.__doc__
    module = inspect.getmodule(the_class)
    debug_module(module, record)


def debug_module(module, record):
    import __builtin__
    record.source_file = "__builtin__"
    if module != __builtin__:
        record.source_file = inspect.getsourcefile(module)
    record.module_name = module.__name__


def debug_default(value, record):
    __class = value.__class__
    debug_class(__class, record)


def debug(value, console=True):
    if not hasattr(settings, 'DEBUG') or settings.DEBUG is False:
        return
    stack = inspect.stack()[1]
    frm = stack[0]
    print frm.f_locals
    record = DebugRecord()
    record.globals = frm.f_globals
    record.locals = frm.f_locals
    record.value = str(value)
    record.invoked = {}
    record.invoked['file'] = stack[1]
    record.invoked['line'] = stack[2]
    record.invoked['function'] = stack[3]

    if inspect.isclass(value):
        debug_class(value, record)
    elif inspect.ismodule(value):
        debug_module(value, record)
    else:
        debug_default(value, record)

    record.dir = dir(record)
    log_record(record)
    if console:
        console_debug(record)


class InspectorPanel(Panel):

    name = 'InspectorPanel'
    template = 'inspector.html'
    has_content = True

    def __init__(self, *args, **kwargs):
        super(InspectorPanel, self).__init__(*args, **kwargs)
        self._records = {}

    @property
    def nav_title(self):
        return 'Inspector Panel'

    def nav_subtitle(self):
        records = self._records[threading.currentThread()]
        return "%s values to debug" % len(records)

    def title(self):
        return 'All values to debug'

    def url(self):
        return ''

    def process_request(self, request):
        collector.clear_collection()


    def process_response(self, request, response):
        records = collector.get_collection()
        self._records[threading.currentThread()] = records
        collector.clear_collection()
        self.record_stats({'records': records, 'count':len(records)})
