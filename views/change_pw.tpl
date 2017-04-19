{% extends 'base.html' %}

{# base.html の title の中に入れるコンテンツ #}
{% block title %}
{{ name }} のページ
{% endblock %}

{# base.html の contents の中に入れるコンテンツ #}

{% block contents %}


    <form action="{{ appUrl }}/user/pw" method="post">
      <input type="hidden" name="from_show_users" value="{{from_show_users}}">
      <input type="hidden" name="user" value="{{user}}">
      <table>
      {% if not role=='admin': %}
        <tr><td>Current PW:</td><td><input type="password" name="current_pw" /></td></tr>
      {% endif %}
        <tr><td>New PW:</td><td><input type="password" name="new_pw1" /></td></tr>
        <tr><td>New PW:</td><td><input type="password" name="new_pw2" /></td></tr>
      </table>
      <p>
      <input type="submit" value="submit">
    </form>
{% endblock %}

{% block sidemenu %}
C（サイドバー1）
{% endblock %}


