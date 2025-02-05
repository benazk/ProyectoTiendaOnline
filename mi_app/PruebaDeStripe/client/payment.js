// Esta funcion es para mostrar la ventana del pago después de haber llamado a la funcion que retrieve-a el clientSecret
document.addEventListener('DOMContentLoaded', async () =>{
    //Fetch publishable key and initialize stripe
    const {publishableKey} = await fetch("/config").then(r => r.json())
    const stripe = Stripe(String(publishableKey))
    //Fetch client secret and initialize elements
    const {clientSecret} = await fetch("/create-payment-intent", {
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        }
    }).then(r => r.json())
    const elements = stripe.elements({clientSecret})
    const paymentElement = elements.create('payment')
    paymentElement.mount("#payment-element")

    const form = document.getElementById("payment-form")
    form.addEventListener("submit", async (e) =>{
        e.preventDefault()

        const {error} = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: window.location.href.split("?")[0] + "complete.html"
            }
        })
        if(error){
            const messages = document.getElementById("error-messages")
            messages.innerText - error.message
        }
    })
})