# Does it matter *which* links we build?
### Transport, New Economic Geography and the North–South divide

**Huey Hares** · Paper 7: Regional Economics and Policy · Supervision 3 · November 2026

## The question

HS2 was designed to bring the North closer to London, while Northern Powerhouse Rail brings northern cities closer to each other. A faster link to a large core lets northern firms reach London, but it also lets London firms reach the North without locating there. This project asks whether it matters which links are built, and whether the wrong ones could widen the divide.

## Files

| File | What it is |
|---|---|
| `index.html` | The website. It's one self-contained file that you open in any browser, and it works offline. It has eight pages: puzzle, theory, model, parameters, simulator, evidence, answer and references. |
| `model.py` | A Python replication of the simulator. Run `python3 model.py` for the central results and the sensitivity table, or `python3 model.py <delta> <theta>` to choose your own values. Requires `numpy`. |
| `README.md` | This file. |

## The model

The model is a three-region version of Krugman's (1991) core–periphery model, following Fujita, Krugman & Venables (1999, ch. 5), with a congestion cost of the kind introduced by Brakman et al. (1996). The three regions are:

- London & the South East
- the North West (Manchester)
- Yorkshire & the Humber (Leeds)

```
Y_r = μ λ_r w_r + (1 − μ) φ_r                      income
G_r = [ Σ_s λ_s (w_s T_sr)^(1−σ) ]^(1/(1−σ))       price index
w_r = [ Σ_s Y_s T_rs^(1−σ) G_s^(σ−1) ]^(1/σ)       wage
ω_r = w_r · G_r^(−μ) · N_r^(−δ)                    real wage, with N_r = μλ_r + (1−μ)φ_r
T_rs = 1 + θ · (rail journey time in hours)        trade cost
λ_r ← λ_r + γ λ_r (ω_r − ω̄)                         migration
```

The short run is solved by damped fixed-point iteration (tolerance 1e-10). The long run iterates migration until shares change by less than 1e-9 per step. The tomahawk diagram uses two identical regions and scans λ for sign changes in ω₁ − ω₂.

## Parameters and sources

| Parameter | Value | Source / justification |
|---|---|---|
| φ, immobile shares | 58.4% / 23.9% / 17.7% | Mid-2025 population: London 9.1m + South East 9.7m; North West 7.7m; Yorkshire & Humber 5.7m (ONS, via ICAEW 2026) |
| λ₀, starting footloose shares | 72.6% / 18.3% / 9.1% | Financial & related professional services jobs, 2023: 1,182k / 298k / 149k (TheCityUK, 2025) |
| Journey times, today | London–Manchester 2h08; London–Leeds 2h13; Manchester–Leeds 55 min | HS2 Ltd (2014); DfT (2021); ITV News (2021) |
| Journey times, HS2-style | London–Manchester 1h11; London–Leeds 1h21 | DfT (2021); ITV News (2021) |
| Journey times, NPR-style | Manchester–Leeds 33 min | DfT (2021) |
| θ, trade cost per hour | 0.45 | Calibrated: the value that brings the "Today" equilibrium closest to the observed footloose shares |
| δ, congestion cost | 0.08 | Combes, Duranton & Gobillon (2019): urban cost elasticity ≈ 0.03 (100k city) to 0.08 (Paris-sized); London is comparable to Paris |
| σ, elasticity of substitution | 5 | Standard in FKV (1999); trade elasticity σ − 1 = 4, close to the typical ≈ 5 in Head & Mayer (2014) |
| μ, footloose share | 0.3 | Manufacturing 7.2% of UK jobs (CIIP, 2025) plus FRPS 7.5% (TheCityUK, 2025) plus other tradable services; satisfies the no-black-hole condition μ < (σ−1)/σ |
| γ, migration speed | 0.2 | Affects adjustment speed only |

**Model fit.** The model's "Today" equilibrium is 61.0 / 26.9 / 12.1, against the actual 72.6 / 18.3 / 9.1. About a sixth of London's lead is therefore not explained by market size and transport costs.

## Results (central calibration: δ = 0.08, θ = 0.45)

| Scenario | Footloose share (London & SE / NW / Yorkshire) | All jobs (London & SE / NW / Yorkshire) | Mobile real wage | Immobile real income (London & SE / NW / Yorkshire) |
|---|---|---|---|---|
| Today | 61.0 / 26.9 / 12.1 | 59.2 / 24.8 / 16.0 | — | — |
| HS2-style | 69.7 / 27.0 / 3.3 | 61.8 / 24.8 / 13.4 | +0.7% | +1.0 / +1.2 / +0.4% |
| NPR-style | 58.4 / 25.6 / 16.0 | 58.4 / 24.4 / 17.2 | +0.4% | −0.4 / +0.8 / +1.9% |
| Both | 58.0 / 41.1 / 0.9 | 58.3 / 29.1 / 12.7 | +1.0% | +0.3 / +2.0 / +3.1% |

