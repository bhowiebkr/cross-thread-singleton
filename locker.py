import os
import sys
from tempfile import gettempdir
import traceback
import psutil


# Used for locking. This could be the name of whatever this scripts/tool is


class Lock(object):
    """A class for locking processes with a temp file

    Args:
        object ([type]): [description]
    """

    def __init__(self, name):
        self.name = name
        self.lock_file = os.path.join(gettempdir(), f".{self.name.replace(' ', '_')}-lock")

    def _lock_file_exists(self):
        if os.path.exists(self.lock_file):
            return True
        return False

    def _get_lock_pid(self):
        if self._lock_file_exists():
            with open(self.lock_file, "r") as f:
                return int(f.readline())
        return None

    def _write_lock(self):
        with open(self.lock_file, "w") as f:
            f.write(str(os.getpid()))

    def is_locked(self):
        """Check if the file is locked

        Returns:
            [bool]: True if locked, False if not
        """
        lock_pid = self._get_lock_pid()

        # If no pid found, file doesn't exists and not locked
        if not lock_pid:
            return False

        # check if the pid has a running python process, if we find one than it's locked
        if "python" in psutil.Process(lock_pid).name():
            return True
        # else no python is running on that pid so it's safe to say it was closed without being cleaned up
        else:
            return False

    def lock(self):
        """Create a lock

        Returns:
            [bool]: True if success, False if failed to lock
        """
        if not self.is_locked():
            self._write_lock()
            return True
        return False

    def unlock(self):
        """Remove the lock
        """
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)


def locker(lock_name):
    """Locking  decorator used to wrap the main entry point of the script.

    Args:
        func ([type]): The function that gets ran
    """

    def wrapper(func):

        lock = Lock(lock_name)

        if lock.is_locked():
            print(f'"{lock_name}" is already locked. ...Exiting.')
            exit()

        try:
            print("Not locked, locking now")
            lock.lock()
            func()
        except:
            traceback.print_exc(limit=1)
        finally:
            lock.unlock()

            def dummy():
                pass

            return dummy

    return wrapper
