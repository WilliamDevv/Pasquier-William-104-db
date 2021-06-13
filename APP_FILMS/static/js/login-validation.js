$(function() {
    $("form[name='login-form']").validate({
        rules: {
            pseudo: "required",
            password: {
                required: true,
                minlength: 6
            }
        },
        messages: {
            pseudo: "Entrez votre pseudo",
            password: {
                required: "Entrez votre mot de passe",
                minlength: "La taille minimum est de 6 caractères"
            }
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
});