import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_haproxy_installed(host):
    cmd = host.run("/usr/sbin/haproxy -v")
    assert cmd.rc == 0

def test_services_running_and_enabled(host):
    service = host.service('haproxy')
    assert service.is_running
    assert service.is_enabled

def test_redirection(host):
    cmd = host.run("curl -vs http://localhost")
    assert "HTTP/1.1 200" in cmd.stderr

def test_only_host1(host):
    ansible_facts = host.ansible.get_variables()
    if ansible_facts['inventory_hostname'] != 'host1':
        return

def test_vip_active_after_one_node_goes_down(host):
    ansible_facts = host.ansible.get_variables()
    if ansible_facts['inventory_hostname'] != 'host1':
        return

    try:
        service_haproxy(host, 'stop')
        wait_awhile()
        test_vip()
    finally:
        # After the test, make sure that haproxy is started again
        service_haproxy(host, 'start')
        wait_awhile()

def service_haproxy(host, state):
    cmd = host.run("sudo systemctl " + state + " haproxy")
    assert cmd.rc == 0

def wait_awhile():
    import time
    time.sleep(10)

# Perform a cURL from the VM host system
def curl_vip():
    import subprocess
    return subprocess.call([ "/usr/bin/curl", "-vs", 
        "--connect-timeout", "1", "http://192.168.3.2"])

def test_vip():
    assert curl_vip() == 0
