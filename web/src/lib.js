// Shared helpers: formatting, data loading and the in-browser estimator.

export const pct = (x, d = 1) => (x == null ? '–' : `${(x * 100).toFixed(d)}%`);
export const num = (x) => (x == null ? '–' : Math.round(x).toLocaleString('en-US'));
export const money = (x) => (x == null ? '–' : `$${x.toFixed(2)}`);

export async function getJSON(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Could not load ${path} (${res.status})`);
  return res.json();
}

export const FLAG = { bestseller: 1, ku: 2, editorsPick: 4, goodreads: 8 };

// Turn a columnar book file into row objects.
export function toRows(cols, categories) {
  const n = cols.asin.length;
  const rows = new Array(n);
  for (let i = 0; i < n; i++) {
    rows[i] = {
      asin: cols.asin[i],
      title: cols.title[i],
      author: cols.author[i],
      price: cols.price[i],
      stars: cols.stars[i],
      reviews: cols.reviews[i],
      year: cols.year[i],
      flags: cols.flags[i],
      category: categories[cols.category[i]],
    };
  }
  return rows;
}

// Same maths as the scikit-learn pipeline in analysis/kindle_analyzer/model.py:
// median imputation -> standard scaling -> logistic regression.
export function estimate(model, input) {
  const raw = {
    log_price: Math.log1p(input.price),
    stars: input.stars == null ? NaN : input.stars,
    log_reviews: input.reviews == null ? NaN : Math.log1p(input.reviews),
    pub_year: input.year == null ? NaN : input.year,
  };
  let z = model.intercept;
  for (const [f, p] of Object.entries(model.numeric)) {
    const x = Number.isNaN(raw[f]) ? p.median : raw[f];
    z += p.coef * ((x - p.mean) / p.scale);
  }
  const bin = {
    is_free: input.price === 0 ? 1 : 0,
    is_ku: input.ku ? 1 : 0,
    reviews_recorded: input.reviews == null ? 0 : 1,
    has_pub_date: input.year == null ? 0 : 1,
  };
  for (const [f, c] of Object.entries(model.binary)) z += c * bin[f];
  z += model.categorical.category[input.category] ?? 0;
  z += model.categorical.publisher_group[input.publisher] ?? 0;
  return 1 / (1 + Math.exp(-z));
}

export function toCSV(rows) {
  const head = ['Title', 'Author', 'Category', 'Price', 'Stars', 'Reviews', 'Year', 'Best Seller', 'Kindle Unlimited', 'Amazon URL'];
  const esc = (v) => {
    const s = v == null ? '' : String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const lines = rows.map((r) => [
    r.title, r.author, r.category, r.price, r.stars, r.reviews, r.year,
    r.flags & FLAG.bestseller ? 'Yes' : 'No', r.flags & FLAG.ku ? 'Yes' : 'No',
    `https://www.amazon.com/dp/${r.asin}`,
  ].map(esc).join(','));
  return [head.join(','), ...lines].join('\n');
}

export function download(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export async function toExcel(rows, scopeLabel, meta) {
  const ExcelJS = (await import('exceljs')).default;
  const wb = new ExcelJS.Workbook();
  const head = { font: { bold: true, color: { argb: 'FFFFFFFF' } }, fill: { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF1F2430' } } };

  const ws = wb.addWorksheet('Listings');
  ws.columns = [
    { header: 'Title', key: 'title', width: 60 },
    { header: 'Author', key: 'author', width: 28 },
    { header: 'Category', key: 'category', width: 28 },
    { header: 'Price ($)', key: 'price', width: 10 },
    { header: 'Stars', key: 'stars', width: 8 },
    { header: 'Reviews', key: 'reviews', width: 10 },
    { header: 'Year', key: 'year', width: 8 },
    { header: 'Best Seller', key: 'bs', width: 12 },
    { header: 'Kindle Unlimited', key: 'ku', width: 16 },
    { header: 'Amazon URL', key: 'url', width: 36 },
  ];
  ws.getRow(1).eachCell((c) => Object.assign(c, head));
  rows.forEach((r) => ws.addRow({
    ...r, bs: r.flags & FLAG.bestseller ? 'Yes' : 'No', ku: r.flags & FLAG.ku ? 'Yes' : 'No',
    url: `https://www.amazon.com/dp/${r.asin}`,
  }));
  ws.views = [{ state: 'frozen', ySplit: 1 }];

  const info = wb.addWorksheet('About');
  info.addRows([
    ['Kindle Bestseller Analyzer export'],
    ['Scope', scopeLabel],
    ['Rows', rows.length],
    ['Source', `${meta.source.name}, ${meta.source.author}, scraped ${meta.source.scraped}`],
    ['Source URL', meta.source.url],
    ['Note', 'Reviews are blank where the scraper did not record them.'],
  ]);
  info.getColumn(1).width = 14;
  info.getColumn(2).width = 90;
  info.getCell('A1').font = { bold: true, size: 14 };

  const buf = await wb.xlsx.writeBuffer();
  download(new Blob([buf], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }), 'kindle_listings.xlsx');
}
