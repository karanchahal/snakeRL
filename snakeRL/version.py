version_info = (0, 0, 1)
# format:
# ('snakeRL:_major', 'snakeRL_minor', 'snakeRL_patch')

def get_version():
    "Returns the version as a human-format string."
    return '%d.%d.%d' % version_info

__version__ = get_version()