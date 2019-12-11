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
    function flash_message(message) {
        let successMessage = $(".success");
        successMessage.css("display", "block");
        successMessage.text(message);
    }

    // Hide all the message.
    function hideMessage() {
        let successMessage = $(".success");
        successMessage.css("display", "none");
        let errorMessage = $(".error");
        errorMessage.css("display", "none");
    }

    // for create and update route, construct the data.
    function constructData(type, available, route) {
        let info;
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
    function clearForm(type) {
        $(`#${type}_customer_id`).val("");
        $(`#${type}_order_id`).val("");
        $(`#${type}_available`).val("");
        let this_type = ($(`#${type}_type`).val() == "Credit Card") ? "credit card" : "paypal";
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
        $(`#${type}_credit_card`).css("display", "none");
        $(`#${type}_paypal`).css("display", "none");
    }


    // ****************************************
    // List all the payments.
    // ****************************************

    // load all the payments from the database, insert it into table.
    $("#list_all-btn").click((event) => {
        event.preventDefault();
        cleanDisplayCard();
        let ajax = $.ajax({
            type: "GET",
            url: "/payments"
        });

        ajax.done(function (res) {
            for (let i = 0; i < res.length; i++) {
                addRow(res[i]);
            }
            flash_message("List all successful! (" + res.length + " result" +
                (res.length === 1 ? "" : "s") + ")");
        });
    });

    function cleanDisplayCard() {
        $("#result-table-body").empty();
    }

    function addRow(payment) {
        let type = payment.type;
        console.log(payment);
        let id = `<td class =\"\" style=\"display: table-cell;\">${payment.id}</td>`;
        let order_id = `<td style=\"display: table-cell;\" class =\"order_id\">${payment.order_id}</td>`;
        let customer_id = `<td style=\"display: table-cell;\" class =\"customer_id\">${payment.customer_id}</td>`;
        let available = `<td style=\"display: table-cell;\" class=\"available\" ><span class=\"footable-toggle fooicon last-column fooicon-plus\"></span>${payment.available}</td>`;
        switch (type) {
            case "credit card":
                let credit_card_icon = `<td style=\"display: table-cell;\"><i class=\"far fa-credit-card\"></i></td>`;
                let credit_card_number = `<td style=\"display: table-cell;\" class=\"credit_card_number\">${payment.info.credit_card_number}</td>`;
                let card_holder_name = `<td style=\"display: table-cell;\" class =\"card_holder_name\">${payment.info.card_holder_name}</td>`;
                let expiration = `<td style=\"display: table-cell;\" class =\"expiration\">${payment.info.expiration_month + "/" + payment.info.expiration_year}</td>`;
                let credit_new_row = `<tr id='result-table-payment-row-${payment.id}' class='result-table-payment-row'>` +
                    id + customer_id + order_id + credit_card_icon + available +
                    `</tr><tr id='result-table-detail-table-row-${payment.id}' class='result-table-detail-table-row' style='display: none;'><td colspan="5"><table class='table table-bordered detail-table'><tbody>` +
                    `<tr><th>Credit Card Number</th>${credit_card_number}</tr>` +
                    `<tr><th>Card Holder Name</th>${card_holder_name}</tr>` +
                    `<tr><th>Expires</th>${expiration}</tr>` +
                    `</tbody></table></td></tr>`;
                $("#result-table-body").append(credit_new_row);
                break;

            case "paypal":
                let paypal_icon = `<td style=\"display: table-cell;\"><i class="fab fa-cc-paypal"></i></td>`;
                let email = `<td style=\"display: table-cell;\" class=\"email\">${payment.info.email}</td>`;
                let phone_number = `<td style=\"display: table-cell;\" class =\"phone_number\">${payment.info.phone_number}</td>`;
                let paypal_new_row = `<tr id='result-table-payment-row-${payment.id}' class='result-table-payment-row'>` +
                    id + customer_id + order_id + paypal_icon + available +
                    `</tr><tr id='result-table-detail-table-row-${payment.id}' class='result-table-detail-table-row' style='display: none;'><td colspan="5"><table class='table table-bordered detail-table'><tbody>` +
                    `<tr><th>Email</th>${email}</tr>` +
                    `<tr><th>Phone Number</th>${phone_number}</tr>` +
                    `</tbody></table></td></tr>`;
                $("#result-table-body").append(paypal_new_row);
                break;
            default:
                showError(`invaild payment type: ${payment.type}`);
        }
    }

    $("#result-table-body").on("click", ".result-table-payment-row", function () {
        let click_row_id = $(this)[0].id;
        // console.log("click_row_id = " + click_row_id);
        let toggle_row_id = "result-table-detail-table-row-" + click_row_id.slice(click_row_id.length - 1);
        // console.log("toggle_row_id = " + toggle_row_id);
        $("#" + toggle_row_id).toggle();
        // toggle fooicon + and -
        let fooicon = $(this).children(".available").children("span");
        if (fooicon.hasClass("fooicon-plus")) {
            fooicon.removeClass("fooicon-plus").addClass("fooicon-minus");
        } else {
            fooicon.removeClass("fooicon-minus").addClass("fooicon-plus");
        }
    });

    $("#expand-all-btn").click(function () {
        $(".result-table-detail-table-row").each(function () {
            $(this).show();
        });
        $(".fooicon").each(function () {
            $(this).removeClass("fooicon-plus").addClass("fooicon-minus");
        });
    });

    $("#collapse-all-btn").click(function () {
        $(".result-table-detail-table-row").each(function () {
            $(this).hide();
        });
        $(".fooicon").each(function () {
            $(this).removeClass("fooicon-minus").addClass("fooicon-plus");
        });
    });

    $(".form-title").click(function(){
        $(this).parent().children("form").toggle();
        $(this).find("svg").each(function () {
            $(this).toggle();
        });
    });

    // ****************************************
    // Create a payment.
    // ****************************************

    $("#create-btn").click(function () {
        // don't refresh the page.
        event.preventDefault();
        // each time we click the button we reset the message.
        hideMessage();
        // in case any field is empty, if so it will throw an error. The error will be caught by the catch block.
        try {
            let available = ($("#create_available").val() == "Yes") ? true : false;
            let type = ($("#create_type").val() == "Credit Card") ? "credit card" : "paypal";
            let data = constructData(type, available, "create");
            // send the data to database.
            var ajax = $.ajax({
                type: "POST",
                url: "/payments",
                contentType: "application/json",
                data: JSON.stringify(data),
            });

            // if the ajax request is succeed, add to the table and reset the form.
            ajax.done(function (res) {
                $("#create_payment_id").text(res.id);
                $("#create_payment_type").text(res.type);
                $("#create_payment_available").text(res.available);
                addRow(res);
                clearForm("create");
                flash_message("Create a new payment successful!");
            });

            // if the ajax request is failed, show the error.
            ajax.fail(function (res) {
                showError(res.responseJSON);
            });
        } catch (err) {
            showError(err);
        }
    });

    // Different forms will be shown base on the type of the payment.
    $("#create_type").change(() => {
        let type = $("#create_type").val();
        switch (type) {
            case "Credit Card":
                $("#create_credit_card").css("display", "block");
                $("#create_paypal").css("display", "none");
                break;
            case "PayPal":
                $("#create_credit_card").css("display", "none");
                $("#create_paypal").css("display", "block");
                break;
            default:
                $("#create_credit_card").css("display", "none");
                $("#create_paypal").css("display", "none");
        }
    });


    // ****************************************
    // Delete a Payment.
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
        });
        ajax.done(function (res) {
            $("#delete_payment_id").val("");
            flash_message("Payment " + payment_id + " has been deleted!")
        });
        ajax.fail(function (res) {
            showError(res.responseJSON);
        });
    });

    // ****************************************
    // Update a Payment.
    // ****************************************

    $("#update-btn").click(function () {
        event.preventDefault();
        var payment_id = $("#update_payment_id").val();
        try {
            let available = ($("#update_available").val() == "Yes") ? true : false;
            let type = ($("#update_type").val() == "Credit Card") ? "credit card" : "paypal";
            let data = constructData(type, available, "update");
            var ajax = $.ajax({
                type: "PUT",
                url: "/payments/" + payment_id,
                contentType: "application/json",
                data: JSON.stringify(data),
            });

            ajax.done(function (res) {
                clearForm("update");
                flash_message("Payment " + payment_id + " has been updated!")
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
                $("#update_credit_card").css("display", "block");
                $("#update_paypal").css("display", "none");
                break;
            case "PayPal":
                $("#update_credit_card").css("display", "none");
                $("#update_paypal").css("display", "block");
                break;
            default:
                $("#update_credit_card").css("display", "none");
                $("#update_paypal").css("display", "none")
        }
    });

    // ****************************************
    // Toggle a Payment.
    // ****************************************

    $("#toggle-btn").click(function () {
        event.preventDefault();
        var payment_id = $("#toggle_payment_id").val();

        var ajax = $.ajax({
            type: "PATCH",
            url: "/payments/" + payment_id + "/toggle",
            contentType: "application/json",
            data: '',
        });
        console.log(payment_id);

        ajax.done(function (res) {
            flash_message("Payment " + payment_id + " availability has been toggled!")
        });

        ajax.fail(function (res) {
            showError(res.responseJSON);
        });
    });

    // ****************************************
    // Query payments.
    // ****************************************

    $("#query-btn").click(function () {
        event.preventDefault();
        cleanDisplayCard();
        var payment_id = $("#query_payment_id").val();
        try {
            let customer_id_string = $("#query_customer_id").val();
            let order_id_string = $("#query_order_id").val();
            let available_string = $("#query_available").val();
            let type_string = $("#query_type").val().toLowerCase();

            let query_string_list = [];
            if (customer_id_string)
                query_string_list.push("customer_id=" + customer_id_string);
            if (order_id_string)
                query_string_list.push("order_id=" + order_id_string);
            if (available_string)
                query_string_list.push("available=" + available_string);
            if (type_string)
                query_string_list.push("type=" + type_string);
            let query_string = query_string_list.join("&");
            let query_url = "/payments";
            query_url += query_string ? "?" + query_string : "";

            var ajax = $.ajax({
                type: "GET",
                url: query_url
            });

            ajax.done(function (res) {
                for (let i = 0; i < res.length; i++)
                    addRow(res[i]);
                flash_message("Query successful! (" + res.length + " result" +
                    (res.length === 1 ? "" : "s") + ")");
            });

            ajax.fail(function (res) {
                showError(res.responseJSON);
            });
        } catch (err) {
            showError(err);
        }
    });

    // ****************************************
    // Read a payment.
    // ****************************************

    $("#read-btn").click(function () {
        event.preventDefault();
        cleanDisplayCard();
        const payment_id = $("#read_payment_id").val();
        try {
            var ajax = $.ajax({
                type: "GET",
                url: "/payments/" + payment_id
            });

            ajax.done(function (res) {
                addRow(res);
                flash_message("Read successful!");
            });

            ajax.fail(function (res) {
                showError(res.responseJSON);
            });
        } catch (err) {
            showError(err);
        }
    });
});
