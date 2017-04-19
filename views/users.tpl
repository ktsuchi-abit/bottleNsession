{% extends 'base.html' %}

{# base.html の title の中に入れるコンテンツ #}
{% block title %}
{{ name }} のページ
{% endblock %}

{# base.html の contents の中に入れるコンテンツ #}

{% block contents %}
    <table border="1">
      <tr><th>UID</th><th>Role</th><th>パスワード変更</th></tr>
      {% for uid, role in users: %}
      <tr><td>{{uid}}</td><td>{{role}}</td><td><a href="{{ appUrl }}/user/pw?user={{ uid }}&from_show_users=1">Change</a></td></tr>
      {% endfor %}
    </table>
{% endblock %}

{% block sidemenu %}
C（サイドバー1）
{% endblock %}
 
