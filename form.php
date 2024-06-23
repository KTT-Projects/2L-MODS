<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NETWORK FORM</title>
</head>
<body>
    <h2>ネットワークの登録</h2>
    <form action="insert_network.php" method="POST">
    <label for="network_name">Network Name:</label>
    <input type="text" id="network_name" name="network_name" required>
    <br>
    <label for="password">Password</label>
    <input type="text" id="password" name="password" required>
    <br>
    <input type="submit" value="登録">
    </form>
</body>
</html>