document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm || "Are you sure?")) event.preventDefault();
    });
  });

  document.querySelectorAll(".composer textarea").forEach((textarea) => {
    const max = Number(textarea.getAttribute("maxlength") || 1000);
    const counter = document.createElement("span");
    counter.className = "muted small";
    counter.style.float = "right";
    const update = () => { counter.textContent = `${textarea.value.length}/${max}`; };
    textarea.insertAdjacentElement("afterend", counter);
    textarea.addEventListener("input", update);
    update();
  });
});
