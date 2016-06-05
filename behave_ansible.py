

from __future__ import unicode_literals

from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.utils.vars import load_extra_vars
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.playbook import Playbook
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor


class AnsibleHelper(object):

    Options = namedtuple('Options',
                         ['connection', 'module_path', 'forks', 'become_user',
                          'become', 'become_method', 'check', 'extra_vars',
                          'listhosts', 'listtasks', 'listtags', 'syntax',
                         ])

    def __init__(self, inventory_file):
        self.variable_manager = vm = VariableManager()
        self.loader = DataLoader()
        self.inventory = Inventory(loader=self.loader,
                                   variable_manager=vm,
                                   host_list=inventory_file)
        vm.set_inventory(self.inventory)
        self.options_args = dict(connection='smart',
                                 module_path=None,
                                 forks=100,
                                 become=None,
                                 become_method=None,
                                 become_user=None,
                                 check=False,
                                 listhosts=False,
                                 listtasks=False,
                                 listtags=False,
                                 syntax=False,
                                 extra_vars={})
        self._run_vars = None

    def run_playbook(self, playbook):
        options = self.Options(**self.options_args)
        vm = self.variable_manager
        vm.extra_vars = load_extra_vars(loader=self.loader, options=options)
        pbe = PlaybookExecutor(
            playbooks=[playbook],
            inventory=self.inventory,
            variable_manager=vm,
            loader=self.loader,
            options=options,
            passwords=dict(conn_pass='playground'),
        )
        res = pbe.run()
        self._run_vars = vm.get_vars(self.loader)
        return res

    def get_vars(self, *args, **kwargs):
        self.inventory.get_vars(*args, **kwargs)

    def get_hosts(self, *args, **kwargs):
        self.inventory.ger_hosts(*args, **kwargs)

    def get_groups(self, *args, **kwargs):
        self.inventory.get_groups(*args, **kwargs)

    @property
    def run_vars(self):
        return self._run_vars
