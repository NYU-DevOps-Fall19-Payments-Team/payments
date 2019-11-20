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

    // for create and update route, construct the data.
    function constructData(type, available,route){
        if (type == "credit card") {
            let credit_card_number = $(`#${route}_credit_card_number`).val();
            let card_holder_name = $(`#${route}_card_holder_name`).val();
            let expiration_month = parseInt($(`#${route}_expiration_month`).val());
            let expiration_year = parseInt($(`#${route}_expiration_year`).val());
            let security_code = $(`#${route}_security_code`).val();
            info = {
                credit_card_number: credit_card_number,
                card_holder_name: card_holder_name,
                expiration_month: expiration_month,
                expiration_year: expiration_year,
                security_code: security_code
            }
        } else {
            let email = $(`#${route}_email`).val();
            let phone_number = $(`#${route}_phone_number`).val();
            let token = $(`#${route}_token`).val();
            info = {
                email: email,
                phone_number: phone_number,
                token: token
            }
        }
        let data = {
            customer_id: parseInt($(`#${route}_customer_id`).val()),
            order_id: parseInt($(`#${route}_order_id`).val()),
            available: available,
            type: type,
            info: info
        };
        return data
    }

    // Clear the form.
    function clearForm(type){
        $(`#${type}_customer_id`).val("");
        $(`#${type}_order_id`).val("");
        $(`#${type}_available`).val("")
        let this_type = ($(`#${type}_type`).val() == "Credit Card")? "credit card" : "paypal";
        $(`#${type}_type`).val("");
        if (this_type == "credit card") {
            $(`#${type}_credit_card_number`).val("");
            $(`#${type}_card_holder_name`).val("");
            $(`#${type}_expiration_month`).val("");
            $(`#${type}_expiration_year`).val("");
            $(`#${type}_security_code`).val("");
        } else {
            $(`#${type}_email`).val("");
            $(`#${type}_phone_number`).val("");
            $(`#${type}_token`).val("");
        }
        $(`#${type}_credit_card`).css("display","none");
        $(`#${type}_paypal`).css("display","none");
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
            let available = ($("#create_available").val() == "Yes")? true : false;
            let type = ($("#create_type").val() == "Credit Card")? "credit card" : "paypal";
            let data = constructData(type,available,"create");
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
                clearForm("create");
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
                $("#create_credit_card").css("display","block");
                $("#create_paypal").css("display","none");
                break;
            case "PayPal":
                $("#create_credit_card").css("display","none");
                $("#create_paypal").css("display","block");
                break;
            default:
                $("#create_credit_card").css("display","none");
                $("#create_paypal").css("display","none");
        }
    })

    
    // ****************************************
    // Delete a Payment
    // ****************************************

    $("#delete-btn").click(function () {
        event.preventDefault();
        hideMessage();
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
        ajax.fail(function (res) {
            showError(res.responseJSON);
        });
    });

    // ****************************************
    // Update a Payments
    // ****************************************

    $("#update-btn").click(function () {
        event.preventDefault();
        var payment_id = $("#update_payment_id").val();
        try {
            let available = ($("#update_available").val() == "Yes")? true : false;
            let type = ($("#update_type").val() == "Credit Card")? "credit card":"paypal";
            let data = constructData(type,available,"update");
            var ajax = $.ajax({
                type: "PUT",
                url: "/payments/" + payment_id,
                contentType: "application/json",
                data: JSON.stringify(data),
            });

            ajax.done(function(res){
                clearForm("update");
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

    // ****************************************
    // Query payments
    // ****************************************

    $("#query-btn").click(function () {
        event.preventDefault();
        var payment_id = $("#query_payment_id").val();
        try {
            let customer_id = parseInt($("#update_customer_id").val());
            let order_id = parseInt($("#update_order_id").val());
            let available = $("#query_available").val() == "Yes";
            let type = "";
            switch ($("#query_type").val()) {
                case "Credit Card":
                    type = "credit card";
                case "Paypal":
                    type = "paypal";

            }
            if ($("#query_type").val() == "Credit Card")
                type = "credit card";

            var ajax = $.ajax({
                type: "GET",
                url: "/payments?customer_id=" + customer_id + "&order_id=" +
                    order_id + "&available=" + available + "&type=" + type
            });
            // console.log(payment_id);

            ajax.done(function (res) {
                // $("#query_customer_id").text(customer_id);
                // $("#query_order_id").text(order_id);
                // $("#query_available").text(available ? "Yes" : "No");
                for (i = 0; i < res.length; i++)
                    addRow(res[i])
                flash_message("Query succesful!");
            });

            ajax.fail(function (res) {
                showError(res.responseJSON);
            });
        } catch (err) {
            showError(err);
        }
    });
});
