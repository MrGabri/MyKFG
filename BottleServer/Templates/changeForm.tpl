<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>MyKFG HomeWork Form</title>
</head>
<body style="background-color:rgb(204,204,204);">
<table width="100%">
  <tbody>
    <tr>
      <td width="10%">
        <center>
          <img src="http://www.karinthy.hu/pages/open/img/logo.png" width="160" height="160" alt=""/>
        </center><br>
        <center>
          <p><strong>MyKFG</strong><br>Homework Admin</p>
        </center>
      </td>
      <td width="80%">
        <table width="100%" border=1px style="border-collapse: collapse;">
			<tr style="background-color:rgb(128, 172, 239);">
				<td colspan="4">
					<p>
					  <center>
						<strong>Change homeworks:</strong>
					  </center>
					</p>
				</td>
			</tr>
			<tr style="background-color:rgb(160, 188, 255);">
			  <td><center>Lesson:</center></td>
			  <td><center>Homework:</center></td>
			  <td>&nbsp;</td>
			  <td><center><p>Custom date</p>
		      <p>(leave empty to use the date of the next lesson)</p></center></td>
			</tr>
            <tr style="background-color:rgb(240, 215, 117);">
				<form action="/saveData" method=POST>
				  <td width=11%>
					  <label>{{less}}</label>
				  </td>
				  <td width=56%>
					<input type="text" name="hw" value="{{hw}}" style="width:99%">
				  </td>
				  <td width=7%>
                      <input type="hidden" name="id" value={{id}}>
					  <center><input type="submit" value="Save" style="width:99%"></center>
				  </td>
				  <td width=26%>
					<input type="date" name="customDate" value={{cd}} style="width:98%">
				  </td>
				</form>
            </tr>
        </table
      </td>
    <td width="10%">&nbsp;</td>
    </tr>
<tr>
  <td>&nbsp;</td>
  <td>&nbsp;</td>
  <td>&nbsp;</td>
</tr>
<tr>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
</tr>
</tbody>
</table>
</body>
</html>
