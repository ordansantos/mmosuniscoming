

<?php
	require '../Slim/Slim/Slim.php';
	\Slim\Slim::registerAutoloader();
	$app = new \Slim\Slim();
	//$app->response()->header('Content-Type', 'application/json;charset=utf-8');
	$app->get('/', function () { 

		echo "servicos.txt \nramos.txt \n";
	});


define ('ERRO', '0');
define ('SUCESSO', '1');
define ('ERRO_STRING_VAZIA', 'Preencha todos os campos corretamente!');
define ('ERRO_EMAIL_EXISTE', 'Email já cadastrado!');
define ('ERRO_SENHA_INVALIDA', 'Sua senha precisa ter no mínimo 6 dígitos');
define ('NOT_IS_IMAGE', 'Envie um formato de imagem válido!');

$app->post('/postProposta/','postProposta');
$app->post('/postLogin/', 'postLogin');
$app->post('/postUsuario/', 'postUsuario');
$app->post('/postFiscalizacao/', 'postFiscalizacao');
/*
$app->post('/postAvaliacao/', 'postAvaliacao');
*/
$app->post('/postComentario/', 'postComentario');
$app->post('/postDeleteComentario/', 'postDeleteComentario');
$app->post('/postLaike/', 'postLaike');
$app->post('/postDeletePost/', 'postDeletePost');
$app->post('/postEnquete/', 'postEnquete');
/*
$app->get('/getPropostas/','getPropostas');
$app->get('/getPropostasByRamo/:ramo', 'getPropostasByRamo');
*/
/*
$app->get('/getFiscalizacoes/', 'getFiscalizacoes');
$app->get('/getFiscalizacoesByRamo/:ramo', 'getFiscalizacoesByRamo');
$app->get('/getAvaliacaoByRamo/:ramo', 'getAvaliacaoByRamo');
*/
$app->post('/postVoto/', 'postVoto');

$app->get('/getRamos/', 'getRamos');
$app->get('/getNomeById/:id', 'getNomeById');
$app->get('/getFotoPerfilById/:id', 'getFotoPerfilById');
$app->get('/getComentariosById/:id', 'getComentariosById');
$app->get('/getUsuarioByComentarioPostId/:comentario_post_id', 'getUsuarioByComentarioPostId');
$app->get('/getNPostsLessThanMid/:n/:m', 'getNPostsLessThanMid');
$app->get('/getAllPostsGreaterThanNid/:n', 'getAllPostsGreaterThanNid');
$app->get('/getNPosts/:n', 'getNPosts');
$app->get('/getCntLaikesAndUserFlagByPostIdAndUserId/:post_id/:usuario_id', getCntLaikesAndUserFlagByPostIdAndUserId);
$app->get('/getUsuarioByPostId/:post_id', 'getUsuarioByPostId');
$app->get('/getEnquete/:enquete_id', 'getEnquete');
$app->get('/getEnqueteIds/', 'getEnqueteIds');
$app->get('/getEnqueteIdsWhereUserDidNotVote/:usuario_id', 'getEnqueteIdsWhereUserDidNotVote');

$app->run();


/*
Json a enviar: {"comentario":"", "usuario_id":"", "ramo_id":""}

Chave estrangeira: usuario_id e ramo_id

Response: erro ou sucesso
*/

function postProposta()
{
	//Prepara a query do banco de dados
	$sql = "INSERT INTO tb_post (comentario, usuario_id, ramo_id, tipo) values (:comentario, :usuario_id, :ramo_id, 0)";
	//Inicia uma conexão com o banco
	$conn = getConn();
	//Prepara a query para receber os dados da tabela
	$stmt = $conn->prepare($sql);
	//Insere os dados

	$stmt->bindParam("comentario", $_POST['comentario']);
	$stmt->bindParam("usuario_id", $_POST['usuario_id']);
	$stmt->bindParam("ramo_id", $_POST['ramo_id']);
	
	//Executa a Query e retorna se ocorreu tudo certo
	if ($stmt->execute()) echo SUCESSO; else echo ERRO;
	
	$conn = null;
}


