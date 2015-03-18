

<!DOCTYPE html>

<html>
 
	<head>
	 	<link rel="shortcut icon" href="images/favicon.png">
  		<title>Sun is Coming</title>
		<meta charset="utf-8"/>
		<script src="//code.jquery.com/jquery-1.11.2.min.js"></script>
		<script src="//code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
		<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" rel="stylesheet">
		<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
		
		<link rel="stylesheet" type="text/css"  href="index.css">
		<link rel="stylesheet" type="text/css"  href="login_border.css">
		<script src="bootbox.min.js"></script>
		

  		
	</head>

	
	<script type="text/javascript">


		      
	 $(document).ready(function() {
		 
		 $("#form").submit (function(event){
			 	event.preventDefault();

			 	$('#signup').attr ("disabled", "disabled");
			 	
				var values = $(this).serialize();
				
				$.ajax({		
					type: "POST",
					url: "WebService/postUsuario",
					data : values,
					success: function (data){
						
						if ($.trim(data) == 1){
							
							bootbox.alert("Cadastro realizado com sucesso, vá se divertir! ;)", function() {
							  $('#signup').attr ("disabled", false);
							  $('#error').hide();
							  $('#inputPassword').val("")
							  $('#inputEmail').val("")
							  rankLoad()
							});
						} else{
						
							$('#error').hide();
							document.getElementById ('error').innerHTML = data
						
							$('#error').fadeIn("fast", function (){
								$('#signup').attr ("disabled", false);
							});
						}
		
					}, error: function (data){
						console.log (data)
						$('#signup').attr ("disabled", false);
					}
				});
			
	 	});
		 
	 });
	 
	 
	 
	function rankLoad(){

	  $.ajax({ 
		type: 'GET', 
		url: 'WebService/getRank', 
		data: { get_param: 'value' }, 
			dataType:'json',
			cache: false,
		  success: function (data) { 
			 document.getElementById('table').innerHTML = '<tr>\
						<td>\
							#\
						</td>\
                        <td>\
                            Usuários\
                        </td>\
                        <td >\
                            Kills\
                        </td>\
                    </tr>'
			 for (i = 0; i < data.rank.length; i++){

				r = data.rank[i];

				tr = document.createElement ('tr');
				c1 = '<td>'+ (i + 1) +'</td>'
				c2 = '<td>'+ r.nm_email +'</td>'
				c3 = '<td>'+ r.nr_killed + '</td>'
				tr.innerHTML = c1 + c2 + c3
				
				document.getElementById('table').appendChild(tr)
				
			}
			 
		  }
	  });

	}
	
	$(document).ready(function() {
		rankLoad();
		setInterval(function () {rankLoad()}, 10000);
	});
	</script>


  <body>

	
	<div class="container">	
	
		
		<div id="rank" class="col-md-5  col-sm-push-3" >
			
<div class="CSSTableGenerator" >
                <table class="table" id='table'>
                    <tr>
						<td>
							#
						</td>
                        <td>
                            Usuários
                        </td>
                        <td >
                            Kills
                        </td>
                    </tr>
 
                </table>
            </div>
            
			
		</div>
		
	
		<div class="col-md-3  col-sm-push-4" >
	      <form class="form-signin" id="form">
	        <label for="inputEmail" class="sr-only">Username</label>
	        
	        <div class="inner-addon left-addon">
    			<i class="glyphicon glyphicon-user"></i>
	       		<input name="email" type="text" id="inputEmail" class="form-control" placeholder="Usuário" autofocus>
	        </div>
	        
	        <br/>
	        <label for="inputPassword" class="sr-only">Password</label>
	        
	        <div class="inner-addon left-addon">
    			<i class="glyphicon glyphicon-lock"></i>
	        	<input name="senha" type="password" id="inputPassword" class="form-control" placeholder="Senha" >
			</div>
			
			<br/>
			<div class="row">
	        	<div class="col-xs-12">
	        		<button type="submit"  id="signup" class="btn btn-lg btn-danger btn-block" type="button">Cadastrar</button>
		  		</div>
		  	</div>
	    			 <div class="alert alert-danger" role="alert" id="error" style="display: none">Dados Inválidos</div>
		</div>
	      </form> 
	      <br/>
	      
	      
</div>   
	      
	 	<div id="footer" >
			<div id="disc" class="center-block">	    


<div id="disqus_thread"></div>
<script type="text/javascript">
    /* * * CONFIGURATION VARIABLES * * */
    var disqus_shortname = 'suniscoming';
    
    /* * * DON'T EDIT BELOW THIS LINE * * */
    (function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
</script>

<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>

			</div>

		</div>
	



  </body>
  
</html>
