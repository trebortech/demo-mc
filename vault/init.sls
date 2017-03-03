{% set vaultbin = 'vault_0.6.4_linux_amd64.zip' %}

"Download and unzip vault binary":
  archive.extracted:
    - name: '/vault'
    - source: salt://vault/{{ vaultbin }}
    - archive_format: zip
    - enforce_toplevel: False

"Stage vault startup script":
  file.managed:
    - name: /etc/init.d/vault
    - source: salt://vault/vault.sh
    - user: root
    - group: root
    - mode: 755

"Create sym link to vault":
  file.symlink:
    - name: '/usr/bin/vault'
    - target: '/vault/vault'

"Deploy config":
  file.managed:
    - name: '/etc/vault.d/config.json'
    - source: salt://vault/base.conf
    - makedirs: True

"Set environment variable for vault":
  environ.setenv:
    - name: 'VAULT_ADDR'
    - value: 'http://127.0.0.1:8200'

"Start vault service":
  service.running:
    - name: vault
    - enable: True
    - require:
      - file: "Stage vault startup script"