/*
Json(Array) a Receber:

{"propostas":[
	{"comentario":"","nm_usuario":"","data_hora":"","nm_ramo":""}
]}

*/
/*
function getPropostas()
{	
	//Realiza uma query no banco de dados em busca dos comentários
	
	$stmt = getConn()->query("
	SELECT comentario, nm_usuario, nm_ramo, data_hora, post_id, perfil_45
	FROM tb_post, tb_usuario, tb_ramo, tb_imagem_usuario
	WHERE ramo_id = id_ramo AND tb_post.usuario_id = tb_usuario.id_usuario AND tb_post.usuario_id = tb_imagem_usuario.usuario_id;");
	
	$propostas = $stmt->fetchAll(PDO::FETCH_OBJ);
	//Transforma em JSON e retorna ao cliente
	echo '{"propostas":'.utf8_encode(json_encode($propostas))."}";
}
*/
/*

Enviar ramo_id via url

Json(Array) a receber:

{"propostas":[
	{"comentario":"","nm_usuario":"","data_hora":"","nm_ramo":""}
]}


*/
/*
function getPropostasByRamo($ramo){

	$conn = getConn();

	$stmt = getConn()->prepare("
	SELECT comentario, nm_usuario, nm_ramo, data_hora 
	FROM tb_proposta, tb_usuario, tb_ramo 
	WHERE ramo_id = id_ramo AND usuario_id = id_usuario AND ramo_id = :ramo;");

	$stmt->bindParam("ramo", $ramo);
	
	$stmt->execute();
	
	$result = $stmt->fetchAll(PDO::FETCH_OBJ);
	
	echo '{"propostas":'.utf8_encode(json_encode($result))."}";
	
	$conn = null;
}
*/
//Imagem se encontra em: WebService/uploaded_images/fiscalizacao_foto/$id.jpg
function saveFiscalizacaoImage($id){
	
	if(empty($_FILES)) {
		return false;
	}
	
	require ('/var/www/html/WebService/wideimage/WideImage.php');
	
	if ($_FILES['imagem']['name']){
		
		$path = '/var/www/html/';
		$nome = 'WebService/uploaded_images/fiscalizacao_foto/'.$id.'.jpg';
		$allowedTypes = array(IMAGETYPE_PNG, IMAGETYPE_JPEG, IMAGETYPE_GIF);
		$detectedType = exif_imagetype($_FILES['imagem']['tmp_name']);
		if (in_array($detectedType, $allowedTypes)){
			
			$image = WideImage::load ($_FILES['imagem']['tmp_name']);
			$image->saveToFile($path.$nome);
			
			$sql = "INSERT INTO tb_imagem_fiscalizacao (post_id, imagem) values (:id, :imagem)";
			$conn = getConn();
			$stmt = $conn->prepare($sql);
			$stmt->bindParam("id", $id);
			$stmt->bindParam("imagem", $nome);
			
			if ($stmt->execute()) return true;
			$conn = null;
		}
	}
	return false;
}

/*
Json a enviar: {"comentario":"", "usuario_id":"", "ramo_id":""}

Resposta: erro ou sucesso
*/
function postFiscalizacao(){

	$sql = "INSERT INTO tb_post (comentario, usuario_id, ramo_id, tipo) values (:comentario, :usuario_id, :ramo_id, 1)";

	$conn = getConn();
	$stmt = $conn->prepare($sql);
	
	$stmt->bindParam("comentario", $_POST['comentario']);
	$stmt->bindParam("usuario_id", $_POST['usuario_id']);
	$stmt->bindParam("ramo_id", $_POST['ramo_id']);

	if ($stmt->execute()){
		
		$post_id = $conn->lastInsertId('post_id');
		
		if (saveFiscalizacaoImage($post_id)){
			$sql = "UPDATE tb_post SET tipo = 2 WHERE post_id = :post_id";
			$stmt = $conn->prepare ($sql);
			$stmt->bindParam ('post_id', $post_id);
			$stmt->execute();
		}
		
		echo SUCESSO;
	} else 
		echo ERRO;
	
	$conn = null;
}


