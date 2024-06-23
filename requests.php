if ($_SERVER['REQUEST_METHOD'] === 'POST'){
    $network_name = $_POST['network_name'] ?? '';
    $password = $_POST['password'] ?? '';

    if (empty($network_name)|| empty($password)){
        echo "ネットワーク名とパスワードを入力してください";
        exit;
    }
    //ネットワーク名とパスワードを検証
    $correct_network_name = '';
    $correct_password = '';

    if ($network_name === $correct_network_name && $password == $correct_password){
        echo "接続が完了しました";
    } else {
        echo "ネットワーク名またはパスワードが正しくありません";
    }
}
