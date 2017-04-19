{% extends 'base.html' %}

{# base.html の title の中に入れるコンテンツ #}
{% block title %}
{{ name }} のページ
{% endblock %}

{# base.html の contents の中に入れるコンテンツ #}

{% block contents %}


    <form action="{{ appUrl }}/user/add" method="post">
      <table>
        <tr><td>Name:</td><td><input type="text" name="uid" /></td></tr>
        <tr><td>Password:</td><td><input type="password" name="pw" /></td></tr>
        <tr><td>Role:</td><td>
          <input type="radio" name="role" value="admin">admin
          <input type="radio" name="role" value="guest" checked>guest
        </td></tr>
      </table>
      <p>
      <input type="submit" value="submit">
    </form>
{% endblock %}

{% block sidemenu %}
C（サイドバー1）
{% endblock %}

