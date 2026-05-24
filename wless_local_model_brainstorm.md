# WasteLess — Estensione Journal: Modello QN Locale per Funzione

> Documento di sintesi della sessione di brainstorming. Va letto da capo; chiude
> con la lista di decisioni da prendere prima di scrivere codice o teoremi.

---

## 1. Contesto

- WasteLess (ASE 2024, replication package in questo repo) propone un *Optimal
  Resource Provisioner* per applicazioni serverless di seconda generazione.
- La pipeline attuale dipende dalla costruzione di un **modello LQN globale**
  dell'applicazione (`Acmeair_variants/Acmeair_*/lqnmodel_*.lqn.py`).
- L'estensione del lavoro a journal ha ricevuto **2 reject**. L'ipotesi più
  plausibile sui motivi: dipendenza da un modello LQN ricostruito a mano,
  parametri (visit ratios, demands, NT, probChoices) difficili da stimare in
  produzione, fragilità del provisioning quando uno qualunque di questi
  parametri è errato.
- Obiettivo della nuova revisione: dare a WasteLess un **contributo metodologico
  nuovo**, rendendolo *meno dipendente* dalla stima di un modello LQN completo,
  e più dipendente da:
  - considerazioni generali di teoria delle code, oppure
  - un modello di funzione **locale**,
  assumendo che siano disponibili **traccie OTEL** e/o **metriche spanmetrics da
  Prometheus** per ogni funzione.

---

## 2. Cosa fa WasteLess oggi

Catena attuale (file di riferimento tra parentesi):

1. Modello LQN dell'app intera — ogni funzione è un Task con un Entry e
   Activities (chiamate sincrone). Le dipendenze tra funzioni sono cablate nel
   grafo (`lqnmodel_X.lqn.py`).
2. Stima dei service demand per funzione (`estimeDemands.py`): da
   `logs/<funzione>.csv` calcola `demand = RT_locale − Σ call_count · RT_chiamato`.
   Presuppone di conoscere il grafo di chiamate.
3. Trasformazione LQN → MPP / ODE fluida (`MPP4Lqn/Lqn2MPP/Lqn2MPP.py`): genera
   `lqnODE.m` con `min(X, NC)`, `min(X, NT)` per modellare concorrenze e thread
   pool.
4. Ottimizzazione (`main_eval.m`): per `u = 1..100` utenti risolve l'ODE
   globale, raccoglie populazione per funzione, calcola
   `NTopt = ceil(NT_lqn / NCopt)` → `optSol.csv`.
5. Baselines: NoConc, GCR (concurrency 80), ProPack (curva exp RT‑vs‑concurrency
   per‑funzione).

Critica metodologica: tutto richiede *grafo globale* + *parametri LQN globali*.

---

## 3. Direzione nuova: niente LQN globale, modello *locale* per funzione

L'opzione vincente tra quelle discusse: ogni funzione si auto‑provisiona usando
**solo le proprie spanmetrics locali**. Il punto sottile è che il tasso
osservato `λ_f` su Prometheus *già contiene* l'effetto a monte (è il rate
effettivo che arriva alla funzione f, qualunque sia la catena che l'ha
generato). Quindi non c'è bisogno di sapere chi chiama f, né con che
probabilità, né come si propagano i burst — Prometheus lo dice già.

Il contributo metodologico, in una frase:

> *WasteLess passa da provisioning model‑based globale (LQN) a provisioning
> observation‑based locale. Le interazioni tra funzioni non vengono modellate
> ma osservate: ogni funzione ottimizza la propria concorrenza/cores/memoria
> usando solo λ_f e la distribuzione degli span‑metrics di RT_f.*

Differenza rispetto a ProPack: ProPack fitta una curva esponenziale di RT vs
concorrenza e non fa queueing theory. Noi facciamo un modello QN locale onesto.

---

## 4. L'insight modellistico chiave

L'LQN serviva per **calcolare** il tempo di attesa downstream. Lo possiamo
invece **osservare**: se separiamo gli span con `kind=server` (durata totale
della funzione f) dagli span con `kind=client` (chiamate uscenti da f),
Prometheus ci dà direttamente l'istogramma di:

- `T_f^total` = durata server‑span di f (CPU + downstream + sync‑wait)
- `T_f^down`  = somma delle durate client‑span emessi da f
- `T_f^self`  = `T_f^total − T_f^down` ≈ CPU + scheduler interno di f

