import React, { useEffect, useMemo, useRef, useState } from 'react';
import { FLAG, download, getJSON, money, num, toCSV, toExcel, toRows } from './lib.js';

const PAGE = 25;
const SORTS = {
  reviews: { label: 'Most reviews', fn: (a, b) => (b.reviews ?? -1) - (a.reviews ?? -1) },
  stars: { label: 'Highest rated', fn: (a, b) => (b.stars ?? -1) - (a.stars ?? -1) },
  priceLow: { label: 'Price: low to high', fn: (a, b) => a.price - b.price },
  priceHigh: { label: 'Price: high to low', fn: (a, b) => b.price - a.price },
  newest: { label: 'Newest', fn: (a, b) => (b.year ?? 0) - (a.year ?? 0) },
  title: { label: 'Title A–Z', fn: (a, b) => a.title.localeCompare(b.title) },
};

export default function Explorer({ meta, scope }) {
  const cats = meta.categories;
  const cache = useRef(new Map());
  const [rows, setRows] = useState(null);
  const [loading, setLoading] = useState(null);
  const [error, setError] = useState(null);
  const [wantAll, setWantAll] = useState(false);
  const [q, setQ] = useState('');
  const [onlyBs, setOnlyBs] = useState(true);
  const [onlyKu, setOnlyKu] = useState(false);
  const [sort, setSort] = useState('reviews');
  const [page, setPage] = useState(0);
  const [exporting, setExporting] = useState(false);

  const isAll = scope === 'All';
  const totalListings = meta.category_table.reduce((s, c) => s + c.listings, 0);

  async function loadCats(indices) {
    const out = [];
    let done = 0;
    setLoading({ done: 0, total: indices.length });
    for (const i of indices) {
      if (!cache.current.has(i)) cache.current.set(i, toRows(await getJSON(`data/books/${i}.json`), cats));
      out.push(...cache.current.get(i));
      done += 1;
      setLoading({ done, total: indices.length });
    }
    setLoading(null);
    return out;
  }

  useEffect(() => {
    let live = true;
    setError(null);
    setPage(0);
    const indices = isAll ? (wantAll ? cats.map((_, i) => i) : null) : [cats.indexOf(scope)];
    if (!indices) { setRows(null); return undefined; }
    loadCats(indices).then((r) => { if (live) setRows(r); }).catch((e) => { if (live) { setError(e.message); setLoading(null); } });
    return () => { live = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [scope, wantAll]);

  const filtered = useMemo(() => {
    if (!rows) return [];
    const needle = q.trim().toLowerCase();
    const out = rows.filter((r) => (!onlyBs || r.flags & FLAG.bestseller) && (!onlyKu || r.flags & FLAG.ku)
      && (!needle || r.title.toLowerCase().includes(needle) || r.author.toLowerCase().includes(needle)));
    return out.sort(SORTS[sort].fn);
  }, [rows, q, onlyBs, onlyKu, sort]);

  useEffect(() => setPage(0), [q, onlyBs, onlyKu, sort]);

  const pages = Math.max(1, Math.ceil(filtered.length / PAGE));
  const view = filtered.slice(page * PAGE, page * PAGE + PAGE);
  const label = isAll ? 'All categories' : scope;

  async function exportXlsx() {
    setExporting(true);
    try { await toExcel(filtered, `${label}${onlyBs ? ', Best Sellers only' : ''}${onlyKu ? ', Kindle Unlimited only' : ''}${q ? `, search "${q}"` : ''}`, meta); }
    finally { setExporting(false); }
  }

  return (
    <div className="explorer">
      <div className="controls">
        <label className="search">
          <span className="sr">Search titles and authors</span>
          <input id="book-search" type="search" placeholder="Search title or author" value={q}
            onChange={(e) => setQ(e.target.value)} onFocus={() => isAll && setWantAll(true)} />
        </label>
        <label className="check"><input id="only-bs" type="checkbox" checked={onlyBs} onChange={(e) => setOnlyBs(e.target.checked)} /> Best Sellers only</label>
        <label className="check"><input id="only-ku" type="checkbox" checked={onlyKu} onChange={(e) => setOnlyKu(e.target.checked)} /> Kindle Unlimited only</label>
        <label className="select">
          <span className="sr">Sort</span>
          <select id="book-sort" value={sort} onChange={(e) => setSort(e.target.value)}>
            {Object.entries(SORTS).map(([k, s]) => <option key={k} value={k}>{s.label}</option>)}
          </select>
        </label>
      </div>

      {isAll && !wantAll && !rows && (
        <div className="empty">
          <p>Browsing all {num(totalListings)} listings downloads about 5 MB. Pick a category above for a quicker look, or load everything.</p>
          <button type="button" className="btn" onClick={() => setWantAll(true)}>Load all listings</button>
        </div>
      )}
      {loading && <p className="status">Loading listings… {loading.done} of {loading.total} files</p>}
      {error && <p className="status err">{error}. Check your connection and reload the page.</p>}

      {rows && (
        <>
          <div className="meta-row">
            <span>{num(filtered.length)} of {num(rows.length)} listings in {label}</span>
            <span className="exports">
              <button type="button" className="btn ghost" disabled={!filtered.length}
                onClick={() => download(new Blob([toCSV(filtered)], { type: 'text/csv' }), 'kindle_listings.csv')}>Export CSV</button>
              <button type="button" className="btn ghost" disabled={!filtered.length || exporting} onClick={exportXlsx}>
                {exporting ? 'Building Excel…' : 'Export Excel'}
              </button>
            </span>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Title</th><th>Author</th>{isAll && <th>Category</th>}<th className="n">Price</th><th className="n">Stars</th><th className="n">Reviews</th><th className="n">Year</th><th>Badges</th></tr>
              </thead>
              <tbody>
                {view.map((r) => (
                  <tr key={r.asin}>
                    <td className="t"><a href={`https://www.amazon.com/dp/${r.asin}`} target="_blank" rel="noopener noreferrer">{r.title}</a></td>
                    <td>{r.author}</td>
                    {isAll && <td className="muted">{r.category}</td>}
                    <td className="n">{r.price === 0 ? 'Free' : money(r.price)}</td>
                    <td className="n">{r.stars ?? '–'}</td>
                    <td className="n" title={r.reviews == null ? 'Not recorded by the scraper' : undefined}>{r.reviews == null ? 'n/r' : num(r.reviews)}</td>
                    <td className="n">{r.year ?? '–'}</td>
                    <td className="badges">
                      {r.flags & FLAG.bestseller ? <span className="chip bs">Best Seller</span> : null}
                      {r.flags & FLAG.ku ? <span className="chip">KU</span> : null}
                      {r.flags & FLAG.editorsPick ? <span className="chip">Editors' Pick</span> : null}
                      {r.flags & FLAG.goodreads ? <span className="chip">Goodreads</span> : null}
                    </td>
                  </tr>
                ))}
                {!view.length && <tr><td colSpan={8} className="none">No listings match. Try clearing a filter.</td></tr>}
              </tbody>
            </table>
          </div>
          <div className="pager">
            <button type="button" className="btn ghost" disabled={page === 0} onClick={() => setPage(page - 1)}>Previous</button>
            <span>Page {page + 1} of {num(pages)}</span>
            <button type="button" className="btn ghost" disabled={page >= pages - 1} onClick={() => setPage(page + 1)}>Next</button>
          </div>
          <p className="foot">“n/r” means the review count was not recorded for that listing. Titles link to the Amazon product page.</p>
        </>
      )}
    </div>
  );
}
