$(document).ready(function(){
$("#createIdeaForm").validate({
			rule:{
				title:{
					required: true
				},
				description:{
					required: true,
					minLength: 6
				}
			},
			message:{
				title:{
					required: "title is required"
				},
				description:{
					required: "Descripton is Required",
					minLength: "It should be atleast 6 characters"
				}
			}
		});
});