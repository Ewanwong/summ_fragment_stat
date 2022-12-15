# summ_fragment_stat

This is an implementation of three summarization characters: coverage, density and compression ratio which are intented to measure the extractiveness of summaries

Ideas from [Grusky et al. 2018](https://aclanthology.org/N18-1065.pdf)


How to use the metrics:
```
scorer = SummarizationCharacterScorer()
results = scorer.compute(articles, summaries)
```