# Deploy Demo Code


"Stage sample files":
  file.recurse:
    - name: '/srv/pillar/napalm/'
    - source: salt://napalm/
    - makedirs: True

"Deploy proxy config":
  file.managed:
    - name: '/etc/salt/proxy.d/base.conf'
    - source: salt://napalm/base.conf
    - makedirs: True