**Sensitivity** (London & SE share of footloose industry):

| δ, θ | Today | HS2-style | NPR-style | Both |
|---|---|---|---|---|
| 0.06, 0.35 | 66% | 100% | 62% | 73% |
| 0.06, 0.45 | 64% | 92% | 61% | 69% |
| 0.06, 0.60 | 62% | 76% | 60% | 66% |
| 0.08, 0.35 | 61% | 66% | 57% | 46% |
| **0.08, 0.45** | **61%** | **70%** | **58%** | **58%** |
| 0.08, 0.60 | 60% | 67% | 59% | 61% |

**Robust findings**
- HS2-style links always raise London's share.
- NPR-style links always lower it.
- The combined effect depends on the parameters.

## Workflow and use of AI

I set the question and decided the argument and structure. I used an LLM (Claude) to help draft the code and text, and to find and check sources. I calibrated the model in Python and reimplemented it in JavaScript, then checked the two against each other, and both against the analytical break point.

## Sources

**Academic**
- Brakman, Garretsen & van Marrewijk (2019) *An Introduction to Geographical and Urban Economics: A Spiky World*, 3rd edn. CUP.
- Brakman, Garretsen, Gigengack, van Marrewijk & Wagenvoort (1996) 'Negative feedbacks in the economy and industrial location', *Journal of Regional Science*, 36(4), 631–652.
- Combes, Duranton & Gobillon (2019) 'The costs of agglomeration: house and land prices in French cities', *Review of Economic Studies*, 86(4), 1556–1589.
- Dixit & Stiglitz (1977) *AER*, 67(3), 297–308.
- Fujita, Krugman & Venables (1999) *The Spatial Economy*. MIT Press.
- Ghani, Goswami & Kerr (2016) *Economic Journal*, 126(591), 317–357.
- Head & Mayer (2014) 'Gravity equations: workhorse, toolkit, and cookbook', *Handbook of International Economics*, vol. 4, 131–195.
- Helpman (1998) 'The size of regions', in *Topics in Public Economics*. CUP.
- Krugman (1991) *JPE*, 99(3), 483–499.
- Martin (1999) *Cambridge Journal of Economics*, 23(1), 65–91.
- Matas, Raymond & Roig (2015) *Regional Studies*, 49(7), 1236–1254.
- Myrdal (1957) *Economic Theory and Under-Developed Regions*. Duckworth.
- Peri (2005) *REStat*, 87(2), 308–322.
- Samuelson (1954) *Economic Journal*, 64(254), 264–289.
- Zheng, Long, Chang & Ye (2019) *Transport Policy*, 81, 230–241.

**Data and reports**
- CIIP (2025) *UK Innovation Report 2025*: https://www.ciip.group.cam.ac.uk/innovation/executive-summary-2025/
- DfT (2021) Integrated Rail Plan announcement: https://gov.uk/government/news/integrated-rail-plan-biggest-ever-public-investment-in-britains-rail-network-will-deliver-faster-more-frequent-and-more-reliable-journeys-across-no
- HS2 Ltd (2014) *Rebalancing Britain*: https://assets.publishing.service.gov.uk/media/5a7ebac940f0b6230268b2ba/Rebalancing_Britain_-_From_HS2_towards_a_national_transport_strategy.pdf
- House of Commons Library, *What next for HS2?*: https://commonslibrary.parliament.uk/what-next-for-hs2
- ICAEW (2026) Chart of the week: England and Wales population: https://www.icaew.com/insights/viewpoints-on-the-news/2026/jul-2026/chart-of-the-week-england-and-wales-population
- ITV News (2021) Northern rail plan journey times: https://itv.com/news/2021-11-18/northern-rail-plan-cuts-how-journeys-will-change-compared-to-what-was-promised
- NAO (2026) *Northern Powerhouse Rail*: https://www.nao.org.uk/reports/northern-powerhouse-rail/
- ONS (2025) *Regional and subregional labour productivity, UK: 2023*: https://www.ons.gov.uk/economy/economicoutputandproductivity/productivitymeasures/bulletins/regionalandsubregionallabourproductivityuk/2023
- TheCityUK (2025) *Enabling growth across the UK 2025*: https://www.thecityuk.com/media/3h5gjei2/enabling-growth-across-the-uk-2025.pdf
- Map outline: Natural Earth 1:10m (public domain), via the `world-atlas` npm package.

## Optional: GitHub Pages

1. Put `index.html` in your branch.
2. In the fork, go to **Settings → Pages**, choose **Deploy from a branch**, and pick your branch.
3. After a minute or two, the site appears at `https://<username>.github.io/<repo>/`.
