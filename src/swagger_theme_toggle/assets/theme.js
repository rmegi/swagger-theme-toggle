(function () {
  var STORAGE_KEY = "swagger-theme-toggle:theme";
  var root = document.documentElement;

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    var buttons = document.querySelectorAll(".stt-toggle button");
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      if (btn.getAttribute("data-theme") === theme) {
        btn.classList.add("stt-active");
      } else {
        btn.classList.remove("stt-active");
      }
    }
  }

  function currentTheme() {
    return localStorage.getItem(STORAGE_KEY) || "system";
  }

  function init() {
    var bar = document.createElement("div");
    bar.className = "stt-toggle";

    var themes = [
      ["light", "Light"],
      ["dark", "Dark"],
      ["system", "Auto"],
    ];

    themes.forEach(function (entry) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.setAttribute("data-theme", entry[0]);
      btn.title = entry[1];
      btn.textContent = entry[1];
      btn.addEventListener("click", function () {
        var theme = this.getAttribute("data-theme");
        localStorage.setItem(STORAGE_KEY, theme);
        applyTheme(theme);
      });
      bar.appendChild(btn);
    });

    document.body.appendChild(bar);
    applyTheme(currentTheme());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
