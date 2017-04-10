<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/style.css?1" type="text/css" />
</head>
<body>
<div id="container">
  {# ヘッダー #}
　<div id="boxA">{% block header %}{% endblock %}</div>

　<div id="wrapper">
    {# コンテンツ #}　　
    <div id="boxB">{% block contents %}{% endblock %}</div>
    {# サイドメニュー #}　　
    <div id="boxC">{% block sidemenu %}{% endblock %}</div>
　</div>
  {# 全体メニュー #}
　<div id="boxD">{% block globalmenu %}{% endblock %}</div>
  {# フッター #}
　<div id="boxE">{% block footer %}{% endblock %}</div>
</div>
</body>
</html>