/*
Json(Array) a Receber:

{"fiscalizacoes":[
	{"comentario":"","nm_usuario":"","data_hora":"","nm_ramo":""}
]}

*/
/*
function getFiscalizacoes()
{	
	
	$stmt = getConn()->query("
	SELECT comentario, nm_usuario, nm_ramo, data_hora 
	FROM tb_fiscalizacao, tb_usuario, tb_ramo 
	WHERE ramo_id = id_ramo AND usuario_id = id_usuario;");
	
	$fiscalizacoes = $stmt->fetchAll(PDO::FETCH_OBJ);
	//Transforma em JSON e retorna ao cliente
	echo '{"fiscalizacoes":'.utf8_encode(json_encode($fiscalizacoes))."}";
}
*/
/*
Json(Array) a Receber:

{"fiscalizacoes":[
	{"comentario":"","nm_usuario":"","data_hora":"","nm_ramo":""}
]}
*/
/*
function getFiscalizacoesByRamo($ramo){
	$stmt = getConn()->prepare("
	SELECT comentario, nm_usuario, nm_ramo, data_hora 
	FROM tb_fiscalizacao, tb_usuario, tb_ramo 
	WHERE ramo_id = id_ramo AND usuario_id = id_usuario AND id_ramo = :ramo;");
	
	$stmt->bindParam("ramo", $ramo);
	$stmt->execute();
	
	$result = $stmt->fetchAll(PDO::FETCH_OBJ);
	
	echo '{"fiscalizacoes":'.utf8_encode(json_encode($result))."}";	
}

*/
/*

Json a enviar: {"nota": "", "usuario_id": "", "ramo_id":""}
nota: INT(0-10)

resposta: sucesso ou erro
*/
/*
function postAvaliacao(){
	$request = \Slim\Slim::getInstance()->request();
	
	$avaliacao = json_decode($request->getBody());
	
	$sql = "INSERT INTO tb_avaliacao (nota, usuario_id, ramo_id) values (:nota, :usuario_id, :ramo_id)";

	$conn = getConn();

	$stmt = $conn->prepare($sql);

	$stmt->bindParam("nota", $avaliacao->nota);
	$stmt->bindParam("usuario_id", $avaliacao->usuario_id);
	$stmt->bindParam("ramo_id", $avaliacao->ramo_id);
	
	if ($stmt->execute()) echo SUCESSO; else echo ERRO;
}

*/
/*
Enviar ramo_id via url
Resposta : string float
*/
/*
function getAvaliacaoByRamo($ramo){

	$sql = "SELECT AVG(nota) FROM tb_avaliacao WHERE ramo_id=:ramo";
	$conn = getConn();
	$stmt = $conn->prepare($sql);
	$stmt->bindParam("ramo", $ramo);
	
	$stmt->execute();
	
	$result = $stmt->fetch();
	
	$avg =  $result['AVG(nota)'];
	
	if ($avg===NULL) $avg = 0;
	
	echo $avg;

}	
*/
/* 
Json a enviar: {"nm_usuario": "", "senha":"", "email": ""}

Resposta: erro ou sucesso
*/ 

function usuarioExiste ($email){
	
	$sql = "SELECT * FROM (tb_usuario) WHERE email = :email";
	$conn = getConn();
	$stmt = $conn->prepare ($sql);
	$stmt->bindParam("email", $email);
	$stmt->execute();
	$result = $stmt->fetch();
	
	if ($result) return true; else return false;
	$conn = null;
}

