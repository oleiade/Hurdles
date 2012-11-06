# -*- coding: utf-8 -*-

# Copyright (c) 2012 theo crevon
#
# See the file LICENSE for copying permission.

#
# Content of this module was extracted from python nose
# project importer.py module.
#
# See : https://github.com/nose-devs/nose/blob/master/nose/importer.py
#

import os
import sys

import imp


class Importer(object):
    """An importer class that does only path-specific imports. That
    is, the given module is not searched for on sys.path, but only at
    the path or in the directory specified.
    """

    def importFromPath(self, path, fqname):
        """Import a dotted-name package whose tail is at path. In other words,
        given foo.bar and path/to/foo/bar.py, import foo from path/to/foo then
        bar from path/to/foo/bar, returning bar.
        """
        # find the base dir of the package
        path_parts = os.path.normpath(os.path.abspath(path)).split(os.sep)
        name_parts = fqname.split('.')
        if path_parts[-1].startswith('__init__'):
            path_parts.pop()
        path_parts = path_parts[:-(len(name_parts))]
        dir_path = os.sep.join(path_parts)
        # then import fqname starting from that dir
        return self.importFromDir(dir_path, fqname)

    def importFromDir(self, dir, fqname):
        """Import a module *only* from path, ignoring sys.path and
        reloading if the version in sys.modules is not the one we want.
        """
        dir = os.path.normpath(os.path.abspath(dir))
        # log.debug("Import %s from %s", fqname, dir)

        # FIXME reimplement local per-dir cache?

        # special case for __main__
        if fqname == '__main__':
            return sys.modules[fqname]

        path = [dir]
        parts = fqname.split('.')
        part_fqname = ''
        mod = parent = fh = None

        for part in parts:
            if part_fqname == '':
                part_fqname = part
            else:
                part_fqname = "%s.%s" % (part_fqname, part)
            try:
                imp.acquire_lock()
                fh, filename, desc = imp.find_module(part, path)
                old = sys.modules.get(part_fqname)
                if old is not None:
                    # test modules frequently have name overlap; make sure
                    # we get a fresh copy of anything we are trying to load
                    # from a new path
                    if (self.sameModule(old, filename)
                        or (getattr(old, '__path__', None))):
                        mod = old
                    else:
                        del sys.modules[part_fqname]
                        mod = imp.load_module(part_fqname, fh, filename, desc)
                else:
                    mod = imp.load_module(part_fqname, fh, filename, desc)
            finally:
                if fh:
                    fh.close()
                imp.release_lock()
            if parent:
                setattr(parent, part, mod)
            if hasattr(mod, '__path__'):
                path = mod.__path__
            parent = mod
        return mod

    def sameModule(self, mod, filename):
        mod_paths = []
        if hasattr(mod, '__path__'):
            for path in mod.__path__:
                mod_paths.append(os.path.dirname(
                    os.path.normpath(
                    os.path.abspath(path))))
        elif hasattr(mod, '__file__'):
            mod_paths.append(os.path.dirname(
                os.path.normpath(
                os.path.abspath(mod.__file__))))
        else:
            # builtin or other module-like object that
            # doesn't have __file__; must be new
            return False
        new_path = os.path.dirname(os.path.normpath(filename))
        for mod_path in mod_paths:
            if mod_path == new_path:
                return True
        return False
