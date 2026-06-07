// Faithful Node simulation of the landing-page client ranking, run against the
// REAL inlined search index from index.html. Verifies the issue-#1 (§1) example
// queries now resolve to the expected sessions. Mirrors the BM25-lite + synonym
// expansion logic emitted by scripts/generate_site.py.
const fs = require('fs');
const path = require('path');

const repo = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(repo, 'index.html'), 'utf8');
const m = html.match(/<script id="search-data" type="application\/json">([\s\S]*?)<\/script>/);
if (!m) { console.error('NO search-data'); process.exit(2); }
const INDEX = JSON.parse(m[1].replace(/\\u003c/g, '<'));
const DOCS = INDEX.docs || [];
const SYN = INDEX.synonyms || {};

const STOP = {};
('a an and the of to in on for with by from at as is are was were be been this' +
 ' that it its they them their what which how why when where can could should' +
 ' would may might will do does did have has had you your we our us i me my').split(' ')
  .forEach(w => STOP[w] = 1);

function tokenize(s) {
  const mm = (s || '').toLowerCase().match(/[a-z0-9][a-z0-9.+#/-]*[a-z0-9]|[a-z0-9]/g) || [];
  const out = [];
  for (const tk of mm) {
    const t = tk.replace(/^[.\-/]+|[.\-/]+$/g, '');
    if (t.length < 2 || STOP[t]) continue;
    out.push(t);
  }
  return out;
}

function expandQuery(q) {
  const terms = {};
  const base = tokenize(q);
  base.forEach(t => terms[t] = Math.max(terms[t] || 0, 1.0));
  function addSyn(list) {
    (list || []).forEach(phrase => tokenize(phrase).forEach(t => {
      terms[t] = Math.max(terms[t] || 0, 0.6);
    }));
  }
  const ql = (q || '').toLowerCase().trim();
  if (SYN[ql]) addSyn(SYN[ql]);
  base.forEach(t => { if (SYN[t]) addSyn(SYN[t]); });
  for (const key in SYN) {
    const members = SYN[key];
    for (const b of base) {
      if (key.indexOf(b) !== -1 || members.join(' ').indexOf(b) !== -1) {
        terms[tokenize(key)[0]] = Math.max(terms[tokenize(key)[0]] || 0, 0.5);
        break;
      }
    }
  }
  return terms;
}

function repeat(arr, n) { let o = []; for (let r = 0; r < n; r++) o = o.concat(arr); return o; }
function joinTokens(list) { return (!list || !list.length) ? [] : tokenize(list.join(' ')); }

const N = DOCS.length;
const df = {}; const docTokens = []; const docLen = []; let avgdl = 0;
for (let d = 0; d < N; d++) {
  const doc = DOCS[d];
  const weighted = []
    .concat(repeat(tokenize(doc.title || ''), 3))
    .concat(repeat(joinTokens(doc.tags), 2))
    .concat(repeat(tokenize((doc.speakers || []).join(' ')), 2))
    .concat(tokenize(doc.text || ''))
    .concat(joinTokens(doc.keywords));
  const tf = {};
  for (const w of weighted) tf[w] = (tf[w] || 0) + 1;
  docTokens.push(tf); docLen.push(weighted.length); avgdl += weighted.length;
  const seen = {};
  for (const t in tf) if (!seen[t]) { df[t] = (df[t] || 0) + 1; seen[t] = 1; }
}
avgdl = N ? avgdl / N : 1;
function idf(t) { const n = df[t] || 0; return Math.log(1 + (N - n + 0.5) / (n + 0.5)); }
const K1 = 1.5, B = 0.75;
function scoreDoc(d, qt) {
  const tf = docTokens[d], dl = docLen[d]; let s = 0;
  for (const t in qt) {
    const f = tf[t]; if (!f) continue;
    s += idf(t) * (f * (K1 + 1) / (f + K1 * (1 - B + B * dl / avgdl))) * qt[t];
  }
  return s;
}

function search(q, topk = 8) {
  const qt = expandQuery(q);
  const ql = q.toLowerCase();
  const scored = [];
  for (let d = 0; d < N; d++) {
    const doc = DOCS[d];
    let sc = scoreDoc(d, qt);
    const hay = ((doc.code || '') + ' ' + (doc.title || '')).toLowerCase();
    if (doc.code && ql === doc.code.toLowerCase()) sc += 1000;
    else if (hay.indexOf(ql) !== -1) sc += 5;
    if (sc > 0) scored.push({ doc, score: sc, ord: d });
  }
  scored.sort((a, b) => b.score !== a.score ? b.score - a.score : a.ord - b.ord);
  return scored.slice(0, topk).map(x => ({
    id: x.doc.code || x.doc.id, type: x.doc.type, score: +x.score.toFixed(2),
  }));
}

// §1-style queries where plain substring search previously FAILED entirely.
// Lexical BM25 + synonym expansion must now surface the right cluster in the
// top-8 unified results (sessions + concepts). (Per-session *semantic* nearest
// neighbours are additionally baked into each page as static "Related".)
const QUERIES = {
  'how do I observe agents in production': ['BRK252', 'ODSP933'],
  'vector database for embeddings': ['DEM364', 'BRK223'],
  'observability': ['BRK252', 'ODSP933'],
  'kubernetes': ['BRK222'],
  'serverless containers': ['BRK221'],
  'postgres': ['DEM364'],
  'vector db': ['DEM364', 'BRK223'],
  'rag retrieval': [],
  'responsible ai governance': [],
};

let pass = 0, fail = 0;
console.log('=== §1 query simulation (top 6) ===');
for (const [q, expect] of Object.entries(QUERIES)) {
  const res = search(q);
  const ids = res.map(r => r.id);
  const hitExpected = expect.every(e => ids.includes(e));
  const ok = expect.length === 0 ? res.length > 0 : hitExpected;
  if (ok) pass++; else fail++;
  console.log(`\nQ: "${q}"`);
  console.log('  top:', ids.join(', '));
  if (expect.length) console.log('  expect ⊆ top:', expect.join(', '), ok ? 'PASS ✓' : 'FAIL ✗');
  else console.log('  (any results) ', ok ? 'PASS ✓' : 'FAIL ✗');
}
console.log(`\n=== ${pass} pass, ${fail} fail ===`);
process.exit(fail ? 1 : 0);
