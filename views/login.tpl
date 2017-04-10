% rebase('base.tpl', title='Login', message=message)
    <form action="/login" method="post">
      <table>
        <tr><td>User ID:</td><td><input type="text" name="uid" /></td></tr>
        <tr><td>Password:</td><td><input type="password" name="pw" /></td></tr>
      </table>
      <p>
      <input type="submit" value="Login">
    </form>

      