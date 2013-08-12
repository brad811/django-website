var validated = false;

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]'));
        }
    }
});

$('#registration_form').submit(function(event) {
	if(!validated) {
		event.preventDefault();
		$.ajax({
			type: "POST",
			url:"/register/",
			data: {
				signup_name: $('#signup_name').val(),
				signup_email: $('#signup_email').val(),
				signup_password: $('#signup_password').val(),
				csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
			},
			success:function(result) {
				result = result.split(",")
				if(result[0] == "valid") {
					validated = true;
					$('form').submit();
				}
				else {
					$("#registration_error").html(result[1]).show();
				}
			}
		});
	}
});

$('#login_form').submit(function(event) {
	if(!validated) {
		event.preventDefault();
		$.ajax({
			type: "POST",
			url:"/login/",
			data: {
				login_email: $('#login_email').val(),
				login_password: $('#login_password').val(),
				remember_me: $('#remember_me').is(':checked'),
				csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
			},
			success:function(result) {
				result = result.split(",")
				if(result[0] == "valid") {
					validated = true;
					$('form').submit();
				}
				else {
					$("#login_error").html(result[1]).show();
				}
			}
		});
	}
});
