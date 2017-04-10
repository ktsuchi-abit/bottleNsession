{% extends 'base.html' %}

{# base.html の title の中に入れるコンテンツ #}
{% block title %}
{{ name }} のページ
{% endblock %}

{# base.html の contents の中に入れるコンテンツ #}
{% block contents %}
B（メインカラム）<br>B（メインカラム）2
{% endblock %}

{% block sidemenu %}
C（サイドバー2）
{% endblock %}
