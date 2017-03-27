"Python Pip":
  pkg.installed:
    - name: python2-pip

"Update PIP":
  cmd.run:
    - name: 'easy_install -U pip'
    - require:
      - pkg: 'Python Pip'