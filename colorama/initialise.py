import atexit
import sys

from .ansitowin32 import AnsiToWin32

orig_stdout = sys.stdout
orig_stderr = sys.stderr

atexit_done = False


def reset_all():
    AnsiToWin32(orig_stdout).reset_all()


def init(autoreset=False, convert=None, strip=None, wrap=True):
    if wrap == False and (autoreset == True or convert == True or strip == True):
        raise ValueError("wrap=False conflicts with any other arg=True")

    sys.stdout = wrap_stream(orig_stdout, convert, strip, autoreset, wrap)
    sys.stderr = wrap_stream(orig_stderr, convert, strip, autoreset, wrap)

    global atexit_done
    if not atexit_done:
        atexit.register(reset_all)
        atexit_done = True


def wrap_stream(stream, convert, strip, autoreset, wrap):
    if wrap:
        wrapper = AnsiToWin32(stream, convert=convert, strip=strip, autoreset=autoreset)
        if wrapper.should_wrap():
            stream = wrapper.stream
    return stream
