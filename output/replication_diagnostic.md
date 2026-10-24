# Methodology diagnostic — extended sample (1994–2024)

Analysis sample: **96,331 firm-years** / **11,968 unique permnos**.
LM (2011) in-sample reference: 50,115 firm-years / 8,341 firms.

## Methodology fixes applied (LM 2011 Internet Appendix)
- 10-K and 10-K405 only (drop 10-KSB family)
- Strip exhibits (`<TYPE>EX-*`), keep only the primary 10-K body
- Strip tables where > 25% of nonblank chars are digits
- Replace `hyphen + LF` with `hyphen` before tokenizing
- N_Words = count of tokens IN the master dictionary
- Excess return = buy-and-hold compounded × 100 (in percent)
- Control: log(turnover), not raw turnover
- Fama-MacBeth quarterly with Newey-West (1 lag) SEs


## Table II — descriptive statistics (mine)

```
               variable     n    mean  median     std      min     max
                Fin-Neg 96331  1.6398  1.6494  0.5590   0.4374  3.0448
                Fin-Pos 96331  0.7318  0.7175  0.1970   0.2824  1.3281
Excess return [0,3] (%) 96331 -0.2060 -0.2006  6.5713 -22.5267 22.4913
              Size ($B) 96331  4.1270  0.5114 12.6704   0.0133 94.4409
         Book-to-market 96331  0.6152  0.5128  0.4595   0.0315  2.5232
 Turnover (pre, median) 96312  1.6359  1.1111  1.7587   0.0503 10.5462
1-yr pre-event FF alpha 96331  0.1047  0.0631  0.4460  -0.9943  1.8197
Institutional ownership 95232  0.5543  0.5850  0.3067   0.0053  1.1183
           NASDAQ dummy 96331  0.5810  1.0000  0.4934   0.0000  1.0000
```

## Table IV — Excess-return regressions, full 10-K (mine)

```
            label  ff48_dummies      sentiment_var    coef     se       t      p     n  n_quarters  adj_r2_avg
 col2_FinNeg_prop          True       fin_neg_prop -0.1262 0.0680 -1.8573 0.0633 95210         123      0.0371
col4_FinNeg_tfidf          True fin_neg_tfidf_full -0.0046 0.0025 -1.8253 0.0680 95210         123      0.0391
 col2_FinNeg_prop         False       fin_neg_prop -0.1946 0.0641 -3.0355 0.0024 95210         123      0.0168
col4_FinNeg_tfidf         False fin_neg_tfidf_full -0.0066 0.0023 -2.8654 0.0042 95210         123      0.0179
```

## Table V — Excess-return regressions, MD&A only (mine)

```
                label  ff48_dummies     sentiment_var    coef     se       t      p     n  n_quarters  adj_r2_avg
 col2_FinNeg_prop_MDA          True  fin_neg_prop_mda -0.1159 0.0470 -2.4635 0.0138 92369         123      0.0374
col4_FinNeg_tfidf_MDA          True fin_neg_tfidf_mda -0.0108 0.0027 -3.9724 0.0001 92369         123      0.0376
 col2_FinNeg_prop_MDA         False  fin_neg_prop_mda -0.1248 0.0487 -2.5634 0.0104 92369         123      0.0179
col4_FinNeg_tfidf_MDA         False fin_neg_tfidf_mda -0.0113 0.0029 -3.9461 0.0001 92369         123      0.0175
```

## LM (2011) reported reference values

Table IV col (2) Fin-Neg proportional: t ≈ -2.84, sign negative
Table IV col (4) Fin-Neg tf-idf:       t ≈ -5.27, larger magnitude than col (2)
Table V cols (2)/(4): same sign, larger |t| for tf-idf than proportional

_(LM signs are negative — higher negative tone predicts lower filing-period excess return.)_