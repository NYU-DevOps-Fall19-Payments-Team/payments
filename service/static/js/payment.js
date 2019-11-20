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
    function flash_message(message){
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
        switch (type){
            case "credit card":
                let credit_card_number = payment.info.credit_card_number;
                let card_holder_name = payment.info.card_holder_name;
                let expiration = payment.info.expiration_month + "/" + payment.info.expiration_year;
                $("#display_credit_card").append(`<div class='row'><div class='col-2'><i class=\"far fa-credit-card\"></i></div><div class='col-1'><p>${id}</p></div><div class='col-3'><p>${card_holder_name}</p></div><div class='col-3'><p>${credit_card_number}</p></div><div class='col-3'><p>${expiration}</p></div></div>`);
                break;
            case "paypal":
                let email = payment.info.email;
                let phone_number = payment.info.phone_number;
                $("#display_paypal").append(`<div class='row'><div class='col-2'><i class="fab fa-cc-paypal"></i></div><div class='col-1'><p>${id}</p></div><div class='col-3'><p>${email}</p></div><div class='col-3'><p>${phone_number}</p></div></div>`);
                break;
            default:
                console.log(payment.type)
        }
    };

    // ****************************************
    // Create a the payment
    // ****************************************
    
    $("#create_submit").click(function () {
        // don't refresh the page.
        event.preventDefault();
        // each time we click the button we reset the message.
        hideMessage();
        // in case any field is empty, if so it will throw an error. The error will be caught by the catch block.
        try {
            let available = false;
            if ($("#create_available").val() == "Yes")
                available = true;
            let type = "paypal";
            if ($("#create_type").val() == "Credit Card")
                type = "credit card";
            let info = {}
            if (type == "credit card") {
                let credit_card_number = $("#create_credit_card_number").val();
                let card_holder_name = $("#create_card_holder_name").val();
                let expiration_month = parseInt($("#create_expiration_month").val());
                let expiration_year = parseInt($("#create_expiration_year").val());
                let security_code = $("#create_security_code").val();
                info = {
                    credit_card_number: credit_card_number,
                    card_holder_name: card_holder_name,
                    expiration_month: expiration_month,
                    expiration_year: expiration_year,
                    security_code: security_code
                }
            } else {
                let email = $("#create_email").val();
                let phone_number = $("#create_phone_number").val();
                let token = $("#create_token").val();
                info = {
                    email: email,
                    phone_number: phone_number,
                    token: token
                }
            }
            let data = {
                customer_id: parseInt($("#create_customer_id").val()),
                order_id: parseInt($("#create_order_id").val()),
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
                $("#create_payment_id").text(res.id);
                $("#create_payment_type").text(res.type);
                $("#create_payment_available").text(res.available);
                addRow(res);
                clearCreateForm();
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
    $("#create_type").change(() =>{
        let type = $("#create_type").val();
        switch (type) {
            case "Credit Card":
                $("#credit_card").css("display","block");
                $("#paypal").css("display","none");
                break;
            case "PayPal":
                $("#credit_card").css("display","none");
                $("#paypal").css("display","block");
                break;
            default:
                $("#credit_card").css("display","none");
                $("#paypal").css("display","none");
        }
    })

    // Clear the create form.
    function clearCreateForm(){
        $("#create_customer_id").val("");
        $("#create_order_id").val("");
        $("#create_available").val("")
        let type = "paypal";
        if ($("#create_type").val() == "Credit Card")
            type = "credit card";
        $("#create_type").val("");
        if (type == "credit card") {
            $("#create_credit_card_number").val("");
            $("#create_card_holder_name").val("");
            $("#create_expiration_month").val("");
            $("#create_expiration_year").val("");
            $("#create_security_code").val("");
        } else {
            $("#create_email").val("");
            $("#create_phone_number").val("");
            $("#create_token").val("");
        }
        credit_card.style.display = 'none';
        paypal.style.display = 'none';
    }

    // ****************************************
    // Delete a Payment
    // ****************************************

    $("#delete-btn").click(function () {
      event.preventDefault();
        var payment_id = $("#delete_payment_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/payments/" + payment_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            $("#delete_payment_id").val("")
            flash_message("Payment has been Deleted!")
        });

        // ajax.fail(function(res){
        //     flash_message("Server error!")
        // });
        ajax.fail(function (res) {
            showError(res.responseJSON);
        });
    });

    // ****************************************
    // Update a Pet
    // ****************************************

    $("#update-btn").click(function () {
        event.preventDefault();
        var payment_id = $("#payment_id_update").val();
        try {
            let available = false;
            if ($("#available_update").val() == "Yes")
                available = true;
            let type = "paypal";
            if ($("#type_update").val() == "Credit Card")
                type = "credit card";
            let info = {}
            if (type == "credit card") {
                let credit_card_number = $("#credit_card_number_update").val();
                let card_holder_name = $("#card_holder_name_update").val();
                let expiration_month = parseInt($("#expiration_month_update").val());
                let expiration_year = parseInt($("#expiration_year_update").val());
                let security_code = $("#security_code_update").val();
                info = {
                    credit_card_number: credit_card_number,
                    card_holder_name: card_holder_name,
                    expiration_month: expiration_month,
                    expiration_year: expiration_year,
                    security_code: security_code
                }
            } else {
                let email = $("#email_update").val();
                let phone_number = $("#phone_number_update").val();
                let token = $("#token_update").val();
                info = {
                    email: email,
                    phone_number: phone_number,
                    token: token
                }
            }
            let data = {
                customer_id: parseInt($("#customer_id_update").val()),
                order_id: parseInt($("#order_id_update").val()),
                available: available,
                type: type,
                info: info
            };
            var ajax = $.ajax({
                type: "PUT",
                url: "/payments/" + payment_id,
                contentType: "application/json",
                data: JSON.stringify(data),
            });
            console.log(payment_id);

            ajax.done(function(res){
                $("#payment_id_update").val("")
                $("#customer_id_update").val("")
                $("#order_id_update").val("")
                $("#available_update").val("") // TODO: not the correct emptying
                $("#type_update").val("")
                $("#credit_card_number_update").val("")
                $("#card_holder_name_update").val("")
                $("#expiration_month_update").val("")
                $("#expiration_year_update").val("")
                $("#security_code_update").val("")
                $("#email_update").val("")
                $("#phone_number_update").val("")
                $("#token_update").val("")
                flash_message("Payment has been Updated!")
            });

            ajax.fail(function (res) {
                showError(res.responseJSON);
            });
        } catch (err) {
            showError(err);
        }
    });
});


