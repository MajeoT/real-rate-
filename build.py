"""Build the website (index.html) from the Claude artifact page, adding the phone-app parts.

Usage: python3 build.py /path/to/real-rate.html
"""
import sys

src = open(sys.argv[1]).read().replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
i = src.index('<div class="wrap">')

head = '''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Log hours worked and paid, and see your real hourly rate, take-home pay and fuel costs.">
<meta name="theme-color" content="#0b6e66">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Real Rate">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}.install{background:var(--accent);color:var(--accent-fg);border-color:var(--accent);padding:4px 12px;font-size:13px}</style>
'''

app_bits = '''<script>
// Phone app: offline worker, and an Install button where the browser supports one (Android Chrome, Edge).
(function () {
  if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(function () {});
  var prompt = null, btn = document.createElement("button");
  btn.type = "button"; btn.className = "install"; btn.textContent = "Install app"; btn.hidden = true;
  var header = document.querySelector("header"); if (header) header.appendChild(btn);
  window.addEventListener("beforeinstallprompt", function (e) { e.preventDefault(); prompt = e; btn.hidden = false; });
  btn.addEventListener("click", function () { if (!prompt) return; prompt.prompt(); prompt.userChoice.finally(function () { prompt = null; btn.hidden = true; }); });
  window.addEventListener("appinstalled", function () { btn.hidden = true; });
})();
</script>
'''

out = head + src[:i] + '</head>\n<body>\n' + src[i:] + app_bits + '</body>\n</html>\n'
open('index.html', 'w').write(out)
print('built index.html')