function saveFotoFromPostUsuario($email){
	
	$id = getIdByEmail($email);
	
	$novo_nome = "default";
	
	$perfil_120 ='WebService/uploaded_images/perfil_120/';
	$perfil_45 = 'WebService/uploaded_images/perfil_45/';
	$perfil_32 = 'WebService/uploaded_images/perfil_32/';
	
	if ($_FILES['foto']['name']){
		$allowedTypes = array(IMAGETYPE_PNG, IMAGETYPE_JPEG, IMAGETYPE_GIF);
		$detectedType = exif_imagetype($_FILES['foto']['tmp_name']);
		if (in_array($detectedType, $allowedTypes)){
			$novo_nome = date ("dmyhis");
			
			$image = WideImage::load ($_FILES['foto']['tmp_name']);

			
			if (isset($_POST['x']) && isset($_POST['y']) && isset($_POST['w']) && isset($_POST['h']) ){
				list($width, $height) = getimagesize($_FILES['foto']['tmp_name']);
				$image= $image->crop($_POST['x'] * $width, $_POST['y'] * $height, $_POST['w'] * $width, $_POST['h'] * $height);
			}
			
			$image->resize(120, 120, 'fill')->saveToFile('/var/www/html/'.$perfil_120.$novo_nome.'.jpg');
			$image->resize(45, 45, 'fill')->saveToFile('/var/www/html/'.$perfil_45.$novo_nome.'.jpg');
			$image->resize(32, 32, 'fill')->saveToFile('/var/www/html/'.$perfil_32.$novo_nome.'.jpg');
		}
	}

	$sql = "INSERT INTO tb_imagem_usuario (usuario_id, perfil_120, perfil_45, perfil_32) values (:id, :perfil_120, :perfil_45, :perfil_32)";
	$conn = getConn();
	
	$stmt = $conn->prepare($sql);
	
	$perfil_120 = $perfil_120.$novo_nome.'.jpg';
	$perfil_45 = $perfil_45.$novo_nome.'.jpg';
	$perfil_32 = $perfil_32.$novo_nome.'.jpg';
	
	$stmt->bindParam("id", $id);
	$stmt->bindParam("perfil_120", $perfil_120);
	$stmt->bindParam("perfil_45", $perfil_45);
	$stmt->bindParam("perfil_32", $perfil_32);
	
	$stmt->execute();
	$conn = null;
}

function postUsuario(){
	
	require ('/var/www/html/WebService/wideimage/WideImage.php');
	
	$name = $_POST['nm_usuario'];
	$senha = $_POST['senha'];
	$email = $_POST['email'];
	
	if (strlen($name) == 0 || strlen($senha) == 0 || strlen($email) == 0){
		echo ERRO_STRING_VAZIA;
		return;
	}
	
	if (strlen($senha) < 6){
		echo ERRO_SENHA_INVALIDA;
		return;
	}
	
	if (usuarioExiste ($email)){ echo ERRO_EMAIL_EXISTE; return; }
	
	$sql = "INSERT INTO tb_usuario (nm_usuario, senha, email) values (:nm_usuario, :senha, :email)";

	$conn = getConn();
	
	$stmt = $conn->prepare($sql);

	
	$stmt->bindParam("nm_usuario", $name);
	$stmt->bindParam("senha", $senha);
	$stmt->bindParam("email", $email);
	
	
	if ($stmt->execute()){
	saveFotoFromPostUsuario($email);
		echo SUCESSO; 
	}
		else 
			echo ERRO;
	$conn = null;
}

/*
POST a enviar:
	'email', 'senha'
Response: id_usuario (0 = error)

*/
function postLogin(){
	//Fazendo o select no banco com as informações enviadas
	$sql = "SELECT id_usuario FROM tb_usuario WHERE email = :email AND senha = :senha";
	$conn = getConn();
	$stmt = $conn->prepare($sql);
	$stmt->bindParam("email", $_POST['email']);
	$stmt->bindParam("senha", $_POST['senha']);
	$stmt->execute();
	$result = $stmt->fetch();
	if (!$result) echo ERRO; else echo $result['id_usuario'];
	$conn = null;
}


/*
Json(Array) a Receber:

{"ramos":[
	{"nm_ramo":"","id_ramo":""}
]}
*/
function getRamos(){
	$stmt = getConn()->query("SELECT * FROM tb_ramo");
	
	$result = $stmt->fetchAll(PDO::FETCH_OBJ);
	
	echo '{"ramos":'.utf8_encode(json_encode($result))."}";	
}

/*
 * Envia id e retorna o nome de usuário
 */
