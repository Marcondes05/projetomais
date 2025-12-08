// ===============================
// AUTOCOMPLETE.JS — POSICIONAMENTO FIXO + FUNCIONAMENTO PERFEITO
// ===============================
(function () {

    if (!window.App) window.App = {};

    function $(id) {
        return document.getElementById(id);
    }

    window.App.setupAutocomplete = function (inputId, hiddenId, badgesId, opts = {}) {

        const single = !!opts.single;

        const input = $(inputId);
        const hidden = $(hiddenId);
        const badges = $(badgesId);
        const box = $(opts.box);

        if (!input || !hidden || !badges || !box) {
            console.warn("⚠ Autocomplete ignorado:", { inputId, hiddenId, badgesId, boxId: opts.box });
            return;
        }

        // Agora o CSS controla o posicionamento dentro do wrapper
        box.style.display = "none";

        let items = [];
        let activeIndex = -1;
        let timer = null;

        // ===============================
        // FECHAR QUANDO CLICAR FORA
        // ===============================
        document.addEventListener("click", (ev) => {
            if (!box.contains(ev.target) && ev.target !== input) {
                box.style.display = "none";
            }
        });

        // ===============================
        // BUSCA
        // ===============================
        input.addEventListener("input", () => {
            clearTimeout(timer);

            const q = input.value.trim();
            if (!q) {
                box.style.display = "none";
                return;
            }

            timer = setTimeout(() => fetchUsers(q), 180);
        });

        function fetchUsers(q) {
            fetch(window.SEARCH_USERS_URL + "?q=" + encodeURIComponent(q))
                .then(r => r.json())
                .then(data => {
                    items = Array.isArray(data) ? data : [];
                    renderList();
                })
                .catch(err => console.error("Erro no autocomplete:", err));
        }

        // ===============================
        // RENDERIZAR LISTA
        // ===============================
        function renderList() {
            box.innerHTML = "";

            if (!items.length) {
                box.style.display = "none";
                return;
            }

            items.forEach((u, index) => {
                const row = document.createElement("div");
                row.className = "autocomplete-item";
                row.dataset.id = u.id;
                row.dataset.nome = u.nome;

                row.innerHTML = `<strong>${u.nome}</strong> — ${u.email}`;

                row.addEventListener("click", () => select(u));
                row.addEventListener("mouseenter", () => highlight(index));

                box.appendChild(row);
            });

            activeIndex = -1;
            box.style.display = "block";
        }

        function highlight(i) {
            [...box.children].forEach(c => c.classList.remove("active"));
            if (box.children[i]) box.children[i].classList.add("active");
            activeIndex = i;
        }

        // ===============================
        // NAVEGAÇÃO TECLADO
        // ===============================
        input.addEventListener("keydown", (ev) => {

            const rows = [...box.children];
            if (box.style.display === "none" || rows.length === 0) return;

            if (ev.key === "ArrowDown") {
                ev.preventDefault();
                highlight(Math.min(activeIndex + 1, rows.length - 1));
            }

            else if (ev.key === "ArrowUp") {
                ev.preventDefault();
                highlight(Math.max(activeIndex - 1, 0));
            }

            else if (ev.key === "Enter") {
                ev.preventDefault();
                if (activeIndex >= 0 && rows[activeIndex]) {
                    const r = rows[activeIndex];
                    select({ id: r.dataset.id, nome: r.dataset.nome });
                }
            }
        });

        // ===============================
        // SELECIONAR ITEM
        // ===============================
        function select(u) {
            if (single) {
                badges.innerHTML = "";
                hidden.value = u.id;
                addBadge(u);
            } else {
                const values = hidden.value ? hidden.value.split(",").filter(Boolean) : [];
                if (!values.includes(String(u.id))) {
                    values.push(String(u.id));
                    hidden.value = values.join(",");
                    addBadge(u);
                }
            }

            input.value = "";
            box.style.display = "none";
        }

        // ===============================
        // ADICIONAR BADGE
        // ===============================
        function addBadge(u) {
            const span = document.createElement("span");
            span.className = "badge-item";
            span.dataset.id = u.id;

            span.innerHTML = `${u.nome} <button type="button" class="badge-remove">x</button>`;

            const btn = span.querySelector(".badge-remove");
            btn.addEventListener("click", () => removeBadge(span));

            badges.appendChild(span);
        }

        // ===============================
        // REMOVER BADGE
        // ===============================
        function removeBadge(span) {
            const id = span.dataset.id;
            span.remove();

            if (single) {
                hidden.value = "";
            } else {
                const arr = hidden.value.split(",").filter(Boolean);
                hidden.value = arr.filter(x => x !== id).join(",");
            }
        }

        window.App.removeBadge = removeBadge;
    };

})();
// ===============================
// AUTOCOMPLETE ESPECIAL PARA FILTROS (SEM BADGES)
// ===============================
window.App.setupAutocompleteFiltro = function (inputId, hiddenId, boxId) {

    const input = document.getElementById(inputId);
    const hidden = document.getElementById(hiddenId);
    const box = document.getElementById(boxId);

    if (!input || !hidden || !box) {
        console.warn("Filtro autocomplete não iniciado:", { inputId, hiddenId, boxId });
        return;
    }

    box.style.display = "none";

    let items = [];
    let timer = null;

    // FECHAR AO CLICAR FORA
    document.addEventListener("click", (ev) => {
        if (!box.contains(ev.target) && ev.target !== input) {
            box.style.display = "none";
        }
    });

    // BUSCA
    input.addEventListener("input", () => {
        clearTimeout(timer);

        const q = input.value.trim();
        if (!q) return (box.style.display = "none");

        timer = setTimeout(() => {
            fetch(window.SEARCH_USERS_URL + "?q=" + encodeURIComponent(q))
                .then(r => r.json())
                .then(data => {
                    items = data;
                    render();
                });
        }, 150);
    });

    // RENDERIZAR RESULTADOS
    function render() {
        box.innerHTML = "";

        if (!items.length) {
            box.style.display = "none";
            return;
        }

        items.forEach(u => {
            const row = document.createElement("div");
            row.className = "autocomplete-item";
            row.innerHTML = `<strong>${u.nome}</strong> — ${u.email}`;

            row.addEventListener("click", () => selecionar(u));

            box.appendChild(row);
        });

        box.style.display = "block";
    }

    function selecionar(u) {
        input.value = u.nome;  // escreve o nome no input
        hidden.value = u.id;   // ID vai no GET
        box.style.display = "none";
    }
};

