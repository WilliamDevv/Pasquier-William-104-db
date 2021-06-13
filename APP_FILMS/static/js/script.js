document.addEventListener("DOMContentLoaded", (event) => {
    var dateField = document.getElementById("birthdate");

    document.getElementById("register-button").addEventListener("click", (event) => {
        console.log(dateField.value);
        var inputDate = new Date(dateField.value);
        var ctrlDate = new Date("1920-01-01");

        if(inputDate > ctrlDate)
            console.log(true)
        else
            console.log(false);
    })
});