//Osman Huseynov


// 1️⃣ AI search function
async function searchAI() {

    const query = document.getElementById("searchInput-ai").value;
    const resultsContainer = document.getElementById("ai_choice");

    // clear previous results
    resultsContainer.innerHTML = "";

    // if the query is too short, do nothing
    if (query.length < 2) return;

    // show loading spinner
    const loader = document.createElement("div");
    loader.style.textAlign = "center";
    loader.style.padding = "12px";
    loader.innerHTML = `
        <div style="
            width:24px;
            height:24px;
            border:3px solid #ddd;
            border-top:3px solid #3498db;
            border-radius:50%;
            animation: spin 0.8s linear infinite;
            margin:auto;
        "></div>
    `;
    resultsContainer.appendChild(loader);

    // inject animation once
    if (!document.getElementById("aiLoaderStyle")) {
        const style = document.createElement("style");
        style.id = "aiLoaderStyle";
        style.innerHTML = `
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }

    try {
        const response = await fetch(`/ai_search?q=${encodeURIComponent(query)}`);

        if (!response.ok) {
            throw new Error(`HTTP Error ${response.status}`);
        }

        const data = await response.json();
        // remove loader
        loader.remove();

        // check if results are in expected format
        if (!data.results || !Array.isArray(data.results) || data.results.length === 0) {
            resultsContainer.innerHTML = `<span style="color: #e74c3c;"">Pas de suggestion pour le moment...</span><p>Essayer d'utiliser d'autre mot clé.</p>`;
            return;
        }

        // simplify data results
        const suggestion = data.results;

        

        // ------------------------------------------------------
        // Process the JSON to display product name, price, and link nicely
        // ------------------------------------------------------
        for (const suggestedProduct of suggestion) {
            if (suggestedProduct.name) {
                // Create form for "Add to Cart" button
                const cart_add = createAddToCartForm(suggestedProduct.link);
                const col = document.createElement("div");
                col.className = "col-12 col-md-4";

                const card = document.createElement("div");
                card.className = "card h-100 shadow-sm";

                // Image
                if (suggestedProduct.img_url) {
                    const img = document.createElement("img");
                    img.src = "/media/" + suggestedProduct.img_url.trim(); // trim just in case
                    img.className = "card-img-top align-self-center";
                    img.style.objectFit = "cover";
                    img.style.height = "200px";
                    img.style.width = "200px";
                    img.alt = suggestedProduct.name;
                    card.appendChild(img);
                } else {
                    const placeholder = document.createElement("div");
                    placeholder.style.height = "200px";
                    placeholder.style.width = "200px";
                    placeholder.style.backgroundColor = "#f0f0f0";
                    placeholder.style.display = "flex";
                    placeholder.style.alignItems = "center";
                    placeholder.style.justifyContent = "center";
                    placeholder.className = "card-img-top align-self-center";
                    placeholder.textContent = "Pas d'image disponible.";
                    card.appendChild(placeholder);
                }

                const cardBody = document.createElement("div");
                cardBody.className = "card-body d-flex flex-column";

                const title = document.createElement("h5");
                title.className = "card-title";
                title.textContent = suggestedProduct.name;

                const price = document.createElement("p");
                price.className = "text-success fw-bold";
                price.textContent = suggestedProduct.price;

                const resume = document.createElement("p");
                resume.className = "card-text small text-muted";
                resume.textContent = suggestedProduct.resume;

                const link = document.createElement("a");
                link.href = "/get/" + suggestedProduct.link;
                link.target = "_blank";
                link.className = "btn btn-primary mt-auto";
                link.textContent = "Voir le produit";

                


                cardBody.appendChild(title);
                cardBody.appendChild(price);
                cardBody.appendChild(resume);
                cardBody.appendChild(link);
                cardBody.appendChild(cart_add);

                card.appendChild(cardBody);
                col.appendChild(card);

                resultsContainer.appendChild(col);
            }
        }

    } catch (err) {
        console.error("Error during AI search:", err);
        resultsContainer.innerHTML = '<span style="color: #e74c3c;">Erreur de connection a l´IA...</span>';
    }
}

// 2️⃣ Trigger via button click
document.getElementById("aiQueryButton").addEventListener("click", searchAI);

// 3️⃣ Trigger via Enter key in input
document.getElementById("searchInput-ai").addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        e.preventDefault(); // prevent default form submission
        searchAI();         // call the same function as the button
    }
});

// 4️⃣ Clear AI search
document.getElementById("clear-ai-search").addEventListener("click", function () {
    const input = document.getElementById("searchInput-ai");
    const results = document.getElementById("ai_choice");
    input.value = "";
    results.innerHTML = "";
});


function createAddToCartForm(productId) {
    const form = document.createElement("form");
    form.method = "POST";
    form.action = `/cart/add/${productId}/`;
    form.className = "m-0";

    // CSRF token
    const csrfInput = document.createElement("input");
    csrfInput.type = "hidden";
    csrfInput.name = "csrfmiddlewaretoken";
    csrfInput.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
    form.appendChild(csrfInput);

    const button = document.createElement("button");
    button.type = "submit";
    button.className = "btn btn-primary mt-2";
    button.innerHTML = '<i class="fa fa-cart-plus"></i> Panier';
    form.appendChild(button);

    // stop redirecting
    form.addEventListener("submit", async function(e) {
        e.preventDefault();

        const response = await fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfInput.value
            }
        });

        if (response.ok) {
            button.innerHTML = "✔ Ajouté";
            button.classList.remove("btn-primary");
            button.classList.add("btn btn-outline-light");
        }
    });

    return form;
}
