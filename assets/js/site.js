(() => {
  "use strict";
  document.documentElement.classList.add("js");

  const menuButton = document.querySelector(".menu-toggle");
  const nav = document.querySelector("#main-nav");
  const closeMenu = () => {
    menuButton?.setAttribute("aria-expanded", "false");
    nav?.classList.remove("is-open");
  };
  menuButton?.addEventListener("click", () => {
    const opened = menuButton.getAttribute("aria-expanded") !== "true";
    menuButton.setAttribute("aria-expanded", String(opened));
    nav?.classList.toggle("is-open", opened);
  });
  nav?.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu();
  });
  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      menuButton?.getAttribute("aria-expanded") === "true"
    ) {
      closeMenu();
      menuButton.focus();
    }
  });
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".site-header")) closeMenu();
  });
  window.matchMedia("(min-width: 681px)").addEventListener("change", closeMenu);

  const catalog = document.querySelector("[data-catalog]");
  if (!catalog) return;
  const cards = [...catalog.querySelectorAll(".research-card")];
  const filters = [...catalog.querySelectorAll("[data-filter]")];
  const search = catalog.querySelector("#research-search");
  const publicOnly = catalog.querySelector("#public-only");
  const counter = catalog.querySelector("#result-count");
  const empty = catalog.querySelector(".empty-state");
  const normalize = (value) =>
    value.normalize("NFKC").toLocaleLowerCase("ja").replace(/\s+/g, " ").trim();
  const searchable = new Map(
    cards.map((card) => [card, normalize(card.textContent)]),
  );
  let selected = "all";

  function restoreFromUrl() {
    const params = new URLSearchParams(window.location.search);
    selected = filters.some(
      (filter) => filter.dataset.filter === params.get("stage"),
    )
      ? params.get("stage")
      : "all";
    search.value = params.get("q") || "";
    publicOnly.checked = params.get("public") === "true";
    render(false);
  }

  function render(updateUrl = true) {
    const keywords = normalize(search.value).split(" ").filter(Boolean);
    let count = 0;
    cards.forEach((card) => {
      const stageMatch =
        selected === "all" || card.dataset.stage.split(" ").includes(selected);
      const textMatch = keywords.every((word) =>
        searchable.get(card).includes(word),
      );
      const publicMatch = !publicOnly.checked || card.dataset.public === "true";
      const visible = stageMatch && textMatch && publicMatch;
      card.hidden = !visible;
      if (visible) count += 1;
    });
    filters.forEach((filter) =>
      filter.setAttribute(
        "aria-pressed",
        String(filter.dataset.filter === selected),
      ),
    );
    counter.replaceChildren();
    const number = document.createElement("strong");
    number.textContent = String(count);
    counter.append(
      number,
      document.createTextNode(` 件 / 全${cards.length}件の開発項目`),
    );
    empty.hidden = count !== 0;
    if (updateUrl) {
      const url = new URL(window.location.href);
      if (selected === "all") url.searchParams.delete("stage");
      else url.searchParams.set("stage", selected);
      if (search.value.trim()) url.searchParams.set("q", search.value.trim());
      else url.searchParams.delete("q");
      if (publicOnly.checked) url.searchParams.set("public", "true");
      else url.searchParams.delete("public");
      history.replaceState(null, "", url);
    }
  }

  filters.forEach((filter) =>
    filter.addEventListener("click", () => {
      selected = filter.dataset.filter;
      render();
    }),
  );
  search.addEventListener("input", () => render());
  publicOnly.addEventListener("change", () => render());
  catalog.querySelectorAll(".reset-filters").forEach((button) =>
    button.addEventListener("click", () => {
      selected = "all";
      search.value = "";
      publicOnly.checked = false;
      render();
      search.focus();
    }),
  );
  window.addEventListener("popstate", restoreFromUrl);
  restoreFromUrl();
  catalog.querySelector(".catalog-tools").hidden = false;
})();
