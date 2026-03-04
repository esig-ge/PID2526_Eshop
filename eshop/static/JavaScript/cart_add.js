function createAddToCartForm(productId) {
    const form = document.createElement("form");
    form.method = "POST";
    form.action = `/cart/add/${productId}/`; // Ton URL Django
    form.className = "m-0";

    // CSRF token
    const csrfInput = document.createElement("input");
    csrfInput.type = "hidden";
    csrfInput.name = "csrfmiddlewaretoken";
    csrfInput.value = document.querySelector('[name=csrfmiddlewaretoken]').value; // récupère le token existant
    form.appendChild(csrfInput);

    // Bouton
    const button = document.createElement("button");
    button.type = "submit";
    button.className = "btn btn-primary btn-sm";
    button.innerHTML = '<i class="fa fa-cart-plus"></i> Panier';
    form.appendChild(button);

    return form;
}