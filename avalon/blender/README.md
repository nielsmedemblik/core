# Avalon Integration for Blender

> TODO: start by showing a (moving gif) of Avalon in action inside of Blender.

## Getting Blender set up for Avalon

To get Avalon running inside of Blender you have to set the environment variable
`BLENDER_USER_SCRIPTS` to `{core}/setup/blender`.

Now when you launch Blender you should see an _Avalon_ menu.
> TODO: add an image showing the menu and possibly some other images showing
> Avalon in action.

## How Avalon _containers_ are implemented

Avalon's containers are implemented as _collections_ (TODO: link to Blender
manual). The needed metadata is added under an `avalon` key, for example:

```python
# TODO: check correct data
collection['avalon'] = {
    "schema": "avalon-core:container-2.0",
    "id": "avalon",
    "name": "modelDefault",
    "namespace": "",
    "loader": str(loader),
    "representation": str(context["representation"]["_id"]),
}
```

## A note about `bpy.context`

When you run code inside of Blender from one of the Avalon (Qt) apps, you only
have access to the [_global
context_](https://docs.blender.org/api/current/bpy.context.html#global-context).
If you have worked with Blender before you might expect to get selected objects
for example with `bpy.context.selected_objects`. But in this case that won't
work, because that is part of the [_screen
context_](https://docs.blender.org/api/current/bpy.context.html#screen-context).

**Keep this in mind when writing Avalon plugins for Blender and _only_ rely on
the _global context_.**

To get the selected objects (as that is quite common and needed by Avalon
itself) there is a simple helper function in `avalon.blender.lib`:

```python
def get_selection() -> List[bpy.types.Object]:
    """Return the selected objects from the current scene."""
    return [obj for obj in bpy.context.scene.objects if obj.select_get()]
```

If you have the need to access more members of the _screen context_ consider
writing you own helper functions in your studio configuration. Or if you think
it should be part of the default integration consider [creating an
issue](https://github.com/getavalon/core/issues/new/choose) or making a [pull
request](https://github.com/getavalon/core/pulls).

## Errors in Qt related code can crash Blender

Exceptions raised by 'Qt code' will crash the QApplication and also take down
Blender in the process. Especially when developing or bug fixing this can be
quite annoying.  If you don't launch Blender from a terminal there is no way to
see the traceback.  If you don't want this you can (temporarily) override
`sys.excepthook` with this for example:

```python
sys.excepthook = lambda *exc_info: traceback.print_exception(*exc_info)
```

A good place for this might either be in a custom startup script for Blender or
you can uncomment the lines in `core/setup/blender/startup/setup_avalon.py`.

**Be careful though!** There can only be one `sys.excepthook`. So if another
vendor or Blender installs it's own excepthook you risk random breakage of
anything that depends on it. Only do this when developing or when bug hunting!
