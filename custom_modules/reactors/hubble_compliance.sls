{% if data['fun'] is defined %}
{% if data['fun'] == 'hubble.audit' %}

{% set compliance = data['return']['Compliance'][:-1]|int %}

{% if compliance < 100 %}
'Send out of compliance event':
  runner.event.send:
    - tag: 'OutOfCompliance'
    - data: {
            'minionid': {{ data['id'] }},
            'Compliance': {{ compliance }}
            }
{% endif %}

{% endif %}
{% endif %}