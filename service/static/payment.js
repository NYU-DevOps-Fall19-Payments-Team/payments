var credit_card = document.getElementById("credit_card")
var paypal = document.getElementById("paypal")
var type = document.getElementById("type")
var submit = document.getElementById("submit")
var errorMessage = document.getElementsByClassName("error")[0];

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

submit.addEventListener('click',(event)=>{
    event.preventDefault();
    errorMessage.style.display = 'none';
    try{
        let customer_id = parseInt(document.getElementById("customer_id").value);
        let order_id = parseInt(document.getElementById("order_id").value);
        let available = false;
        if(document.getElementById("available").value == "Yes")
            available = true;
        let type = "paypal";
        if(document.getElementById("type").value == "Credit Card")
            type = "credit card";
        let info = {}
        if(type == "credit card"){
            let credit_card_number = document.getElementById("credit_card_number").value;
            let card_holder_name = document.getElementById("card_holder_name").value;
            let expiration_month = parseInt(document.getElementById("expiration_month").value);
            let expiration_year = parseInt(document.getElementById("expiration_year").value);
            let security_code = document.getElementById("security_code").value;
            info ={
                credit_card_number:credit_card_number,
                card_holder_name:card_holder_name,
                expiration_month:expiration_month,
                expiration_year:expiration_year,
                security_code:security_code
            }
        }else{
            let email = document.getElementById("email").value;
            let phone_number = document.getElementById("phone_number").value;
            let token = document.getElementById("token").value;
            info = {
                email:email,
                phone_number:phone_number,
                token:token
            }
        }
        let data = {
            customer_id:customer_id,
            order_id:order_id,
            available:available,
            type:type,
            info:info
        }
        fetch("/payments", {
            method:'POST',
            headers: {
                'Content-Type': 'application/json'
              },
            body:JSON.stringify(data)})
            .then(handleErrors)
            .then((res)=>{
                console.log("redirecting...")
                window.location.href = "/payments";
            })
            .catch((err)=>{
                showError(err);
            })
    } catch(err){
        showError(err);
    }
})

function showError(error){
    errorMessage.style.display = 'block';
    errorMessage.innerHTML = error.message;
}

async function handleErrors(response){
    if(!response.ok){
        let error = await response.json();
        throw Error(error.message);
    }
    return response;
}