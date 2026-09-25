import React, { useMemo, useState } from 'react';
import { estimate, pct } from './lib.js';

const PUBLISHERS = ['Sold by Amazon.com', 'Big Five', 'Academic & professional', 'Other publishers', 'Not listed'];

export default function Estimator({ meta, scope }) {
  const m = meta.estimator;
  const [category, setCategory] = useState(scope !== 'All' ? scope : 'Literature & Fiction');
  const [price, setPrice] = useState('4.99');
  const [stars, setStars] = useState('4.5');
  const [reviews, setReviews] = useState('500');
  const [year, setYear] = useState('2022');
  const [ku, setKu] = useState(true);
  const [publisher, setPublisher] = useState('Sold by Amazon.com');

  const p = useMemo(() => {
    const n = (v) => (v === '' || Number.isNaN(Number(v)) ? null : Number(v));
    const priceN = n(price);
    if (priceN == null || priceN < 0) return null;
    return estimate(m, { category, price: priceN, stars: n(stars), reviews: n(reviews), year: n(year), ku, publisher });
  }, [m, category, price, stars, reviews, year, ku, publisher]);

  const ratio = p != null ? p / m.prevalence : null;
  const logistic = meta.model.models.logistic;

  return (
    <div className="estimator">
      <form className="est-form" onSubmit={(e) => e.preventDefault()}>
        <label>Category
          <select id="est-category" value={category} onChange={(e) => setCategory(e.target.value)}>
            {meta.categories.map((c) => <option key={c}>{c}</option>)}
          </select>
        </label>
        <label>Price ($)
          <input id="est-price" type="number" min="0" step="0.01" value={price} onChange={(e) => setPrice(e.target.value)} />
        </label>
        <label>Star rating <small>(blank = unrated)</small>
          <input id="est-stars" type="number" min="1" max="5" step="0.1" value={stars} onChange={(e) => setStars(e.target.value)} />
        </label>
        <label>Reviews <small>(blank = unknown)</small>
          <input id="est-reviews" type="number" min="0" step="1" value={reviews} onChange={(e) => setReviews(e.target.value)} />
        </label>
        <label>Publication year <small>(blank = unknown)</small>
          <input id="est-year" type="number" min="1900" max="2024" step="1" value={year} onChange={(e) => setYear(e.target.value)} />
        </label>
        <label>Publisher
          <select id="est-publisher" value={publisher} onChange={(e) => setPublisher(e.target.value)}>
            {PUBLISHERS.map((x) => <option key={x}>{x}</option>)}
          </select>
        </label>
        <label className="check wide"><input id="est-ku" type="checkbox" checked={ku} onChange={(e) => setKu(e.target.checked)} /> In Kindle Unlimited</label>
      </form>
      <div className="est-out" aria-live="polite">
        <span className="k">Share of similar listings with the badge</span>
        <strong>{p == null ? '–' : pct(p, p < 0.01 ? 2 : 1)}</strong>
        <span className="vs">
          {ratio == null ? 'Enter a price to see an estimate.' : `${ratio >= 1 ? `${ratio.toFixed(1)}× the` : `${(ratio * 100).toFixed(0)}% of the`} ${pct(m.prevalence)} average`}
        </span>
        <p className="fine">
          Logistic regression trained on all 133k listings (cross-validated ROC-AUC {logistic.roc_auc.mean.toFixed(2)}).
          It describes which traits go with the badge in October 2023; it is not a sales forecast.
        </p>
      </div>
    </div>
  );
}
