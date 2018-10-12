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
      <td width="10%"><center>
          <img src="http://www.karinthy.hu/pages/open/img/logo.png" width="160" height="160" alt=""/>
        </center><br>
        <center>
      <p><strong>MyKFG</strong><br>
        Homework Admin </p>
    </center></td>
        </td>
      <td width="80%"><table width="100%" border=1px style="border-collapse: collapse;">
          <p>
            <center>
              <strong>Homeworks:</strong>
            </center>
          </p>
          <tbody border=0px>
            <tr style="background-color:rgb(128, 172, 239);"> </tr>
        </table
				
</table>
<table width="100%" border=1px style="border-collapse: collapse;">
  <tbody border=0px>
    <tr style="background-color:rgb(160, 188, 255);">
      <td width="13%">Date:</td>
      <td width="13%">Date of the Next lesson:</td>
      <td width="10%">Lesson:</td>
      <td width="64%">Homeworks:</td>
    </tr>
    %counter = True
    %for hw in homeworks:
        %hwid = hw["id"]
        %if counter:
            <tr style="background-color:rgb(240, 215, 117);"> 
        %else:
            <tr style="background-color:rgb(240, 234, 162);"> 
        %end
                <td>{{hw["Date"]}}</td>
                <td>{{hw["nextLessonDate"]}}</td>
                <td>{{hw["Lesson"]}}</td>
                <td>{{hw["HW"]}}</td>
            </tr>
        %counter = not counter
    %end
    <tr style="background-color:rgb(128, 172, 239);">
        <td colspan="5">
        <a href="http://37.221.213.41/login"><center><strong>Login</strong></center></a> 
        </td>
    </tr>
  </tbody>
  
</table>
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