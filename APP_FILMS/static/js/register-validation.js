$(function() {
    $("form[name='register-form']").validate({
        rules: {
            name: "required",
            firstname: "required",
            pseudo: "required",
            birthdate: {
                date: true,
                required: true,
                maxDate: true,
                minDate: true
            },
            mail: {
                email: true,
                required: true,
                maxlength: 320
            },
            confirm_mail: {
                email: true,
                required: true,
                maxlength: 320,
                equalTo: "#mail"
            },
            password: {
                required: true,
                minlength: 6
            },
            confirm_password: {
                required: true,
                minlength: 6,
                equalTo: "#password"
            }
        },
        messages: {
            name: "Entrez votre nom de famille",
            firstname: "Entrez votre prénom",
            pseudo: "Entrez votre pseudo",
            birthdate: {
                required: "Entrez votre date de naissance",
                maxDate: "La date de naissance est trop récente",
                minDate: "La date de naissance est trop vieille"
            },
            mail: {
                required: "Entrez votre adresse mail",
                maxlength: "La taille maximum est de 320 caractères"
            },
            confirm_mail: {
                required: "Entrez la confirmation de votre adresse mail",
                maxlength: "La taille maximum est de 320 caractères",
                equalTo: "L'adresse mail doit être similaire"
            },
            password: {
                required: "Entrez votre mot de passe",
                minlength: "La taille minimum est de 6 caractères"
            },
            confirm_password: {
                required: "Entrez la confirmation de votre mot de passe",
                minlength: "La taille minimum est de 6 caractères",
                equalTo: "Le mot de passe doit être similaire"
            }
        },
        submitHandler: function(form) {
            form.submit();
        }
    });

    $.validator.addMethod("maxDate", function(value, element) {
        var curDate = new Date();
        var inputDate = new Date(value);

        if(inputDate < curDate)
            return true;
        return false;
    }, "Date trop récente");

    $.validator.addMethod("minDate", function(value, element) {
        var minDateValue = new Date("1920-01-01");
        var inputDate = new Date(value);

        if(inputDate > minDateValue)
            return true;
        return false;
    }, "Date trop vieille");
});