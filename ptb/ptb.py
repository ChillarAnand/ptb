import cgitb
import inspect
import linecache
import os
import pydoc
import sys
import traceback

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer


__UNDEF__ = object()                          # sentinel object


def format_color(code):
    """
    Returns colored text.
    :param code: string
    :return: string
    """
    return highlight(code=code, lexer=PythonLexer(), formatter=TerminalFormatter())


def format_objects(objects):
    """
    :param objects: List of tuples with name, location and value.
    :return: List of formatted objects.

    Eg: 
    (foo, local, 21) --> ['foo = 21']
    (bar, None, None) --> [bar undefined]
    """
    visited, objs = {}, []

    for name, where, value in objects:

        if name in visited:
            continue
        visited[name] = 1

        if where and value is not __UNDEF__:
            if where == 'global':
                name = 'global ' + name
            elif where != 'local':
                name = where + name.split('.')[-1]
            objs.append('%s = %s' % (name, pydoc.text.repr(value)))
        else:
            objs.append(name + ' undefined')

    return objs


def format_locals(local_vars):
    """
    Seperate builtins from variables.

    :param local_vars: Dictionary of locals.
    :return: A tuple of dictionaries.
    """
    local_variables = {k: v for (k, v) in local_vars.items()
                       if not k.startswith('__')}
    local_builtins = {k: v for (k, v) in local_vars.items()
                      if k.startswith('__')}

    local_variables = '{:<10} {}\n'.format('Locals:', local_variables)
    local_builtins = '{:<10} {}\n'.format('Builtins:', local_builtins)

    return local_variables, local_builtins


def format_code(lines, lnum, index):
    """

    """
    code = []
    i = lnum - index
    for line in lines:
        num = '%13d ' % i

        if i == lnum:
            num = '---------> {} '.format(i)

        code.append(num+line.rstrip())
        i += 1

    code = '\n'.join(code)

    return code


def frame_parser(frame_record):
    """
    Parse given frame and return formatted values.
    :param frame_record: frame
    :return: tuple (fname, call, code, objects, local_vars)
    """
    frame, fname, lnum, func, lines, index = frame_record
    fname = fname and os.path.abspath(fname) or '?'
    args, varargs, varkw, local_vars = inspect.getargvalues(frame)

    call = ''
    if func != '?':
        call = func + inspect.formatargvalues(
            args, varargs, varkw, local_vars,
            formatvalue=lambda value: '=' + pydoc.text.repr(value))

    highlight = {}

    def reader(lnum=[lnum]):
        highlight[lnum[0]] = 1
        try:
            return linecache.getline(fname, lnum[0])
        finally:
            lnum[0] += 1

    code = format_code(lines, lnum, index)

    objects = cgitb.scanvars(reader, frame, local_vars)

    return (fname, call, code, objects, local_vars)


def ptb(einfo, original, path, context, locals, builtins):
    """
    Return pretty traceback for given exception.
    :param einfo: tuple with exception info.
    :param context: int, number of lines to be displayed.
    :return: string, pretty traceback.
    """
    et, ev, tb = einfo
    frame_records = inspect.getinnerframes(tb, context)

    pretty_tb = 'Pretty Traceback: \n\n'
    for frame_record in frame_records:
        fname, call, code, objects, frame_vars = frame_parser(frame_record)
        
        if path:
            if not path in fname:
                continue
        fname = '{:<10} {}\n'.format('File:', fname)
        call = '{:<10} {}\n'.format('Call:',  call)
        context = '{:<10}\n{}\n'.format('Context:', code)

        objects = format_objects(objects)
        objects = ', '.join(objects)
        objects = '{:<10} {}\n'.format('Objects:', objects)
        local_vars, local_builtins = format_locals(frame_vars)

        pretty_tb = pretty_tb + fname + call + context + objects

        if locals:
            pretty_tb = pretty_tb + local_vars
        if builtins:
            pretty_tb = pretty_tb + local_builtins

        pretty_tb = pretty_tb + '\n'

    if original:
        original_tb = '{} {}\n\n'.format(
            'Original Traceback: \n',
            ''.join(traceback.format_exception(*einfo)))

        pretty_tb = original_tb + pretty_tb

    pretty_tb = '{}{}: {}'.format(pretty_tb, str(et)[8:-2], str(ev))

    return pretty_tb


class Hook(object):
    """
    A hook to replace sys.excepthook that shows pretty traceback.
    """

    def __init__(self, module=None, path=None, context=1, 
                 locals=None, builtins=None, original=None):
        self.context = context
        self.out = sys.stdout
        self.module = module
        self.path = path
        self.original = original
        self.locals = locals
        self.builtins = builtins

    def __call__(self, etype, evalue, etb):
        # if ptb is called as module, we need to skip 4 frames.
        # see main() function.
        # this is a hack. we need a better solution.
        if self.module:
            etb = etb.tb_next.tb_next.tb_next.tb_next

        self.handle((etype, evalue, etb))

    def handle(self, einfo=None):
        einfo = einfo or sys.exc_info()
        tb = ptb(einfo, self.original, self.path, self.context, self.locals, self.builtins)

        if self.out == sys.stdout:
            self.out.write(format_color(tb))
        else:
            self.out.write(tb)


def enable(context=1, **kwargs):
    sys.excepthook = Hook(context=context, **kwargs)


def main():
    """
    To make ptb run from commannd line.
    """
    filename = sys.argv[1]
    enable(context=1, module=True)

    import __main__
    __main__.__dict__.clear()
    __main__.__dict__.update({"__name__": "__main__",
                              "__file__": filename,
                              "__builtins__": __builtins__,
                          })

    exec(compile(open(filename).read(), filename, 'exec'))


if __name__ == '__main__':
    main()