function getNomeById($id){
	
	$sql = "SELECT nm_usuario FROM tb_usuario WHERE id_usuario=:id";
	$conn = getConn();
	$stmt = $conn->prepare($sql);
	$stmt->bindParam("id", $id);
	
	$stmt->execute();
	
	$result = $stmt->fetch();
	
	echo $result['nm_usuario'];
	$conn = null;
}

function getIdByEmail($email){
	$sql = "SELECT id_usuario FROM tb_usuario WHERE email=:email";
	$conn = getConn();
	$stmt = $conn->prepare($sql);
	$stmt->bindParam("email", $email);
	
	$stmt->execute();
	
	$result = $stmt->fetch();
	
	return $result['id_usuario'];
	$conn = null;
}

//Conexão com o banco
function getConn(){
	return new PDO('mysql:host=localhost;dbname=bd_ifpitaco', 'root', '', 
	array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"));
}

function getFotoPerfilById($id){
	
	$sql = "
	SELECT perfil_120 FROM tb_imagem_usuario, tb_usuario
	WHERE tb_imagem_usuario.usuario_id = tb_usuario.id_usuario AND tb_usuario.id_usuario = :id";
	$conn = getConn();
	$stmt = $conn->prepare($sql);
	$stmt->bindParam("id", $id);
	
	$stmt->execute();
	
	$result = $stmt->fetch();
	
	echo $result['perfil_120'];
	$conn = null;
}

function postComentario (){
	
	$usuario_id = $_POST['usuario_id'];
	$post_id = $_POST['post_id'];
	$comentario = $_POST['comentario'];
	
	if (strlen($comentario) == 0){
		echo ERRO_STRING_VAZIA;
		return;
	}
	
	$sql = "INSERT INTO tb_comentario_post (usuario_id, post_id, comentario) values (:usuario_id, :post_id, :comentario)";
	
	$conn = getConn();
	
	$stmt = $conn->prepare($sql);
	
	$stmt->bindParam("usuario_id", $usuario_id);
	$stmt->bindParam("post_id", $post_id);
	$stmt->bindParam("comentario", $comentario);
	
	if ($stmt->execute())
		echo SUCESSO;
	else
		echo ERRO;
	$conn = null;
}

function postExists ($id){
	$conn = getConn();
	$sql = "SELECT EXISTS(SELECT 1 FROM tb_post WHERE post_id = :id) as cnt";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('id', $id);
	$stmt->execute();
	$result = $stmt->fetch();
	return $result['cnt'];
	$conn = null;
}

function getComentariosById ($id){

	if (postExists($id) == 0){
		echo '{"flag":"0"}';
		return;
	}
	
	$conn = getConn();
	
	$sql = "SELECT nm_usuario, id_usuario, 
			comentario, data_hora, comentario_post_id, perfil_32 FROM tb_usuario,
			tb_comentario_post, tb_imagem_usuario WHERE tb_comentario_post.usuario_id = id_usuario 
			AND tb_imagem_usuario.usuario_id = id_usuario AND post_id = :id ORDER BY comentario_post_id";
	
	$stmt = $conn->prepare($sql);
	
	$stmt->bindParam ('id', $id);
	
	$stmt->execute();
	$result = $stmt->fetchAll(PDO::FETCH_OBJ);
	echo '{ "flag": "1", "comentarios":'.utf8_encode(json_encode($result))."}";
	$conn = null;
}



function postDeleteComentario (){
	
	$conn = getConn();
	$sql = "DELETE FROM tb_comentario_post WHERE comentario_post_id = :comentario_post_id";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('comentario_post_id', $_POST['comentario_post_id']);
	
	if ($stmt->execute())
		echo SUCESSO;
	else 	
		echo ERRO;
	
	$conn = null;
}

function getUsuarioByComentarioPostId($comentario_post_id){
	$conn = getConn();
	$sql = "SELECT usuario_id FROM tb_comentario_post WHERE comentario_post_id = :id";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('id', $comentario_post_id);
	$stmt->execute();
	$result = $stmt->fetch();
	echo $result['usuario_id'];
	$conn = null;
}

//Ordenado do Maior para o menor
function getNPostsLessThanMid($n, $m){
	
	$conn = getConn();
	
	//Linha utilizada para usar o LIMIT
	$conn->setAttribute( PDO::ATTR_EMULATE_PREPARES, false );

	
	$sql = "SELECT comentario, nm_usuario, nm_ramo, data_hora, post_id, perfil_45, tb_post.usuario_id as usuario_id, tipo
			FROM tb_post, tb_usuario, tb_ramo, tb_imagem_usuario
			WHERE ramo_id = id_ramo AND tb_post.usuario_id = tb_usuario.id_usuario AND 
			tb_post.usuario_id = tb_imagem_usuario.usuario_id 
			AND post_id < :m ORDER BY post_id DESC LIMIT :n";
	
	$stmt = $conn->prepare($sql);
	
	$stmt->bindParam('n', $n);
	$stmt->bindParam('m', $m);
	 
    $stmt->execute();
	
	$posts = $stmt->fetchAll(PDO::FETCH_OBJ);

	echo '{"posts":'.utf8_encode(json_encode($posts))."}";
	$conn = null;
}

//Ordenado do menor para o maior
function getAllPostsGreaterThanNid($n){

	$conn = getConn();

	$sql = "SELECT comentario, nm_usuario, nm_ramo, data_hora, post_id, perfil_45, tb_post.usuario_id as usuario_id, tipo
			FROM tb_post, tb_usuario, tb_ramo, tb_imagem_usuario
			WHERE ramo_id = id_ramo AND tb_post.usuario_id = tb_usuario.id_usuario AND
			tb_post.usuario_id = tb_imagem_usuario.usuario_id
			AND post_id > :n ORDER BY post_id";

	$stmt = $conn->prepare($sql);

	$stmt->bindParam('n', $n);

	$stmt->execute();

	$posts = $stmt->fetchAll(PDO::FETCH_OBJ);

	echo '{"posts":'.utf8_encode(json_encode($posts))."}";
	$conn = null;
}


//Ordenado do Maior para o menor
function getNPosts($n){
	
	$conn = getConn();
	
	//Linha utilizada para usar o LIMIT
	$conn->setAttribute( PDO::ATTR_EMULATE_PREPARES, false );

	
	$sql = "SELECT comentario, nm_usuario, nm_ramo, data_hora, post_id, perfil_45, tb_post.usuario_id as usuario_id, tipo
			FROM tb_post, tb_usuario, tb_ramo, tb_imagem_usuario
			WHERE ramo_id = id_ramo AND tb_post.usuario_id = tb_usuario.id_usuario AND 
			tb_post.usuario_id = tb_imagem_usuario.usuario_id 
			ORDER BY post_id DESC LIMIT :n";
	
	$stmt = $conn->prepare($sql);
	
	$stmt->bindParam('n', $n, PDO::PARAM_INT);
	 
    $stmt->execute();
	
	$posts = $stmt->fetchAll(PDO::FETCH_OBJ);

	echo '{"posts":'.utf8_encode(json_encode($posts))."}";
	$conn = null;
}

function deleteLaike(){
	$conn = getConn();
	$sql = "DELETE FROM tb_laikar WHERE post_id = :post_id AND usuario_id = :usuario_id";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('usuario_id', $_POST['usuario_id']);
	$stmt->bindParam ('post_id', $_POST['post_id']);
	
	if ($stmt->execute())
		return SUCESSO;
	else 	
		return ERRO;
	$conn = null;
}

//Se enviar um post de like existente, o mesmo é apagado
function postLaike (){
	
	$conn = getConn();
	
	$sql = "INSERT INTO tb_laikar (usuario_id, post_id) values (:usuario_id, :post_id)";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('usuario_id', $_POST['usuario_id']);
	$stmt->bindParam ('post_id', $_POST['post_id']);

	if ($stmt->execute())
		echo SUCESSO;
	else 	
		echo deleteLaike();
	$conn = null;
}

//Flag responde se usuário curtiu

function doesUserLaike($usuario_id, $post_id){
	$conn = getConn();
	$sql = "SELECT EXISTS(SELECT 1 FROM tb_laikar WHERE post_id = :post_id AND usuario_id = :usuario_id) as cnt";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('post_id', $post_id);
	$stmt->bindParam ('usuario_id', $usuario_id);
	$stmt->execute();
	$result = $stmt->fetch();
	return $result['cnt'];
	$conn = null;
}

function getCntLaikesAndUserFlagByPostIdAndUserId ($post_id, $usuario_id){
	
	$conn = getConn();
	$sql = "SELECT COUNT(*) as cnt FROM tb_laikar WHERE post_id = :post_id";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('post_id', $post_id);
	$stmt->execute();
	$result = $stmt->fetch();
	echo '{"flag":"'.doesUserLaike($usuario_id, $post_id).'", "cnt":"'.$result['cnt'].'"}';
	$conn = null;
}

function getUsuarioByPostId($post_id){
	$conn = getConn();
	$sql = "SELECT usuario_id FROM tb_post WHERE post_id = :id";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('id', $post_id);
	$stmt->execute();
	$result = $stmt->fetch();
	echo $result['usuario_id'];
	$conn = null;
}

function postDeletePost (){
	
	$conn = getConn();
	$sql = "DELETE FROM tb_post WHERE post_id = :post_id";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('post_id', $_POST['post_id']);
	
	if ($stmt->execute())
		if (deleteComentarioByPost($_POST['post_id'])){
			echo deleteLaikeByPost($_POST['post_id']);
			return;
		}
	
	echo ERRO;
	$conn = null;
}


function deleteComentarioByPost ($post_id){

	$conn = getConn();
	$sql = "DELETE FROM tb_comentario_post WHERE post_id = :post_id";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('post_id', $_POST['post_id']);

	if ($stmt->execute())
		return SUCESSO;
	$conn = null;
	return	ERRO;
}

function deleteLaikeByPost ($post_id){

	$conn = getConn();
	$sql = "DELETE FROM tb_laikar WHERE post_id = :post_id";
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('post_id', $_POST['post_id']);

	if ($stmt->execute())
		return SUCESSO;
	$conn = null;
	return	ERRO;
}


function saveEnqueteImage($id){

	require ('/var/www/html/WebService/wideimage/WideImage.php');
	
	$path_image = "";
	
	if(!empty($_FILES))
	if ($_FILES['imagem']['name']){
	
		$path = '/var/www/html/';
		$nome = 'WebService/uploaded_images/enquete_foto/'.$id.'.jpg';
		
		$allowedTypes = array(IMAGETYPE_PNG, IMAGETYPE_JPEG, IMAGETYPE_GIF);
		$detectedType = exif_imagetype($_FILES['imagem']['tmp_name']);
		if (in_array($detectedType, $allowedTypes)){
				
			$image = WideImage::load ($_FILES['imagem']['tmp_name']);
			$image->saveToFile($path.$nome);
			$path_image = $nome;

		}
	}
	
	$sql = "INSERT INTO tb_imagem_enquete (enquete_id, imagem) values (:id, :imagem)";
	$conn = getConn();
	$stmt = $conn->prepare($sql);
	$stmt->bindParam("id", $id);
	$stmt->bindParam("imagem", $path_image);
	
	$conn = null;
	if ($stmt->execute()) return true;
	
	return false;
}


function postEnquete(){
	
	$conn = getConn();
	
	$sql = "INSERT INTO tb_enquete
			(usuario_id, titulo, opt_1, opt_2, opt_3, opt_4, opt_5, qtd_opt)
			VALUES (:usuario_id, :titulo, :opt_1, :opt_2, :opt_3, :opt_4, :opt_5, :qtd_opt)";
	
	$opt = array ("", "", "", "", "", "");
	
	for ($i = 0; $i < $_POST['qtd_opt']; $i++)
		$opt[$i] = $_POST['opt_'.($i + 1)];
	
	$stmt = $conn->prepare($sql);
	
	$stmt->bindParam('usuario_id', $_POST['usuario_id']);
	$stmt->bindParam('titulo', $_POST['titulo']);
	$stmt->bindParam('qtd_opt', $_POST['qtd_opt']);
	
	for ($i = 0; $i < $_POST['qtd_opt']; $i++)
		$opt[$i] = $_POST['opt_'.($i + 1)];
	
	for ($i = 1; $i <= 5; $i++)
		$stmt->bindParam('opt_'.$i, $opt[$i-1]);	
	
	if ($stmt->execute()){
		$id_enquete = $conn->lastInsertId('id_enquete');
		saveEnqueteImage($id_enquete);
		echo $id_enquete;
	}
	else 
		echo ERRO;
	$con = null;
}

function getEnquete($id){
	
	$sql = "
		SELECT 
		e.qtd_opt, e.opt_1, e.opt_2, e.opt_3, e.opt_4, e.opt_5, e.titulo, e.id_enquete, e.usuario_id, e.data_hora,
		i_e.imagem as e_imagem, u.nm_usuario,
		iu.perfil_45,
		
		(SELECT COUNT(*) FROM tb_enquete_voto WHERE enquete_id = :id AND voto = 1) as qtd_opt_1,
		(SELECT COUNT(*) FROM tb_enquete_voto WHERE enquete_id = :id AND voto = 2) as qtd_opt_2,
		(SELECT COUNT(*) FROM tb_enquete_voto WHERE enquete_id = :id AND voto = 3) as qtd_opt_3,
		(SELECT COUNT(*) FROM tb_enquete_voto WHERE enquete_id = :id AND voto = 4) as qtd_opt_4,
		(SELECT COUNT(*) FROM tb_enquete_voto WHERE enquete_id = :id AND voto = 5) as qtd_opt_5
		
		FROM tb_enquete as e, tb_imagem_enquete as i_e, tb_usuario as u, tb_imagem_usuario as iu
		
		WHERE i_e.enquete_id = e.id_enquete AND u.id_usuario = e.usuario_id AND iu.usuario_id = e.usuario_id 
		AND e.id_enquete = :id ORDER BY e.id_enquete
			";
	
	$conn = getConn();
	$stmt = $conn->prepare($sql);
	$stmt->bindParam("id", $id);
	$stmt->execute();
	$enquete = $stmt->fetchAll(PDO::FETCH_OBJ);
	echo utf8_encode(json_encode($enquete));
	$conn = null;
}

function postVoto(){
	ECHO 'AQUI';
	print_r($_POST);
	$sql = "INSERT INTO tb_enquete_voto (usuario_id, enquete_id, voto) VALUES (:usuario_id, :enquete_id, :voto)";
	
	$conn = getConn();
	$stmt = $conn->prepare($sql);
	$stmt->bindParam ('usuario_id', $_POST['usuario_id']);
	$stmt->bindParam ('enquete_id', $_POST['enquete_id']);
	$stmt->bindParam ('voto', $_POST['voto']);
	
	if ($stmt->execute())
		echo SUCESSO;
	else 
		echo ERRO;
	$conn = null;
}

function getEnqueteIds(){
	
	$sql = "SELECT id_enquete FROM tb_enquete";
	$conn = getConn();
	$stmt = $conn->prepare($sql);
	$stmt->execute();
	$ids = $stmt->fetchAll(PDO::FETCH_OBJ);
	echo '{"ids":'.utf8_encode(json_encode($ids))."}";
	$conn = null;
}

function getEnqueteIdsWhereUserDidNotVote($id){
	
	$sql = "SELECT id_enquete FROM tb_enquete WHERE id_enquete NOT IN (
			SELECT enquete_id FROM tb_enquete_voto WHERE usuario_id = :id)";
	$conn = getConn();
	$stmt = $conn->prepare($sql);
	$stmt->bindParam('id', $id);
	$stmt->execute();
	$ids = $stmt->fetchAll(PDO::FETCH_OBJ);
	echo '{"ids":'.utf8_encode(json_encode($ids))."}";
	$conn = null;
}

