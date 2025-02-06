document.addEventListener('DOMContentLoaded', async () =>{
        //Fetch publishable key and initialize stripe
        const {publishableKey} = await fetch("/config").then(r => r.json())
        const stripe = Stripe(String(publishableKey))
        //Fetch client secret and initialize elements
        const params = new URLSearchParams(window.location.href)
        const clientSecret = params.get("payment_intent_client_secret")
        const {paymentIntent} = await stripe.retrievePaymentIntent(clientSecret)
        const paymentIntentPre = document.getElementById("payment-intent")
        paymentIntentPre.innerText = JSON.stringify(paymentIntent, null, 2)
        window.flaskUrls = { pago: "{{url_for('tienda.get_items')}}"};
        await fetch(flaskUrls.pago)        
})

