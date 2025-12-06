function setupAutocomplete(inputId, hiddenId, badgeContainerId) {
    const input = document.getElementById(inputId);
    const hidden = document.getElementById(hiddenId);
    const badgeContainer = document.getElementById(badgeContainerId);

    let selected = [];

    input.addEventListener("input", async function () {
        const query = input.value.trim();
        if (query.length < 2) return;

        const response = await fetch(`/project/buscar-usuarios?q=${query}`);
        const users = await response.json();

        let box = document.getElementById(inputId + "-box");
        if (!box) {
            box = document.createElement("div");
            box.id = inputId + "-box";
            box.className = "autocomplete-box";
            input.parentNode.appendChild(box);
        }

        box.innerHTML = "";

        users.forEach(u => {
            const item = document.createElement("div");
            item.className = "autocomplete-item";
            item.innerText = `${u.nome} (${u.email})`;

            item.onclick = () => {
                // Evita duplicado
                if (!selected.some(x => x.id === u.id)) {
                    selected.push({
                        id: u.id,
                        nome: u.nome,
                        email: u.email
                    });
                    renderBadges();
                }

                input.value = "";
                box.innerHTML = "";
            };

            box.appendChild(item);
        });
    });

    function renderBadges() {
        badgeContainer.innerHTML = "";

        selected.forEach(item => {
            const badge = document.createElement("span");
            badge.className = "badge-user";
            badge.innerHTML = `${item.nome} <button class="remove-btn">x</button>`;

            badge.querySelector("button").onclick = () => {
                selected = selected.filter(x => x.id !== item.id);
                renderBadges();
            };

            badgeContainer.appendChild(badge);
        });

        // ENVIA APENAS OS IDs PARA O BACKEND
        hidden.value = selected.map(x => x.id).join(",");
    }
}
