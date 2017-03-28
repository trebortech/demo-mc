
# install napalm

"Install NAPALM dependencies":
  pkg.installed:
    - pkgs:
      - python-devel
      - python2-pip
      - gcc
      - openssl-devel

"Install pip NAPALM dependencies":
  pip.installed:
    - pkgs:
      - pyconfig
      - napalm-ios
    - upgrade: True
