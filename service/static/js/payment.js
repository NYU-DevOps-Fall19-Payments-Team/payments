$(function () {
    // ****************************************
    // UTILITY FUNCTION
    // ****************************************

    // Show the error message.
    function showError(error) {
        let errorMessage = $(".error");
        errorMessage.css("display", "block");
        errorMessage.text(error.message);
    }

    // Show the success message.
    function showSuccess(message){
        let successMessage = $(".success");
        successMessage.css("display", "block");
        successMessage.text(message);
    }

    // Hide all the message.
    function hideMessage(){
        let successMessage = $(".success");
        successMessage.css("display", "none");
        let errorMessage = $(".error");
        errorMessage.css("display", "none");
    }

    // ****************************************
    // Read all the payments
    // ****************************************

    // load all the payments from the database, insert it into table.
    console.log("----------loading table------------")
    var ajax = $.ajax({
        type: "GET",
        url: "/payments",
        contentType: "application/json"
    });

    ajax.done(function(res){
        for(i = 0; i < res.length; i++)
            addRow(res[i])
    });
    
    function addRow(payment){
        let type = payment.type;
        let id = payment.id;
        let info;
        switch (type){
            case "credit card":
                info = payment.info.credit_card_number;
                $("#display_credit_card").append(`<div class='row'><div class='col'><i class=\"far fa-credit-card\"></i></div><div class='col-2'><p>${id}</p></div><div class='col'><p>${info}</p></div></div>`);
                break;
            case "paypal":
                info = payment.info.email;
                $("#display_paypal").append(`<div class='row'><div class='col'><i class="fab fa-cc-paypal"></i></div><div class='col-2'><p>${id}</p></div><div class='col'><p>${info}</p></div></div>`);
                break;
            default:
                console.log(payment.type)
        }
    };

    // ****************************************
    // Create a the payment
    // ****************************************

    // create a new payment.
    $("#submit").click(function () {
        // don't refresh the page.
        event.preventDefault();
        // each time we click the button we reset the message.
        hideMessage();
        // in case any field is empty, if so it will throw an error. The error will be caught by the catch block.
        try {
            let available = false;
            if ($("#available").val() == "Yes")
                available = true;
            let type = "paypal";
            if ($("#type").val() == "Credit Card")
                type = "credit card";
            let info = {}
            if (type == "credit card") {
                let credit_card_number = $("#credit_card_number").val();
                let card_holder_name = $("#card_holder_name").val();
                let expiration_month = parseInt($("#expiration_month").val());
                let expiration_year = parseInt($("#expiration_year").val());
                let security_code = $("#security_code").val();
                info = {
                    credit_card_number: credit_card_number,
                    card_holder_name: card_holder_name,
                    expiration_month: expiration_month,
                    expiration_year: expiration_year,
                    security_code: security_code
                }
            } else {
                let email = $("#email").val();
                let phone_number = $("#phone_number").val();
                let token = $("#token").val();
                info = {
                    email: email,
                    phone_number: phone_number,
                    token: token
                }
            }
            let data = {
                customer_id: parseInt($("#customer_id").val()),
                order_id: parseInt($("#order_id").val()),
                available: available,
                type: type,
                info: info
            };
            // send the data to database.
            var ajax = $.ajax({
                type: "POST",
                url: "/payments",
                contentType: "application/json",
                data: JSON.stringify(data),
            });
            
            // if the ajax request is succeed, add to the table and reset the form.
            ajax.done(function(res){
                $("#payment_id").text(res.id);
                $("#payment_type").text(res.type);
                $("#payment_available").text(res.available);
                addRow(res);
                clearForm();
                showSuccess("create a new payment!");
            });
            
            // if the ajax request is failed, show the error.
            ajax.fail(function (res) {
                showError(res.responseJSON);
            });
        }catch (err) {
            showError(err);
        }
    });

    // Different forms will be shown base on the type of the payment.
    type.addEventListener('change', () => {
        let index = type.selectedIndex;
        switch (index) {
            case 1:
                credit_card.style.display = 'block';
                paypal.style.display = 'none';
                break;
            case 2:
                credit_card.style.display = 'none';
                paypal.style.display = 'block';
                break;
            default:
                credit_card.style.display = 'none';
                paypal.style.display = 'none';
        }
    });

    // Clear the create form.
    function clearForm(){
        $("#customer_id").val("");
        $("#order_id").val("");
        $("#available").val("")
        let type = "paypal";
        if ($("#type").val() == "Credit Card")
            type = "credit card";
        $("#type").val("");
        if (type == "credit card") {
            $("#credit_card_number").val("");
            $("#card_holder_name").val("");
            $("#expiration_month").val("");
            $("#expiration_year").val("");
            $("#security_code").val("");
        } else {
            $("#email").val("");
            $("#phone_number").val("");
            $("#token").val("");
        }
        credit_card.style.display = 'none';
        paypal.style.display = 'none';
    }
});

