import numpy as np
from multiprocessing import Pool

class SummarizationCharacterScorer:
    """
    This is an implementation of three summarization characters: coverage, density and compression ratio which are intented to measure the extractiveness of summaries
    Ideas from Grusky et al. 2018
    """
    def __init__(self, num_process=5):
        self.num_process = num_process


    def _compute(self, article: str, summary:str)-> tuple:
        
        if len(summary.split(' ')) == 0:  # in case some summaries is empty
            return 0.0, 0.0, 0.0
        shared_sequence = self._get_extractive_segments(article, summary)
        coverage = np.sum([len(sequence.split(' ')) for sequence in shared_sequence]) / len(summary.split(' '))
        density = np.sum([len(sequence.split(' ')) ** 2 for sequence in shared_sequence]) / len(summary.split(' '))
        compression_ratio = len(article.split(' ')) / len(summary.split(' '))
        # print(coverage, density, compression_ratio, flush=True)
        return coverage, density, compression_ratio

    def _get_extractive_segments(self, article: str, summary: str)-> list:
        """
        greedily identify these extractive fragments of an article-summary pair
        algorithm taken from Grusky et al. 2018
        """
        article_words = article.split(' ')
        summary_words = summary.split(' ')
        shared_sequences = []
        i = 0
        j = 0
        while i < len(summary_words):
            shared_tokens = []
            
            while j < len(article_words):
                if summary_words[i] == article_words[j]:
                    i_end, j_end = i, j
                    while i_end < len(summary_words) and j_end < len(article_words) and summary_words[i_end] == article_words[j_end]:
                       
                        i_end, j_end = i_end + 1, j_end + 1
                   
                    if len(shared_tokens) < i_end - i:
                        shared_tokens = summary_words[i:i_end]
                    j = j_end
                else:
                    j = j + 1
           
            i, j = i + np.max([len(shared_tokens), 1]), 0
            if len(shared_tokens) > 0:
                shared_sequences.append(' '.join(shared_tokens))
       
        return shared_sequences

    def compute(self, articles: list, summaries:list) -> dict:
        coverage_list = []
        density_list = []
        compression_ratio_list = []
        with Pool(processes=self.num_process) as pool:

            res = pool.starmap(self._compute, zip(articles, summaries))
        for coverage, density, compression_ratio in res:
            
            coverage_list.append(coverage)
            density_list.append(density)
            compression_ratio_list.append(compression_ratio)
        return {"coverage":np.mean(coverage_list), "density":np.mean(density), "compression_ratio":np.mean(compression_ratio_list)}

if __name__ == "__main__":
    

    from datasets import list_datasets, load_dataset
    import numpy as np
    
    booksum = load_dataset('kmfoda/booksum')
    print(booksum)

    articles = booksum['train']['chapter'] + booksum['validation']['chapter'] + booksum['test']['chapter']
    summaries = booksum['train']['summary_text'] + booksum['validation']['summary_text'] + booksum['test']['summary_text']

    SC = SummarizationCharacterScorer(30)
    

    print(SC.compute(articles, summaries))