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

// Live version badge — JSONP from the release channel. release.clawee.org/clawee/version.js
// is a plain <script> that invokes this global with the current published version
// (sourced from the R2 latest.json catalog), so the badge tracks releases without a
// manual bump. The hardcoded <span class="ver"> in index.html is the fallback if the
// script is blocked or the channel is unreachable.
window.__claweeVersion = function (d) {
  if (!d || !d.version) return;
  document.querySelectorAll(".ver").forEach(function (el) {
    el.textContent = "v" + d.version;
  });
};
(function () {
  var s = document.createElement("script");
  s.src = "https://release.clawee.org/clawee/version.js";
  s.async = true;
  s.referrerPolicy = "no-referrer";
  document.head.appendChild(s);
})();
