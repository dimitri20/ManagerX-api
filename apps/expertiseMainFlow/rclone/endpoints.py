from enum import Enum


class RcloneOperations(Enum):
    OPERATIONS_LIST = 'operations/list'  # List the given remote and path in JSON format
    OPERATIONS_MKDIR = 'operations/mkdir'  # Make a destination directory or container
    OPERATIONS_MOVE_FILE = 'operations/movefile'  # Move a file from source remote to destination remote
    OPERATIONS_PUBLIC_LINK = 'operations/publiclink'  # Create or retrieve a public link to the given file or folder.
    OPERATIONS_PURGE = 'operations/purge'  # Remove a directory or container and all of its contents
    OPERATIONS_REMOVE_DIR = 'operations/rmdir'  # Remove an empty directory or container
    OPERATIONS_REMOVE_DIRS = 'operations/rmdirs'  # Remove all the empty directories in the path
