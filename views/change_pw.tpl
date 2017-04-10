% rebase('base.tpl', title='Change PW', message=message)

    <form action="/user/pw" method="post">
      <table>
        <tr><td>Current PW:</td><td><input type="password" name="current_pw" /></td></tr>
        <tr><td>New PW:</td><td><input type="password" name="new_pw1" /></td></tr>
        <tr><td>New PW:</td><td><input type="password" name="new_pw2" /></td></tr>
      </table>
      <p>
      <input type="submit" value="submit">
    </form>
    <p>
    <a href="/">TOP</a>
