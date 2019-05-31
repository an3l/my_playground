var klikovi=0;

$(document).ready(function(){
    $('#table_div_priznanje').hide();
		klikovi=0;
});
//
//<td> <a href="{% url 'tehnicka:delete' ucenik.id %}"> <span> Izbriši </span><i class="fa fa-user"></i> </a> </td>
$('#priznanja_btn').click(function(){
	var url_brisi = "{% url 'tehnicka:index' ucenik.id %}";//delete_priznanje
	klikovi=klikovi+1;
	if(klikovi>0){
	  $('body #table_div_priznanje').show();
		$('#table_priznanje tr:last').after('<tr id="brisi_red"> \
		<td class="table-light"> <input type="text" min=2 max=5 name="priznanje_naziv" value=""> </td>\
		<td class="table-light"> <input type="number" name="priznanje_bodovi" min="0" placeholder="0" value=""> </td>\
		<td class="table-light"> <a href="#" id="brisi_priznanje" class="brisime"> <span> Izbrisi </span><i class="fa fa-trash"></i> </a> </td>\
		</tr>');

// @todo dodati vrstu takmicenja
		// <td class="table-light"> <input type="text" name="vrsta_takmicenja" value=""> </td>\
		// <td>
		// 	<select class="" name="smjer">
		// 	{% for tip in vrsta_takmicenja %}
		// 		<option value="{{tip.id}}"> "{{tip.naziv}}"</option>
		// 	{% endfor%}
		// 	</select>
		// </td>

		$('.brisime').click(function(){
				$(this).closest('tr').remove();
			// console.log(clicked.index());
			//$(clicked).parent().parent().remove();
		});
	}


});

// $('#priznanja_btn').click(function(){
// 	console.log("Click");
// 	$('#table_priznanje').append('
//     <tr>
//       <td> <input type="number" min=2 max=5 name="razred5" value=""> </td>
//       <td> <input type="number" min=2 max=5 name="razred5" value=""> </td>
//     </tr>
// ');
// 	//$('#table > tbody:last-child').append('<tr>...</tr><tr>...</tr>');
// });
