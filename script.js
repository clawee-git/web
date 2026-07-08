// clawee.org — copy-to-clipboard for command snippets. No dependencies.
document.querySelectorAll(".copy").forEach(function (btn) {
  btn.setAttribute("aria-live", "polite"); // announce the "copied" feedback to screen readers
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
  // Trust the payload only if it looks like a version string (JSONP runs foreign code
  // paths; never write anything that isn't a plain semver-ish string).
  if (!d || typeof d.version !== "string" || !/^v?\d+\.\d+\.\d+(-[\w.]+)?$/.test(d.version)) return;
  document.querySelectorAll(".ver").forEach(function (el) {
    el.textContent = "v" + d.version.replace(/^v/, "");
  });
};
(function () {
  var s = document.createElement("script");
  // Hourly cache-buster: the query changes once per clock hour, so a returning
  // visitor picks up a new release within the hour even though the CF edge
  // caches version.js for up to 4h. Stable WITHIN the hour → CF still serves a
  // single cached copy per hour (no cache-thrash).
  s.src = "https://release.clawee.org/clawee/version.js?" + Math.floor(Date.now() / 3600000);
  s.async = true;
  s.referrerPolicy = "no-referrer";
  document.head.appendChild(s);
})();
