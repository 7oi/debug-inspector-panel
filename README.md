Inspector Panel
===============

> So long as I can put `print` statements in the code, and can read it thoroughly, I can usually find the bugs.

*Joshua Bloch*, about his techniques for debugging programs (extracted from [Coders at work](http://goo.gl/WI0RU))

Inspector panel is intended to retrieve information about variables when developing Django applications.

The panel must be used with [django-debug-toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar).

### Motivation

Have you found yourself doing this all the time?:

    def my_view(request):
        my_var = some_third_party_function()
        print my_var
        print type(my_var)
        #...

Well, I used to do that a lot. So, I decided to write this simple panel.

The idea is to use just one function `dj_debug` and get lots of information. Here's an example of a [real Django App](https://github.com/santiagobasulto/guide-to-testing-in-django):

    def index(request):
        latest_poll_list = Poll.published.all().order_by('-pub_date')[:5]
        dj_debug(latest_poll_list)  # Just add this line
        return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})

You get first some information in the Debug Toolbar:

![Debug Toolbar panel](http://i.imgur.com/Wv9rV.png)

And you can optionally get the same info in the console:

![Console debug](http://i.imgur.com/z4Ybe.png)

### Installation

    $ pip install git+git://github.com/santiagobasulto/debug-inspector-panel

Add the panel to the `DEBUG_TOOLBAR_PANELS` settings variable: 

    DEBUG_TOOLBAR_PANELS = (
        ...
        'inspector_panel.panels.inspector.InspectorPanel',
        ...
    )

Add `inspector_panel` to your `INSTALLED_APPS`

    INSTALLED_APPS = (
        # ... More Apps ... #
        'debug_toolbar',
        'inspector_panel'
    )

Add this setting variable:
    
    DEBUG_INSPECTOR_PANEL_EXTEND_BUILTINS = True

If `DEBUG_INSPECTOR_PANEL_EXTEND_BUILTINS` is set to True, debug inspector panel will add a builtin function called `dj_debug` that you can use without importing anything.
If you set this to False, you have to import the `debug` function whenever you want to use it as follows:

    from inspector_panel import debug


### Use
#### By Importing It
Just import the debug function:

    from inspector_panel import debug

and use it to debug whatever you want:

    debug([1, 2, 3])
    debug(Poll)
    debug(Poll.objects.all())

    def my_function():
        print "Hello World"

    debug(my_function)

Optionally you can disable console logging:

    debug([1, 2, 3], console=False)

#### Without Importing
After you set `DEBUG_INSPECTOR_PANEL_EXTEND_BUILTINS` to `True`, you no longer need to import a function
to use `dj_debug`. You can simply use it whenver you want:

    dj_debug([1, 2, 3])
    dj_debug(Poll)
    dj_debug(Poll.objects.all())

    def my_function():
        print "Hello World"

    dj_debug(my_function)


### Important!

This panel is NOT a replacement for other more complete tools as [python logging](http://docs.python.org/library/logging.html) and [pdb](http://docs.python.org/library/pdb).

### License

See LICENSE on project root.
