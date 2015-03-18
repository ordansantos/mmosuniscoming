

<?php
	session_start();

	if ($_SESSION['id_usuario'] != '') {
    	header ("location: home.php");
	}
	
	$user = $_SESSION['nm_usuario'];
	$foto = $_SESSION['foto'];
?>

<!DOCTYPE html>

<html>
 
	<head>
	 	<link rel="shortcut icon" href="images/favicon.png">
  		<title>IFPitaco</title>
		<meta charset="utf-8"/>
		<script src="//code.jquery.com/jquery-1.11.2.min.js"></script>
		<script src="//code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
		<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" rel="stylesheet">
		<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
		
		<link rel="stylesheet" type="text/css"  href="css/index.css">
		<link rel="stylesheet" type="text/css"  href="css/login_border.css">
		
		

  		
	</head>

	
	<script type="text/javascript">


		      
	 $(document).ready(function() {
		 
		 $("#form").submit (function(event){
			 	
			 	event.preventDefault();
				var teste;
			 	$('#login').attr ("disabled", "disabled");
			 	
				var values = $(this).serialize();
				$.ajax({		
					type: "POST",
					url: "services/login.php",
					data : values,
					success: function (data){
						console.log (data);
						if ($.trim(data) != '0')
							window.location.assign("home.php");
						 else{
							$('#error').hide();
							$('#error').fadeIn("fast", function (){
								$('#login').attr ("disabled", false);
							});
						 }
					}
				});
			
	 	});
		 
	 });
	</script>


  <body>
  	<div id="bar">
	  <div class="container-fluid">
	      <a class="navbar-header" href="index.php">
	        <img alt="Brand" src="images/logo2.png" id="logo">
	      </a>
	  </div>
	</div>
	
	<div class="container">	
	
		<div class="box-info col-md-6 " >
			<p>Proponha melhorias ao IFPB, fiscalize problemas do dia a dia e opine! Ajude no crescimento de sua instituição.</p>
		</div>
	
		<div class="col-md-4 col-sm-push-2" >
		 
	      <form class="form-signin" id="form">
	        



	        <label for="inputEmail" class="sr-only">Email address</label>
	        
	        <div class="inner-addon left-addon">
    			<i class="glyphicon glyphicon-user"></i>
	       		<input name="email" type="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus>
	        </div>
	        
	        <br/>
	        <label for="inputPassword" class="sr-only">Password</label>
	        
	        <div class="inner-addon left-addon">
    			<i class="glyphicon glyphicon-lock"></i>
	        	<input name="senha" type="password" id="inputPassword" class="form-control" placeholder="Password" required >
			</div>
			
			<br/>
			<div class="row">
				<div class="col-xs-6">
	        		<button class="btn btn-lg btn-primary btn-block" id="login" type="submit">Log in</button>
	        	</div>
	        	<div class="col-xs-6">
	        		<button onClick="parent.location='cadastrar.html'" id="signup" class="btn btn-lg btn-success btn-block" type="button">Sign up</button>
		  		</div>
		  	</div>
	    	
	      </form> 
	      <br/>
		 <div class="alert alert-danger" role="alert" id="error" style="display: none">Dados Inválidos</div>
		</div>
	</div>
	
	
	


  </body>
  
</html>
