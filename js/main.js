const NAV_ITEMS = [
  { href: "index.html", label: "Dashboard" },
  { href: "forecast.html", label: "Forecast" },
  { href: "clustering.html", label: "Clustering" },
  { href: "country.html", label: "Country" },
  { href: "about.html", label: "About" },
];

function renderNav(active) {
  const nav = document.getElementById("nav");
  nav.innerHTML = NAV_ITEMS.map(
    (item) => `<a href="${item.href}" class="${item.href === active ? "active" : ""}">${item.label}</a>`
  ).join("");
}

function fmt(n, digits = 0) {
  return Number(n).toLocaleString(undefined, { maximumFractionDigits: digits, minimumFractionDigits: digits });
}

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "html") node.innerHTML = v;
    else node.setAttribute(k, v);
  }
  for (const child of [].concat(children)) {
    if (child == null) continue;
    node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }
  return node;
}

const CHIP_CLASS = ["chip-0", "chip-1", "chip-2", "chip-3"];
const CHART_COLORS = ["#16a34a", "#2563eb", "#d97706", "#0d9488"];
