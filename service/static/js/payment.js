$(function (){
    $("#submit").click(function (){
        event.preventDefault();
        try{
            let available = false;
            if($("#available").val() == "Yes")
                available = true;
            let type = "paypal";
            if($("#type").val() == "Credit Card")
                type = "credit card";
            let info = {}
            if(type == "credit card"){
                let credit_card_number = $("#credit_card_number").val();
                let card_holder_name = $("#card_holder_name").val();
                let expiration_month = parseInt($("#expiration_month").val());
                let expiration_year = parseInt($("#expiration_year").val());
                let security_code = $("#security_code").val();
                info ={
                    credit_card_number:credit_card_number,
                    card_holder_name:card_holder_name,
                    expiration_month:expiration_month,
                    expiration_year:expiration_year,
                    security_code:security_code
                }
            }else{
                let email = $("#email").val();
                let phone_number = $("#phone_number").val();
                let token = $("#token").val();
                info = {
                    email:email,
                    phone_number:phone_number,
                    token:token
                }
            }
            let data = {
                customer_id:parseInt($("#customer_id").val()),
                order_id:parseInt($("#order_id").val()),
                available:available,
                type:type,
                info:info
            }
            var ajax = $.ajax({
                type:"POST",
                url: "/payments",
                contentType: "application/json",
                data: JSON.stringify(data),
            })

            ajax.done(function(res){
                $("#payment_id").text(res.id);
                $("#payment_type").text(res.type);
                $("#payment_available").text(res.available);
            });
    
            ajax.fail(function(res){
                showError(res.responseJSON);
            });
        }catch(err){
            showError(err);
        }
    })

    type.addEventListener('change',()=>{
        let index = type.selectedIndex;
        switch(index){
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
    })
    
    function showError(error){
        let errorMessage = $(".error");
        errorMessage.css("display","block");
        errorMessage.text(error.message);
    }
})

