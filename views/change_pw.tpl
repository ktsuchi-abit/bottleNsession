{% extends 'base.html' %}

{# base.html の title の中に入れるコンテンツ #}
{% block title %}
{{ name }} のページ
{% endblock %}

{# base.html の contents の中に入れるコンテンツ #}

{% block contents %}


    <form action="{{ appUrl }}/user/pw" method="post">
      <table>
        <tr><td>Current PW:</td><td><input type="password" name="current_pw" /></td></tr>
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


