% rebase('base.tpl', title='User List')

    <table border="1">
      <tr><th>UID</th><th>Role</th></tr>
      % for uid, role in users:
      <tr><td>{{uid}}</td><td>{{role}}</td></tr>
      % end
    </table>
  <p>
  <a href="/">TOP</a>     
