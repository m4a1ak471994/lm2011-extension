# LM (2011) replication diagnostic — v2 (post-appendix fixes)

Analysis sample: **83,422 firm-years** / **11,125 unique permnos**.
Paper targets: **50,115 firm-years / 8,341 firms**.

## Methodology fixes applied (LM 2011 Internet Appendix)
- 10-K and 10-K405 only (drop 10-KSB family)
- Strip exhibits (`<TYPE>EX-*`), keep only the primary 10-K body
- Strip tables where > 25% of nonblank chars are digits
- Replace `hyphen + LF` with `hyphen` before tokenizing
- N_Words = count of tokens IN the master dictionary
- Excess return = buy-and-hold compounded × 100 (in percent)
- Control: log(turnover), not raw turnover
- Fama-MacBeth quarterly with Newey-West (1 lag) SEs


## Table II — descriptive statistics (ours)

```
               variable     n    mean  median    std      min     max
                Fin-Neg 83422  1.5620  1.5653 0.5385   0.4232  2.9826
                Fin-Pos 83422  0.7202  0.7061 0.1978   0.2715  1.3308
Excess return [0,3] (%) 83422 -0.1871 -0.1825 6.2528 -21.6128 20.9435
              Size ($B) 83422  3.1883  0.4235 9.6376   0.0129 71.6897
         Book-to-market 83422  0.6232  0.5237 0.4568   0.0365  2.5181
 Turnover (pre, median) 83403  1.5147  0.9980 1.6075   0.0471  9.0132
1-yr pre-event FF alpha 83422  0.1119  0.0689 0.4488  -0.9834  1.8376
Institutional ownership 82475  0.5289  0.5452 0.3050   0.0045  1.1171
           NASDAQ dummy 83422  0.5825  1.0000 0.4931   0.0000  1.0000
```

## Table IV — Excess-return regressions, full 10-K (ours)

```
            label  ff48_dummies      sentiment_var    coef     se       t      p     n  n_quarters  adj_r2_avg
 col2_FinNeg_prop          True       fin_neg_prop -0.1245 0.0742 -1.6769 0.0936 82413         110      0.0377
col4_FinNeg_tfidf          True fin_neg_tfidf_full -0.0044 0.0025 -1.7964 0.0724 82413         110      0.0400
 col2_FinNeg_prop         False       fin_neg_prop -0.1801 0.0657 -2.7413 0.0061 82413         110      0.0194
col4_FinNeg_tfidf         False fin_neg_tfidf_full -0.0060 0.0023 -2.6144 0.0089 82413         110      0.0212
```

## Table V — Excess-return regressions, MD&A only (ours)

```
                label  ff48_dummies     sentiment_var    coef     se       t      p     n  n_quarters  adj_r2_avg
 col2_FinNeg_prop_MDA          True  fin_neg_prop_mda -0.1553 0.0456 -3.4089 0.0007 79656         110      0.0393
col4_FinNeg_tfidf_MDA          True fin_neg_tfidf_mda -0.0108 0.0028 -3.8078 0.0001 79656         110      0.0409
 col2_FinNeg_prop_MDA         False  fin_neg_prop_mda -0.1835 0.0454 -4.0464 0.0001 79656         110      0.0203
col4_FinNeg_tfidf_MDA         False fin_neg_tfidf_mda -0.0112 0.0030 -3.7258 0.0002 79656         110      0.0202
```

## LM (2011) reported reference values

Table IV col (2) Fin-Neg proportional: t ≈ -2.84, sign negative
Table IV col (4) Fin-Neg tf-idf:       t ≈ -5.27, larger magnitude than col (2)
Table V cols (2)/(4): same sign, larger |t| for tf-idf than proportional

_(LM signs are negative — higher negative tone predicts lower filing-period excess return.)_