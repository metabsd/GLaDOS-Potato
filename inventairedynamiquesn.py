#!/usr/bin/env python

# (l) 2016, Benoit Martin-Poitras <b.martinpoitras@saq.qc.ca>
#
# Utiliser le style PEP8 https://www.python.org/dev/peps/pep-0008/
# Lutilisation des espaces est prefere, ne pas faire de tab. Si vous utilisez des tab vous pouvez configurer votre editeur text pour simuler 4 espaces.
# Ce programme a pour but de creer une liste de host dynamique pour Ansible. La source est ServiceNOW et le format et JSON.

DOCUMENTATION = '''
Exemples
--------
# Collecter les host de ServiceNOW et les afficher en format JSON
./inventairedynamiquesn.py --pretty
# Utilisation en tant que playbook
ansible-playbook -i ~/projects/ansible/contrib/inventory/inventairedynamiquesn.py inventaire_servicenow.yml
# Playbook avec les options suivantes:
    - name: Inventaire ServiceNOW Test
      hosts: all
      connection: local
      gather_facts: no
      tasks:
        - debug: msg="Hosts - {{ inventory_hostname }}"
'''

import requests
import os
import argparse
import keyring
import json
import yaml
from collections import defaultdict

BOOLEANS_TRUE = ['yes', 'on', '1', 'true', 1, True]
BOOLEANS_FALSE = ['no', 'off', '0', 'false', 0, False]

SN_ENV_ARGS = dict(
    config_file='SN_CONFIG_FILE',
    url='SN_URL',
    user='SN_USER',
)

def fail(msg):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)

def log(msg, pretty_print=False):
    if pretty_print:
        print(json.dumps(msg, sort_keys=True, indent=2))
    else:
        print(msg + u'\n')

class EnvArgs(object):
    def __init__(self):
        self.config_file = None
        self.url = None
        self.user = None

class ServiceNowInventory():
    ''' Classe definissant le programme par :
        - ses parametres
        - la liste venant de ServiceNOW
        - la transformation pour generer linventaire dynamique pour Ansible'''

    def _parse_config_file(self):
        config = dict()
        config_path = None

        if self._args.config_file:
            config_path = self._args.config_file
        elif self._env_args.config_file:
            config_path = self._env_args.config_file

        if config_path:
            try:
                config_file = os.path.abspath(config_path)
            except:
                config_file = None

            if config_file and os.path.exists(config_file):
                with open(config_file) as f:
                    try:
                        config = yaml.safe_load(f.read())
                    except Exception as exc:
                        self.fail("Error: parsing %s - %s" % (config_path, str(exc)))
        return config

    def _parse_cli_args(self):
        '''Definition des parametres disponible pour le programme'''
        basename = os.path.splitext(os.path.basename(__file__))[0]
        default_config = basename + '.yml'
        parser = argparse.ArgumentParser(description='Return Ansible inventory for one or more hosts')
        parser.add_argument('--list', action='store_true', default=True,
                            help='List all hosts (default: True)')
        parser.add_argument('--host', action='store',
                            help='Only get information for a specific host.')
        parser.add_argument('--pretty', action='store_true', default=False,
                            help='Pretty print JSON output(default: False)')
        parser.add_argument('--config-file', action='store', default=default_config,
                            help="Name of the config file to use. Default is %s" % (default_config))
        return parser.parse_args()
    '''
    def _json_format_dict(self, data, pretty_print=False):
    # format inventory data for output
    if pretty_print:
        return json.dumps(data, sort_keys=True, indent=4)
    else:
        return json.dumps(data)
    '''
    def _parse_env_args(self):
        args = EnvArgs()
        for key, value in SN_ENV_ARGS.items():
            if os.environ.get(value):
                val = os.environ.get(value)
                if val in BOOLEANS_TRUE:
                    val = True
                if val in BOOLEANS_FALSE:
                    val = False
                setattr(args, key, val)
        return args

    def get_hosts(self, config):

        '''Variable du fichier yml'''
        defaults = config.get('defaults', dict())
        pwd = keyring.get_password("system", defaults.get('user') )
        #print defaults.get('url')
        #print defaults.get('user')
        #print pwd
        #print self.headers
        '''Faire une requete https'''
        response = requests.get(defaults.get('url'), auth=(defaults.get('user'), pwd), headers=self.headers)
        '''sassurer que le retour est 200'''
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()

        '''Decoder le resultat JSON dans un dictionaire et test le resultat.'''
        json_hosts = response.json()

        '''Afficher le json'''
        #print(json.dumps(jsonhosts, indent=4))
        print type(json_hosts)
        print (json_hosts.keys())
        for host in json_hosts["result"]:
            print host["name"]

    '''Contructeur'''
    def __init__(self):

        self.defaultgroup = 'group_all'
        self._args = self._parse_cli_args()
        self._env_args = self._parse_env_args()
        self.groups = defaultdict(list)
        self.hostvars = defaultdict(dict)
        self.response = None
        '''Utiliser le bon headers'''
        self.headers = {"Content-Type":"application/json","Accept":"application/json"}
        self.result = {}
        self.result['all'] = {}
        self.result['all']['hosts'] = []
        self.result['_meta'] = {}
        self.result['_meta']['hostvars'] = {}

    '''
        if self.response:
            self.get_host()
            if self.options.hosts:
                print(json.dumps({}))
            elif self.options.list:
                print(json.dumps(self.result))
            else:
                print("usage: --list or --host HOSTNAME")
                exit(1)
        else:
            print("Error: ServiceNOW connection is wrong.")
            exit(1)
    '''

    def run(self):
        config_from_file = self._parse_config_file()
        if not config_from_file:
            config_from_file = dict()
        """Work in Progress"""
        self.get_hosts(config_from_file)

        exit(0)

ServiceNowInventory().run()
