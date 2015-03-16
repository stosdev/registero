{% load i18n %}
{% trans "Institute name" %}: {{ coach_profile.institute_name }}, {% trans "Coach" %}: {{ coach_profile.user }} ({{ coach_profile.user.email }})
-----------

{% trans "Institute type" %}: {{ coach_profile.get_institute_type_display }}

{% trans "Accomodation required" %}: {{ coach_profile.accomodation_required|yesno }}
{% if coach_profile.accomodation_required %}
{% trans "Institute address" %}: {{ coach_profile.institute_address }}

{% trans "Institutes NIP" %}: {{ coach_profile.institute_nip }}
{% endif %}
{% trans "Comment" %}: {{ coach_profile.comment }}
{% for team in coach_profile.user.teams.all %}
{% trans "Team" %} {{ team.order }}
{% for participant in team.participants.all %}
  * {{ participant.first_name }} {{ participant.last_name }}, {% trans "Shirt size" %}: {{ participant.shirt_size }}
{% endfor %}

{% endfor %}
