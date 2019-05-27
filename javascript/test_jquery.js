// Unlike vanilla js
// $ is working as querySelectorAll()
$("li");
$('#submit').click(function(){
	console.log("Click");
	$('#table').append("<tr> <td scope='row'> Third1 </td> </tr>");
	//$('#table > tbody:last-child').append('<tr>...</tr><tr>...</tr>');
});
