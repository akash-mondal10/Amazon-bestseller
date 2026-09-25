import React from 'react';
import {
  Bar, BarChart, CartesianGrid, Cell, ComposedChart, Line, ReferenceLine,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts';
import { num, pct } from './lib.js';

const INK = '#1f2430';
const ACCENT = '#d9731a';
const MUTED = '#b9c0cc';
const GRID = '#ebe8e1';
const rateTick = (v) => { const x = v * 100; return `${Number.isInteger(Math.round(x * 10) / 10) ? Math.round(x) : x.toFixed(1)}%`; };
const tick = { fill: '#5b6272', fontSize: 12, fontFamily: 'IBM Plex Mono, ui-monospace, monospace' };

function Tip({ active, payload, label, render }) {
  if (!active || !payload?.length) return null;
  return <div className="tip">{render(payload[0].payload, label)}</div>;
}

export function Panel({ title, note, children }) {
  return (
    <figure className="panel">
      <figcaption>
        <h3>{title}</h3>
        {note && <p>{note}</p>}
      </figcaption>
      {children}
    </figure>
  );
}

export function PriceChart({ data, base }) {
  return (
    <Panel title="Badge rate by price" note="Share of listings in each price band that carry the Best Seller badge.">
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} margin={{ top: 10, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid vertical={false} stroke={GRID} />
          <XAxis dataKey="band" tick={tick} interval={0} tickLine={false} axisLine={{ stroke: GRID }} height={40} angle={-20} textAnchor="end" />
          <YAxis tickFormatter={rateTick} tick={tick} width={44} tickLine={false} axisLine={false} />
          <ReferenceLine y={base} stroke={INK} strokeDasharray="4 4" />
          <Tooltip cursor={{ fill: '#f3efe7' }} content={<Tip render={(d) => (<><b>{d.band}</b><span>{pct(d.rate, 2)} have the badge</span><span>{num(d.bestsellers)} of {num(d.listings)} listings</span></>)} />} />
          <Bar dataKey="rate" radius={[3, 3, 0, 0]}>
            {data.map((d) => <Cell key={d.band} fill={d.rate >= base ? ACCENT : MUTED} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Panel>
  );
}

export function KuChart({ data }) {
  const [ku, not] = data;
  const ratio = not.rate ? ku.rate / not.rate : null;
  return (
    <Panel title="Kindle Unlimited" note={ratio ? `Books in Kindle Unlimited carry the badge ${ratio.toFixed(1)}× as often.` : 'Badge rate for books in and out of Kindle Unlimited.'}>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} layout="vertical" margin={{ top: 10, right: 56, left: 8, bottom: 0 }}>
          <CartesianGrid horizontal={false} stroke={GRID} />
          <XAxis type="number" tickFormatter={rateTick} tick={tick} tickLine={false} axisLine={{ stroke: GRID }} />
          <YAxis type="category" dataKey="label" tick={{ ...tick, fontFamily: 'IBM Plex Sans, sans-serif' }} width={118} tickLine={false} axisLine={false} />
          <Tooltip cursor={{ fill: '#f3efe7' }} content={<Tip render={(d) => (<><b>{d.label}</b><span>{pct(d.rate, 2)} have the badge</span><span>{num(d.listings)} listings</span></>)} />} />
          <Bar dataKey="rate" radius={[0, 3, 3, 0]} barSize={34} label={{ position: 'right', formatter: (v) => pct(v), fill: INK, fontSize: 12 }}>
            <Cell fill={ACCENT} />
            <Cell fill={MUTED} />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Panel>
  );
}

export function CategoryChart({ data, base, active, onPick }) {
  const h = Math.max(320, data.length * 22 + 40);
  return (
    <Panel title="Badge rate by category" note="Click a bar to focus the whole page on that category. The dashed line is the overall rate.">
      <ResponsiveContainer width="100%" height={h}>
        <BarChart data={data} layout="vertical" margin={{ top: 6, right: 48, left: 4, bottom: 0 }}>
          <CartesianGrid horizontal={false} stroke={GRID} />
          <XAxis type="number" tickFormatter={rateTick} tick={tick} tickLine={false} axisLine={{ stroke: GRID }} />
          <YAxis type="category" dataKey="category" width={210} interval={0} tick={{ ...tick, fontSize: 11.5, fontFamily: 'IBM Plex Sans, sans-serif' }} tickLine={false} axisLine={false} />
          <ReferenceLine x={base} stroke={INK} strokeDasharray="4 4" />
          <Tooltip cursor={{ fill: '#f3efe7' }} content={<Tip render={(d) => (<><b>{d.category}</b><span>{pct(d.rate, 2)} have the badge</span><span>{num(d.bestsellers)} of {num(d.listings)} listings</span></>)} />} />
          <Bar dataKey="rate" radius={[0, 3, 3, 0]} onClick={(d) => onPick(d.category ?? d.payload?.category)} style={{ cursor: 'pointer' }}>
            {data.map((d) => (
              <Cell key={d.category} fill={active === d.category ? INK : d.rate >= base ? ACCENT : MUTED} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Panel>
  );
}

export function YearChart({ data }) {
  const rows = data.filter((d) => d.listings >= 30);
  return (
    <Panel title="By publication year" note="Bars: listings published that year. Line: badge rate. Years with fewer than 30 listings are hidden.">
      <ResponsiveContainer width="100%" height={260}>
        <ComposedChart data={rows} margin={{ top: 10, right: 4, left: 0, bottom: 0 }}>
          <CartesianGrid vertical={false} stroke={GRID} />
          <XAxis dataKey="year" tick={tick} tickLine={false} axisLine={{ stroke: GRID }} minTickGap={16} />
          <YAxis yAxisId="n" tickFormatter={(v) => (v >= 1000 ? `${v / 1000}k` : v)} tick={tick} width={40} tickLine={false} axisLine={false} />
          <YAxis yAxisId="r" orientation="right" tickFormatter={rateTick} tick={tick} width={40} tickLine={false} axisLine={false} />
          <Tooltip content={<Tip render={(d) => (<><b>{d.year}</b><span>{num(d.listings)} listings</span><span>{pct(d.rate, 2)} have the badge</span></>)} />} />
          <Bar yAxisId="n" dataKey="listings" fill="#e4e0d7" radius={[2, 2, 0, 0]} />
          <Line yAxisId="r" dataKey="rate" stroke={ACCENT} strokeWidth={2.5} dot={{ r: 2.5 }} connectNulls />
        </ComposedChart>
      </ResponsiveContainer>
    </Panel>
  );
}

export function SimpleRateChart({ title, note, data, labelKey, horizontal }) {
  if (horizontal) {
    return (
      <Panel title={title} note={note}>
        <ResponsiveContainer width="100%" height={Math.max(200, data.length * 38 + 30)}>
          <BarChart data={data} layout="vertical" margin={{ top: 6, right: 52, left: 8, bottom: 0 }}>
            <CartesianGrid horizontal={false} stroke={GRID} />
            <XAxis type="number" tickFormatter={rateTick} tick={tick} tickLine={false} axisLine={{ stroke: GRID }} />
            <YAxis type="category" dataKey={labelKey} width={160} tick={{ ...tick, fontFamily: 'IBM Plex Sans, sans-serif' }} tickLine={false} axisLine={false} />
            <Tooltip cursor={{ fill: '#f3efe7' }} content={<Tip render={(d) => (<><b>{d[labelKey]}</b><span>{pct(d.rate, 2)} have the badge</span><span>{num(d.listings)} listings</span></>)} />} />
            <Bar dataKey="rate" fill={INK} radius={[0, 3, 3, 0]} barSize={20} label={{ position: 'right', formatter: (v) => pct(v), fill: INK, fontSize: 11 }} />
          </BarChart>
        </ResponsiveContainer>
      </Panel>
    );
  }
  return (
    <Panel title={title} note={note}>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} margin={{ top: 10, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid vertical={false} stroke={GRID} />
          <XAxis dataKey={labelKey} tick={{ ...tick, fontSize: 11 }} interval={0} tickLine={false} axisLine={{ stroke: GRID }} />
          <YAxis tickFormatter={rateTick} tick={tick} width={44} tickLine={false} axisLine={false} />
          <Tooltip cursor={{ fill: '#f3efe7' }} content={<Tip render={(d) => (<><b>{d[labelKey]}</b><span>{pct(d.rate, 2)} have the badge</span><span>{num(d.listings)} listings</span></>)} />} />
          <Bar dataKey="rate" fill={INK} radius={[3, 3, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </Panel>
  );
}

export function RankingChart({ models, prevalence }) {
  const names = { baseline: 'Random pick', logistic: 'Logistic regression', gbm: 'Gradient boosting' };
  const data = Object.entries(names).map(([k, label]) => ({ label, value: models[k].precision_top1pct.mean, sd: models[k].precision_top1pct.std }));
  return (
    <Panel title="How often the top 1% are real bestsellers" note={`Each model ranks every listing; this is the share of its top 1% that carry the badge. Random picking gets about ${pct(prevalence)}.`}>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} layout="vertical" margin={{ top: 6, right: 56, left: 8, bottom: 0 }}>
          <CartesianGrid horizontal={false} stroke={GRID} />
          <XAxis type="number" tickFormatter={rateTick} tick={tick} tickLine={false} axisLine={{ stroke: GRID }} />
          <YAxis type="category" dataKey="label" width={140} tick={{ ...tick, fontFamily: 'IBM Plex Sans, sans-serif' }} tickLine={false} axisLine={false} />
          <Tooltip cursor={{ fill: '#f3efe7' }} content={<Tip render={(d) => (<><b>{d.label}</b><span>{pct(d.value)} (± {pct(d.sd)} across 5 folds)</span></>)} />} />
          <Bar dataKey="value" barSize={26} radius={[0, 3, 3, 0]} label={{ position: 'right', formatter: (v) => pct(v), fill: INK, fontSize: 12 }}>
            {data.map((d, i) => <Cell key={d.label} fill={[MUTED, '#c9a57c', ACCENT][i]} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Panel>
  );
}

export function ImportanceChart({ data }) {
  const rows = data.filter((d) => d.importance > 0.0005);
  return (
    <Panel title="What the model relies on" note="Drop in ranking quality (PR-AUC) when each feature is shuffled on held-out books. Bigger means more important.">
      <ResponsiveContainer width="100%" height={Math.max(200, rows.length * 30 + 30)}>
        <BarChart data={rows} layout="vertical" margin={{ top: 6, right: 20, left: 8, bottom: 0 }}>
          <CartesianGrid horizontal={false} stroke={GRID} />
          <XAxis type="number" tick={tick} tickLine={false} axisLine={{ stroke: GRID }} tickFormatter={(v) => v.toFixed(2)} />
          <YAxis type="category" dataKey="feature" width={140} tick={{ ...tick, fontFamily: 'IBM Plex Sans, sans-serif' }} tickLine={false} axisLine={false} />
          <Tooltip cursor={{ fill: '#f3efe7' }} content={<Tip render={(d) => (<><b>{d.feature}</b><span>PR-AUC drop {d.importance.toFixed(4)}</span></>)} />} />
          <Bar dataKey="importance" fill={ACCENT} radius={[0, 3, 3, 0]} barSize={18} />
        </BarChart>
      </ResponsiveContainer>
    </Panel>
  );
}
