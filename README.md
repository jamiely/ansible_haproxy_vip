Role Name
=========

An example Ansible role that installs haproxy and keepalived
to provide high-availability. keepalived monitors for the presence
of an haproxy pid and will cause the VIP to point to a different
host.

This role also has an example of how to test roles that require
multiple hosts. Running molecule test will provision 2 nodes
using vagrant (Virtualbox), provision the nodes using Ansible,
then run tests by interacting with both nodes.

Role Variables
--------------

See `defaults/main.yml` for an explanation of the variables.


Example Playbook
----------------

See the included molecule playbook and test for an example of
how to use the role.

License
-------

BSD

Devs
----

Use `virtualenv` with `requirements.txt` to install the requirements
in an isolated workspace.

```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```