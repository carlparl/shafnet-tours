(() => {
  "use strict";

  const storageKey = "shafnet-admin-sidebar-collapsed";
  const body = document.body;
  const toggle = document.querySelector("[data-sidebar-toggle]");
  if (!body || !toggle) return;

  const applyState = (collapsed) => {
    body.classList.toggle("workspace-collapsed", collapsed);
    toggle.setAttribute("aria-expanded", String(!collapsed));
    toggle.setAttribute(
      "aria-label",
      collapsed ? "Expand workspace navigation" : "Collapse workspace navigation"
    );
  };

  let collapsed = false;
  try {
    collapsed = localStorage.getItem(storageKey) === "true";
  } catch (_) {
    collapsed = false;
  }
  applyState(collapsed);

  toggle.addEventListener("click", () => {
    collapsed = !body.classList.contains("workspace-collapsed");
    applyState(collapsed);
    try {
      localStorage.setItem(storageKey, String(collapsed));
    } catch (_) {
      // The control still works when browser storage is unavailable.
    }
  });
})();
