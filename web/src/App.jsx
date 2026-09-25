import React, { useEffect, useState } from 'react';
import { CategoryChart, ImportanceChart, KuChart, PriceChart, RankingChart, SimpleRateChart, YearChart } from './Charts.jsx';
import Estimator from './Estimator.jsx';
import Explorer from './Explorer.jsx';
import { getJSON, money, num, pct } from './lib.js';

function Kpi({ label, value, sub }) {
  return (
    <div className="kpi">
      <span className="k">{label}</span>
      <strong>{value}</strong>
      {sub && <span className="s">{sub}</span>}
    </div>
  );
}

export default function App() {
  const [meta, setMeta] = useState(null);
  const [scopes, setScopes] = useState(null);
  const [scope, setScope] = useState('All');
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([getJSON('data/meta.json'), getJSON('data/scopes.json')])
      .then(([m, s]) => { setMeta(m); setScopes(s); })
      .catch((e) => setError(e.message));
  }, []);

  if (error) return <main className="wrap"><p className="status err">{error}. Reload the page to try again.</p></main>;
  if (!meta) return <main className="wrap"><p className="status">Loading 133,102 Kindle listings…</p></main>;

  const s = scopes[scope];
  const k = s.kpis;
  const overall = scopes.All.kpis;
  const gbm = meta.model.models.gbm;
  const lift = gbm.precision_top1pct.mean / meta.model.prevalence;
  const pick = (c) => {
    setScope(c === scope ? 'All' : c);
    document.getElementById('scope-top')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <>
      <header className="hero">
        <div className="wrap">
          <p className="eyebrow">Amazon Kindle store · 133,102 listings · scraped October 2023</p>
          <h1>What goes with the <span className="badge-word">Best Seller</span> badge?</h1>
          <p className="lede">
            Only {pct(overall.bestseller_rate)} of Kindle listings carry Amazon's orange badge. This project cleans the
            full catalogue, measures which traits go with the badge, and trains a model to rank the listings most likely to have it.
          </p>
        </div>
      </header>

      <main>
        <section className="scope-bar" id="scope-top">
          <div className="wrap scope-inner">
            <label htmlFor="scope">Showing</label>
            <select id="scope" value={scope} onChange={(e) => setScope(e.target.value)}>
              <option value="All">All 31 categories</option>
              {meta.categories.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
            {scope !== 'All' && <button type="button" className="btn ghost sm" onClick={() => setScope('All')}>Show all</button>}
          </div>
        </section>

        <section className="wrap kpis">
          <Kpi label="Listings" value={num(k.listings)} sub={`${num(k.unique_books)} unique books`} />
          <Kpi label="Best Sellers" value={num(k.bestsellers)} sub={`${pct(k.bestseller_rate)} of listings`} />
          <Kpi label="Median price" value={money(k.median_price)} sub={`${pct(k.free_share)} free`} />
          <Kpi label="Average rating" value={k.avg_stars ? k.avg_stars.toFixed(2) : '–'} sub="out of 5 stars" />
          <Kpi label="In Kindle Unlimited" value={pct(k.ku_share, 0)} sub="of listings" />
          <Kpi label="Median reviews" value={k.median_reviews == null ? 'n/r' : num(k.median_reviews)}
            sub={k.review_capture < 0.5 ? 'not recorded in this category' : `recorded for ${pct(k.review_capture, 0)}`} />
        </section>

        {scope === 'All' && (
          <section className="wrap findings">
            <h2>Key findings</h2>
            <ol>{meta.insights.map((t) => <li key={t}>{t}</li>)}</ol>
          </section>
        )}

        <section className="wrap grid two">
          <PriceChart data={s.price} base={k.bestseller_rate} />
          <KuChart data={s.ku} />
          <YearChart data={s.years} />
          <SimpleRateChart title="By star rating" labelKey="band" data={s.stars}
            note="Ratings barely separate books: almost everything sits between 4.3 and 4.8 stars." />
          <SimpleRateChart horizontal title="By publisher group" labelKey="group" data={s.publishers}
            note="Seller names normalised into five groups. Amazon is the seller for most self-published books." />
          {scope === 'All' ? (
            <div className="panel authors">
              <h3>Authors with the most Best Seller listings</h3>
              <table className="mini">
                <thead><tr><th>Author</th><th className="n">Best Sellers</th><th className="n">Listings</th></tr></thead>
                <tbody>{meta.top_authors.map((a) => <tr key={a.author}><td>{a.author}</td><td className="n">{a.bestsellers}</td><td className="n">{a.listings}</td></tr>)}</tbody>
              </table>
            </div>
          ) : (
            <div className="panel authors">
              <h3>{scope} vs all categories</h3>
              <table className="mini">
                <tbody>
                  <tr><td>Badge rate</td><td className="n">{pct(k.bestseller_rate)}</td><td className="n muted">{pct(overall.bestseller_rate)}</td></tr>
                  <tr><td>Median price</td><td className="n">{money(k.median_price)}</td><td className="n muted">{money(overall.median_price)}</td></tr>
                  <tr><td>Kindle Unlimited share</td><td className="n">{pct(k.ku_share, 0)}</td><td className="n muted">{pct(overall.ku_share, 0)}</td></tr>
                  <tr><td>Average rating</td><td className="n">{k.avg_stars?.toFixed(2)}</td><td className="n muted">{overall.avg_stars.toFixed(2)}</td></tr>
                </tbody>
              </table>
            </div>
          )}
        </section>

        <section className="wrap">
          <CategoryChart data={meta.category_table} base={overall.bestseller_rate} active={scope} onPick={pick} />
        </section>

        <section className="band">
          <div className="wrap">
            <h2>Can a model find the bestsellers?</h2>
            <p className="section-lede">
              With a badge this rare, accuracy is meaningless: always guessing “no” is {pct(meta.model.always_no_accuracy)} accurate.
              So each model ranks all listings and is judged on how many real bestsellers land at the top. Every score is from
              5-fold cross-validation, with all listings of the same book kept in the same fold.
            </p>
            <div className="grid three stats">
              <Kpi label="Top 1% precision" value={pct(gbm.precision_top1pct.mean)} sub={`${lift.toFixed(0)}× the ${pct(meta.model.prevalence)} base rate`} />
              <Kpi label="Bestsellers found in top 5%" value={pct(gbm.recall_top5pct.mean, 0)} sub="of all badge listings" />
              <Kpi label="ROC-AUC" value={gbm.roc_auc.mean.toFixed(2)} sub={`PR-AUC ${gbm.pr_auc.mean.toFixed(3)} vs ${meta.model.prevalence.toFixed(3)} random`} />
            </div>
            <div className="grid two">
              <RankingChart models={meta.model.models} prevalence={meta.model.prevalence} />
              <ImportanceChart data={meta.model.permutation_importance} />
            </div>
            <h3 className="sub-h">Try a listing</h3>
            <Estimator key={scope} meta={meta} scope={scope} />
          </div>
        </section>

        <section className="wrap">
          <h2>Browse the listings</h2>
          <Explorer meta={meta} scope={scope} />
        </section>

        <section className="wrap method">
          <h2>Data and method</h2>
          <p>
            Source: <a href={meta.source.url} target="_blank" rel="noopener noreferrer">{meta.source.name}</a> by {meta.source.author},
            scraped {meta.source.scraped}. Cleaning and analysis run in Python (pandas, scikit-learn, Matplotlib, Seaborn); this
            page reads the exported results.
          </p>
          <div className="table-wrap">
            <table className="mini clean">
              <thead><tr><th>Cleaning step</th><th className="n">Rows</th><th>What and why</th></tr></thead>
              <tbody>
                {meta.cleaning.steps.map((st) => (
                  <tr key={st.step}><td>{st.step}</td><td className="n">{num(st.rows_affected)}</td><td className="muted">{st.note}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
          <ul className="caveats">
            <li>The badge reflects one moment (October 2023). It is shown per category page, so the same book can have it in one listing and not another.</li>
            <li>Ratings and reviews are measured at the same time as the badge, so the model shows association, not cause or a forecast.</li>
            <li>Amazon shows at most one badge per listing, so Editors' Pick and Goodreads Choice were left out of the model to avoid a shortcut.</li>
          </ul>
        </section>
      </main>

      <footer className="wrap foot-site">
        <span>Kindle Bestseller Analyzer · Akash Mondal</span>
        <span>Not affiliated with Amazon. Data © respective owners, via Kaggle.</span>
      </footer>
    </>
  );
}
