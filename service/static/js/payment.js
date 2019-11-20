$(function () {
    // ****************************************
    // UTILITY FUNCTIONS
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
    $("#list_all-btn").click(()=>{
        event.preventDefault();
        cleanDisplayCard()
        var ajax = $.ajax({
            type: "GET",
            url: "/payments",
            contentType: "application/json"
        });
    
        ajax.done(function(res){
            for(i = 0; i < res.length; i++)
                addRow(res[i])
        });
    })

    function cleanDisplayCard(){
        $(".display_payments").remove();
    }

    function addRow(payment){
        let type = payment.type;
        console.log(payment)
        let id = `<div class ='col-1'>${payment.id}</div>`;
        let customer_id = `<div class ='col-2'>${payment.customer_id}</div>`;
        let order_id = `<div class ='col-1'>${payment.order_id}</div>`;
        let available = `<div class ='col-1'>${payment.available}</div>`;
        switch (type){
            case "credit card":
                let credit_card_icon = "<div class='col-1'><i class=\"far fa-credit-card\"></i></div>";
                let credit_card_number = `<div class ='col-2'>${payment.info.credit_card_number}</div>`;
                let card_holder_name = `<div class ='col-2'>${payment.info.card_holder_name}</div>`;
                let expiration = `<div class ='col-2'>${payment.info.expiration_month + "/" + payment.info.expiration_year}</div>`;
                let credit_new_row = id + customer_id + order_id + available + credit_card_icon + card_holder_name + credit_card_number + expiration; 
                $("#display_credit_card").append(`<div class='row display_payments'>${credit_new_row}</div>`);
                break;
            case "paypal":
                let paypal_icon = "<div class='col-1'><i class=\"fab fa-cc-paypal\"></i></div>";
                let email = `<div class ='col-3'>${payment.info.email}</div>`;
                let phone_number = `<div class ='col-2'>${payment.info.phone_number}</div>`;
                let paypal_new_row = id + customer_id + order_id + available + paypal_icon + email + phone_number;
                $("#display_paypal").append(`<div class='row display_payments'>${paypal_new_row}</div>`);
                break;
            default:
                showError(`invaild payment type: ${payment.type}`);
        }
    };

    // ****************************************
    // Create a the payment
    // ****************************************

    $("#create-btn").click(function () {
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
                flash_message("create a new payment!");
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
        var payment_id = $("#update_payment_id").val();
        try {
            let available = false;
            if ($("#update_available").val() == "Yes")
                available = true;
            let type = "paypal";
            if ($("#update_type").val() == "Credit Card")
                type = "credit card";
            let info = {}
            if (type == "credit card") {
                let credit_card_number = $("#update_credit_card_number").val();
                let card_holder_name = $("#update_card_holder_name").val();
                let expiration_month = parseInt($("#update_expiration_month").val());
                let expiration_year = parseInt($("#update_expiration_year").val());
                let security_code = $("#update_security_code").val();
                info = {
                    credit_card_number: credit_card_number,
                    card_holder_name: card_holder_name,
                    expiration_month: expiration_month,
                    expiration_year: expiration_year,
                    security_code: security_code
                }
            } else {
                let email = $("#update_email").val();
                let phone_number = $("#update_phone_number").val();
                let token = $("#update_token").val();
                info = {
                    email: email,
                    phone_number: phone_number,
                    token: token
                }
            }
            let data = {
                customer_id: parseInt($("#update_customer_id").val()),
                order_id: parseInt($("#update_order_id").val()),
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
                $("#update_payment_id").val("")
                $("#update_customer_id").val("")
                $("#update_order_id").val("")
                $("#update_available").val("")
                $("#update_type").val("")
                $("#update_credit_card_number").val("")
                $("#update_card_holder_name").val("")
                $("#update_expiration_month").val("")
                $("#update_expiration_year").val("")
                $("#update_security_code").val("")
                $("#update_email").val("")
                $("#update_phone_number").val("")
                $("#update_token").val("")
                flash_message("Payment has been Updated!")
            });

            ajax.fail(function (res) {
                showError(res.responseJSON);
            });
        } catch (err) {
            showError(err);
        }
    });

    $("#update_type").change(() => {
        let type = $("#update_type").val();
        switch (type) {
            case "Credit Card":
                $("#update_credit_card").css("display", "block")
                $("#update_paypal").css("display", "none")
                break;
            case "PayPal":
                $("#update_credit_card").css("display", "none")
                $("#update_paypal").css("display", "block")
                break;
            default:
                $("#update_credit_card").css("display", "none")
                $("#update_paypal").css("display", "none")
        }
    });
});
