import os
import sys

import unittest
import functools
from contextlib import contextmanager
from StringIO import StringIO

from behave_ansible import AnsibleHelper


def capture_output(func):

    @contextmanager
    def save_restore_std():
	new_out, new_err = StringIO(), StringIO()
	old_out, old_err = sys.stdout, sys.stderr
	try:
	    sys.stdout, sys.stderr = new_out, new_err
	    yield sys.stdout, sys.stderr
	finally:
	    sys.stdout, sys.stderr = old_out, old_err

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
	with save_restore_std() as (out, err):
	     return func(*args, **kwargs)

    return wrapper

class TestBase(unittest.TestCase):

    @capture_output
    def test_failed_playbook(self):
        inv_file = os.path.join(os.path.dirname(__file__), 'inv_test.cfg')
        pb_file = os.path.join(os.path.dirname(__file__), 'failed_pb.yml')
        ah = AnsibleHelper(inv_file)
        self.assertEqual(ah.run_playbook(pb_file), 2)


    @capture_output
    def test_success_playbook(self):
        inv_file = os.path.join(os.path.dirname(__file__), 'inv_test.cfg')
        pb_file = os.path.join(os.path.dirname(__file__), 'success_pb.yml')
        ah = AnsibleHelper(inv_file)
        self.assertEqual(ah.run_playbook(pb_file), 0)



if __name__ == '__main__':
    unittest.main()