**Conseguenza:** il downstream diventa un I/O delay osservato, non un
sotto‑modello da risolvere. È questo che rompe la dipendenza dall'LQN globale.

---

## 5. Architettura del modello locale (due piani)

Nell'LQN un task con multiplicity NT e chiamate sincrone è modellabile in
isolamento come una rete di code chiusa (Method of Layers, Rolia‑Sevcik 1995).
La novità non è inventare quel sotto‑modello — esiste — ma **non doverne
stimare i parametri da un grafo globale**: te li dà Prometheus.

Il modello locale per la funzione f vive su due piani.

```
┌────────── piano cluster (open) ──────────┐
│  arrivi λ_f → coda d'ammissione → c_f    │
│             istanze in parallelo          │
└──────────────────┬───────────────────────┘
                   │
       ┌───────────▼──────────┐
       │  piano istanza        │
       │  (closed CQN, k_f)    │
       │  ┌──CPU───┐ ┌──I/O──┐ │
       │  │ C_f    │ │ delay │ │
       │  │ cores  │ │ D_io  │ │
       │  │ D_cpu  │ │  ∞-s   │ │
       │  └────────┘ └───────┘ │
       └───────────────────────┘
```

- Piano istanza: closed‑CQN con k_f clienti che ciclano tra una stazione CPU
  (multi‑server C_f core, demand D_cpu) e un delay center (demand D_io).
  Risolvibile in O(k_f) con MVA.
- Piano cluster: c_f istanze viste come macro‑server **load‑dependent**, da
  gestire con il teorema di decomposizione di Chandy‑Herzog‑Woo (1975) →
  M/M/c_f‑like con rate per server = `X^inst(k_f, C_f)`.

