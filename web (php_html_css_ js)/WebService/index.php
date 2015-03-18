

<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

require '../Slim/Slim/Slim.php';
\Slim\Slim::registerAutoloader();

$app = new \Slim\Slim();

//$app->response()->header('Content-Type', 'application/json;charset=utf-8');

$app->get('/', function () { 

	echo "Sun Is Coming!";
});

define ('ERRO', 'Erro no banco de dados');
define ('SUCESSO', '1');
define ('ERRO_STRING_VAZIA', 'Preencha todos os campos corretamente!');
define ('ERRO_EMAIL_EXISTE', 'Usuário já cadastrado!');
define ('ERRO_SENHA_INVALIDA', 'Sua senha precisa ter no mínimo 6 dígitos');

$app->post('/postUsuario/', 'postUsuario');

$app->get('/getRank/', 'getRank');

$app->run();

function postUsuario(){

	$senha = $_POST['senha'];
	$email = $_POST['email'];
	
	if (strlen($senha) == 0 || strlen($email) == 0){
		echo ERRO_STRING_VAZIA;
		return;
	}
	
	if (strlen($senha) < 6){
		echo ERRO_SENHA_INVALIDA;
		return;
	}
	
	if (usuarioExiste ($email)){ echo ERRO_EMAIL_EXISTE; return; }
	
	$sql = "INSERT INTO tb_master (nm_password, nm_email) values (:senha, :nm_email)";

	$conn = getConn();
	
	$stmt = $conn->prepare($sql);

	
	$stmt->bindParam("senha", $senha);
	$stmt->bindParam("nm_email", $email);
	
	
	if ($stmt->execute())
		echo SUCESSO; 
	else
		echo ERRO;
	$conn = null;
}

/*Verifica se o usuário com o seguinte email existe.*/
function usuarioExiste ($email){
	
	$sql = "SELECT * FROM (tb_master) WHERE nm_email = :nm_email";
	$conn = getConn();
	$stmt = $conn->prepare ($sql);
	$stmt->bindParam("nm_email", $email);
	$stmt->execute();
	$result = $stmt->fetch();
	
	if ($result) return true; else return false;
	$conn = null;
}

function getRank(){
	
	$stmt = getConn()->query("SELECT nm_email, nr_killed FROM tb_master ORDER BY nr_killed DESC");
	
	$result = $stmt->fetchAll(PDO::FETCH_OBJ);
	
	echo '{"rank":'.utf8_encode(json_encode($result))."}";	
}



//Conexão com o banco
function getConn(){
	return new PDO('mysql:host=localhost;dbname=suniscoming', 'root', '', 
	array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"));
}



