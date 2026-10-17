# Competition-related participant-facing views live in core/views.py (home, dashboard, rules),
# since they're composed with data from teams/challenges too. This app exposes its data via
# competitions.services.get_current_competition() and its Django admin configuration instead.
