// clawee.org — copy-to-clipboard for command snippets. No dependencies.
document.querySelectorAll(".copy").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var text = btn.getAttribute("data-copy") || "";
    navigator.clipboard.writeText(text).then(function () {
      var prev = btn.textContent;
      btn.textContent = "copied";
      btn.classList.add("copied");
      setTimeout(function () {
        btn.textContent = prev;
        btn.classList.remove("copied");
      }, 1400);
    }).catch(function () {
      btn.textContent = "ctrl+c";
      setTimeout(function () { btn.textContent = "copy"; }, 1400);
    });
  });
});