// ===============================
// AUTOCOMPLETE SIMPLES PARA FILTRO (SEM BADGES)
// ===============================
window.App.setupAutocompleteFiltro = function (inputId, hiddenId, boxId) {

    const input = document.getElementById(inputId);
    const hidden = document.getElementById(hiddenId);
    const box = document.getElementById(boxId);

    if (!input || !hidden || !box) {
        console.warn("Filtro ignorado:", { inputId, hiddenId, boxId });
        return;
    }

    let items = [];
    let timer = null;

    // Buscar
    input.addEventListener("input", () => {
        clearTimeout(timer);
        const q = input.value.trim();
        if (!q) return box.style.display = "none";

        timer = setTimeout(() => {
            fetch(window.SEARCH_USERS_URL + "?q=" + encodeURIComponent(q))
                .then(r => r.json())
                .then(data => {
                    items = data;
                    renderList();
                });
        }, 180);
    });

    function renderList() {
        box.innerHTML = "";
        if (!items.length) {
            box.style.display = "none";
            return;
        }

        items.forEach(u => {
            const row = document.createElement("div");
            row.className = "autocomplete-item";
            row.dataset.id = u.id;
            row.dataset.nome = u.nome;

            row.innerHTML = `<strong>${u.nome}</strong> — ${u.email}`;

            row.addEventListener("click", () => select(u));

            box.appendChild(row);
        });

        box.style.display = "block";
    }

    // Seleção simples (sem badge)
    function select(u) {
        input.value = u.nome;  // aparece no campo
        hidden.value = u.id;   // usado no filtro
        box.style.display = "none";
    }

    // Fecha ao clicar fora
    document.addEventListener("click", (ev) => {
        if (!box.contains(ev.target) && ev.target !== input) {
            box.style.display = "none";
        }
    });
};