Variabili decisionali per ogni f: `(c_f, k_f, C_f, M_f)` =
(# istanze, concorrenza per istanza, cores per istanza, memoria per istanza).

---

## 6. Tre varianti del modello

### V1 — Sakasegawa con servizio inflato (closed‑form)

- Per‑istanza, niente CQN: collasso CPU vs I/O in un servizio effettivo
  `S_eff = (k_f · D_cpu)/C_f · 𝟙[k_f > C_f] + D_io`.
- Cluster: M/G/c_f con `μ = k_f / S_eff`, formula Allen‑Cunneen per E[W].
- `E[R_f] = R^inst + E[W_gw]` in forma chiusa.
- **Pro:** tutti i teoremi diventano espliciti; il paper ha equazioni che si
  leggono; nessun solver.
- **Contro:** sotto‑modella la sovrapposizione CPU/I/O quando k_f ≈ C_f
  (zona di mezzo); tende a sovrastimare R per workload misti.

### V2 — MVA per‑istanza + Chandy‑Herzog‑Woo al cluster (raccomandato)

- Per‑istanza: MVA esatto (product‑form) o Bard‑Schweitzer (altrimenti) →
  restituisce `X^inst(k, C)` e `R^inst(k, C)`.
- Cluster: Erlang‑C / M/M/c_f con server‑rate = `X^inst(k, C)`.
- **Pro:** fedele al fenomeno fisico; cattura la finestra in cui aumentare k_f
  *aiuta* perché copre i tempi I/O; approssimazione ben caratterizzata in
  letteratura.
- **Contro:** non più closed‑form; teoremi si dimostrano via *bounds*
  (balanced job bounds di Lazowska‑Zahorjan).

### V3 — Markov‑modulated fluid model

- Tieni il piano istanza come PFQN ma rendi `λ_f, D_io, D_cpu` modulati da uno
  stato discreto (burst / regime / idle) stimato via HMM o change‑point su
  Prometheus.
- **Pro:** robusto a workload non‑stazionari, apre la porta a SLO sui
  percentili.
- **Contro:** complica la dimostrabilità → da tenere come *future work*.

**Decisione di lavoro proposta:** V1 come main result (teoremi puliti), V2 come
refinement con validation sperimentale in appendix, V3 in conclusione.

---

## 7. Calibrazione esplicita da spanmetrics

### 7.1. Stime base (low‑load identification)

Per ogni funzione f, da Prometheus:

```
λ_f         = rate(spanmetrics_calls_total{service=f, kind=SERVER}[1m])

E[T^srv]    = histogram_avg(spanmetrics_duration_seconds_*{service=f, kind=SERVER})
Var[T^srv]  = histogram_var(...)                   # ricostruita dai bucket
SCV_s       = Var / E[T^srv]^2

per ogni target g chiamato da f:
  v_{f→g}   = rate(client{service=f, target=g}) / λ_f   # fan-out medio
  E[C_{f→g}]= histogram_avg(client{service=f, target=g})

D̂_io  = Σ_g v_{f→g} · E[C_{f→g}]                   # ipotesi: chiamate seriali
D̂_cpu = E[T^srv] |_low_load − D̂_io |_low_load      # self-time a basso carico
```

Per "low load" intendi finestre temporali in cui
`ρ̂ = λ_f · E[T^srv] / (c_f · k_f) < 0.2`. Lì le code sono trascurabili e
`E[T^srv] ≈ D_cpu + D_io`. È la classica Service Demand Law (Denning‑Buzen).

### 7.2. Identificazione robusta (con node‑exporter, opzionale)

Se hai `node_cpu_seconds_total` o `container_cpu_usage_seconds_total`:

```
D̂_cpu = (U_cpu · C_f) / λ_f      (per istanza)
D̂_io  = E[T^srv] − D̂_cpu
```

Questo rende lo stimatore identificabile in *qualunque* regime di carico, non
solo a basso load.

### 7.3. Note non banali

1. **Serial vs parallel fan‑out.** Senza traccie non sai se i client span di f
   sono in serie o in parallelo. Per la maggior parte dei pattern await/RPC è
   serie → somma corretta. Se vuoi essere conservativo: la somma è un upper
   bound della componente bloccante reale → il provisioning risulta
   cautelativo, non aggressivo (difendibile in paper).

2. **m_req (memoria per richiesta).** Da
   `container_memory_usage_bytes / k_f_corrente` in finestre saturate, oppure
   stima statica dal manifest.

3. **SCV degli arrivi.** Senza inter‑arrivi raw, proxy via indice di
   dispersione: `var(count_per_window) / mean(count_per_window)`. Per Poisson
   vale 1.

---

## 8. Servono le traccie OTEL?

**Per il modello base (V1/V2): NO.** Bastano spanmetrics con tag `span.kind`.

Le traccie servono solo per:

1. Confermare la struttura serial vs parallel dei fan‑out.
2. Validare la decomposizione `T_total = T_self + Σ T_client` per‑richiesta.
3. Sanity check / ground truth nella sezione di validation.
4. (Opzionale) stimare uno scaling factor α per `D_cpu(C_f)` se non assumi
   single‑thread per request.

Posizionamento in paper: **il metodo richiede solo spanmetrics**; le traccie
sono usate offline per validation. È un vantaggio operativo forte: la
metodologia funziona in deployment con tracing campionato (1%) o assente.

---

## 9. Teoremi target

Con V1 + input `(λ_f, D_cpu, D_io, SCV)` e decision vars `(c_f, k_f, C_f, M_f)`:

**T1 — Stabilità.**
Il sistema è stabile sse
`λ_f < c_f · μ(k_f, C_f)`
con `μ(k_f, C_f) = min(k_f / (D_cpu + D_io), C_f / D_cpu)`.

**T2 — Concorrenza ottima per istanza (bottleneck balancing).**
Il valore di k che massimizza la throughput per istanza dato C è
```
k*(C) = ceil( C · (1 + D_io / D_cpu) )
```
Si ottiene eguagliando i due bound della CQN. È già un risultato pubblicabile e
interpretabile: *la concorrenza ottimale per istanza è il numero di core
moltiplicato per (1 + rapporto I/O / CPU)*.

**T3 — Monotonicità del costo nel SLO.**
Il costo ottimo `J*(τ)` è non‑crescente in τ e convesso a tratti in `1/τ`.

**T4 — Min‑cost configuration (forma chiusa V1).**
Dato `ρ* = ρ*(τ, SCV)` derivato da Allen‑Cunneen invertito:
```
c_f* = ceil( λ_f · (D_cpu + D_io) / (k_f* · ρ*) )
k_f* = k*(C_f*)
M_f* = k_f* · m_req
C_f* = argmin_{C ∈ grid} cost(C) · c_f*(C)
```
Risolvibile in `O(|grid_C|)` step (typically ≤ 6 valori discreti). Niente solver.

**T5 — Robustezza all'errore di calibrazione.**
Se `|D̂_io − D_io| ≤ ε`, allora
`|E[R̂] − E[R]| ≤ K(ρ) · ε`
con K(ρ) esplicito. Dimostra che il metodo è robusto agli errori di stima dei
demand.

**T6 — Memory‑constrained regime.**
Se `M_f / m_req < k*(C_f)`, l'istanza è memory‑bound e il min‑cost richiede
```
c_f = ceil( λ_f · (D_cpu + D_io) / ((M_f / m_req) · ρ*) )
```
Caso operativo molto comune: la memoria diventa il driver del costo.

**Verdetto:** T2 e T4 da soli giustificano un paper journal. Sostituiscono
un'ottimizzazione su un modello LQN globale con due formule chiuse per
funzione, parametrizzate da quantità misurabili in produzione.

---

## 10. Cosa NON è ancora deciso

Ci sono cinque scelte da fissare prima di scrivere codice o lemmi formali:

1. **V1 vs V2 come main result.**
   - V1 → leggibilità massima, teoremi closed‑form.
   - V2 → fedeltà fisica, teoremi via bounds.
   - Default proposto: V1 main + V2 refinement.

2. **Calibrazione: spanmetrics‑only oppure include `cpu_usage_seconds`.**
   - Solo spanmetrics: setup operativo minimale, funziona solo in regime con
     periodi di basso carico identificabili.
   - + node‑exporter: robusto a workload sempre carichi, ma serve una metrica
     in più.

3. **Disciplina di servizio per‑istanza nel modello.**
   - PS: più realistica per container Linux, rompe product‑form a multi‑server.
   - FCFS multi‑server: product‑form (MVA esatto), meno fedele al container.
   - Default proposto: dichiarare FCFS nel modello, mostrare empiricamente che
     la differenza vs PS è < 10%.

4. **Cosa fare con le traccie OTEL.**
   - Ignorate del tutto (deployment più leggero).
   - Usate solo per validation in sezione experiments.
   - Default proposto: la seconda — rafforza il paper, non appesantisce il
     metodo.

5. **Scope del primo paper journal.**
   - Solo SLO sulla media → fattibile, T1–T6 bastano.
   - SLO sui percentili (P95/P99) → richiede V3 o concentration bounds sugli
     istogrammi; alza il livello ma raddoppia il lavoro.
   - Default proposto: media nel primo paper, percentili come follow‑up.

---

## 11. Prossimi passi (quando ripartiamo)

In ordine:

1. Fissare le 5 decisioni di §10.
2. Scrivere lo *scheletro formale*: definizioni (sistema, decisione, SLO),
   statement dei teoremi T1–T6, ipotesi esplicite.
3. Scrivere un modulo Python `wless_local/` con:
   - `prom_calibrator.py` → estrae `(λ_f, D_cpu, D_io, SCV)` da una query
     Prometheus (PromQL specificato).
   - `local_model.py` → V1 (closed‑form) e V2 (MVA + Erlang‑C).
   - `provisioner.py` → risolve l'optimization di T4 su un grid di
     `(C_f, k_f, c_f, M_f)`.
4. Validation sperimentale sulle 30 varianti Acmeair già nel repo: confrontare
   `optSol.csv` (LQN globale) con la nuova soluzione locale → mostrare che la
   nuova è competitiva (entro X%) ma con metodo molto più semplice.
5. Sezione "ablation": run su workload non‑stazionari per giustificare V3.

---

## 12. Quick‑reference: simboli usati

| Simbolo | Significato |
|---|---|
| `f` | funzione (servizio) |
| `λ_f` | arrival rate alla funzione f |
| `c_f` | numero di istanze attive di f (decision var) |
| `k_f` | concorrenza per istanza (decision var, NT in LQN) |
| `C_f` | cores per istanza (decision var) |
| `M_f` | memoria per istanza (decision var) |
| `m_req` | memoria per request concorrente |
| `D_cpu` | demand CPU per request (su 1 core) |
| `D_io` | tempo medio bloccato su downstream per request |
| `S_eff` | servizio effettivo per‑istanza nel modello V1 |
| `X^inst(k,C)` | throughput di una istanza saturata, dalla CQN per‑istanza |
| `R^inst(k,C)` | mean residence time inside the instance, dalla CQN |
| `E[W_gw]` | mean queueing wait al gateway (cluster‑level) |
| `E[R_f]` | mean response time end‑to‑end di f |
| `τ_f` | target SLO sulla mean response time di f |
| `ρ*` | max utilization compatibile con SLO via Allen‑Cunneen invertito |
| `SCV_a / SCV_s` | squared coefficient of variation di arrivi / servizio |

---

Documento generato in sessione di brainstorming. Da consultare prima di
riprendere il lavoro per ricostruire lo stato del ragionamento.
