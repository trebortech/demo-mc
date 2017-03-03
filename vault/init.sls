{% set vaultbin = 'vault_0.6.4_linux_amd64.zip' %}

"Download and unzip vault binary":
  archive.extracted:
    - name: '/vault'
    - source: salt://vault/{{ vaultbin }}
    - archive_format: zip


"Deploy config":
  file.managed:
    - name: '/vault/bases.conf'
    - source: salt://vault/base.conf

"Set environment variable for vault":
  environ.setenv:
    - name: 'VAULT_ADDR'
    - value: 'http://127.0.0.1:8200'
