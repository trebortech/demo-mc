{% if data['fun_args'][0]['test'] is defined %}
{% if data['fun_args'][0]['test'] == true %}

{% set returns = data['return'] %}

{% for return in returns %}
{% if returns[return]['result'] == None %}
'Send out of compliance event':
  runner.event.send:
    - tag: 'OutOfCompliance'
    - data: {
            'minionid': data['id'],
            'return': {{ returns[return]['__id__'] }}
            }
{% endif %}
{% endfor %}

{% endif %}
{% endif %}