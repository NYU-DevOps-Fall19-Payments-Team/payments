$(function () {
  // ****************************************
  //  U T I L I T Y   F U N C T I O N S
  // ****************************************

  // Updates the form with data from the response
  function update_form_data(res) {
    $("#pet_id").val(res._id);
    $("#pet_name").val(res.name);
    $("#pet_category").val(res.category);
    if (res.available == true) {
        $("#pet_available").val("true");
      } else {
        $("#pet_available").val("false");
      }
    }

    /// Clears all form fields
    function clear_form_data() {
      $("#pet_name").val("");
      $("#pet_category").val("");
      $("#pet_available").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
      $("#flash_message").empty();
      $("#flash_message").append(message);
    }

    $("#submit").click(function () {
        event.preventDefault();
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
            var ajax = $.ajax({
                type: "POST",
                url: "/payments",
                contentType: "application/json",
                data: JSON.stringify(data),
            });

            ajax.done(function(res){
                $("#payment_id").text(res.id);
                $("#payment_type").text(res.type);
                $("#payment_available").text(res.available);
            });

            ajax.fail(function (res) {
                showError(res.responseJSON);
            });
        } catch (err) {
            showError(err);
        }
    });

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
    // function clear_delete_form(){
    //   $("#customer_in_id").val("");
    //       credit_card.style.display = 'none';
    //       paypal.style.display = 'none';
    //     }
    //   });

    function showError(error) {
        let errorMessage = $(".error");
        errorMessage.css("display", "block");
        errorMessage.text(error.message);
    }

    // ****************************************
    // Delete a Payment
    // ****************************************

    $("#delete-btn").click(function () {
      event.preventDefault();
        var payment_id = $("#payment_in_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/payments/" + payment_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            $("#payment_in_id").val("")
            flash_message("Payment has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Update a Pet
    // ****************************************

    $("#update-btn").click(function () {

      var payment_id = $("#payment_id").val();
      var name = $("#pet_name").val();
      var category = $("#pet_category").val();
      var available = $("#pet_available").val() == "true";

      var data = {
          "name": name,
          "category": category,
          "available": available
        };

        var ajax = $.ajax({
              type: "PUT",
              url: "/pets/" + pet_id,
              contentType: "application/json",
              data: JSON.stringify(data)
            })

            ajax.done(function(res){
              update_form_data(res)
              flash_message("Success")
            });

            ajax.fail(function(res){
              flash_message(res.responseJSON.message)
            });

          });
});
