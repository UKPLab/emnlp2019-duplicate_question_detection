# Neural Duplicate Question Detection without Labeled Training Data

This repository contains the data and code to reproduce the results of our paper: 
"Neural Duplicate Question Detection without Labeled Training Data".

Please use the following citation:

```
@article{rueckle:EMNLP:2019,
  title = {Neural Duplicate Question Detection without Labeled Training Data},
  author = {R{\"u}ckl{\'e}, Andreas and Moosavi, Nafise Sadat and Gurevych, Iryna},
  publisher = {Association for Computational Linguistics},
  booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP 2019)",
  pages = "1607--1617",
  year = "2019",
  address = "Hong Kong, China",
  url = "https://www.aclweb.org/anthology/D19-1171",
  doi = "10.18653/v1/D19-1171",
}
```

> **Abstract:** Supervised training of neural models to duplicate question detection in community Question Answering (cQA) requires large amounts of labeled question pairs, which are costly to obtain. To minimize this cost, recent works thus often used alternative methods, e.g., adversarial domain adaptation. In this work, we propose two novel methods: (1) the automatic generation of duplicate questions, and (2) weak supervision using the title and body of a question. We show that both can achieve improved performances even though they do not require any labeled data. We provide comprehensive comparisons of popular training strategies, which provides important insights on how to `best' train models in different scenarios. We show that our proposed approaches are more effective in many cases because they can utilize larger amounts of unlabeled data from cQA forums. Finally, we also show that our proposed approach for weak supervision with question title and body information is also an effective method to train cQA answer selection models without direct answer supervision.




Contact person: Andreas Rücklé

https://www.ukp.tu-darmstadt.de/

https://www.tu-darmstadt.de/


> This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication. 

# How to Train Models

Below we provide a brief instruction on how to train BERT models with WS-TB for arbitrary [StackExchange sites](https://https://stackexchange.com/sites).
Information to reproduce our experiments from the paper are provided further below in the section "Reproducing Experiments".

## Obtaining the Training Data

Our simplest approach to train models without labeled training data (i.e., without annotated duplicates) is to use the relation between a question title and its body. This means that we train a model to detect whether a given title and body belong to the same question (WS-TB). The trained model can then be used to find question duplicates or to retrieve answers for a given question (see our paper).

To create a training dataset for WS-TB, the first step is to obtain the data dump of a stackexchange platform, e.g., StackOverflow, Stackexchange Travel, etc. Data dumps are publicly available here: [https://archive.org/download/stackexchange](https://archive.org/download/stackexchange).

For a data dump we then create a training dataset by running:

```
python data-creation-wstb/create_train_data.py --se_path=<path/to/extracted/se-dump> --target_folder=<path/to/target/folder> --n_train_queries=5000 --n_dev_queries=500 --n_max_questions=10000 --pool_size=20 --pooling=<embedder>
```

Embedder can be one of ["use"](https://tfhub.dev/google/universal-sentence-encoder/3), ["p-means"](https://github.com/UKPLab/arxiv2018-xling-sentence-embeddings), or "none". In the paper, we used the devsets provided by other works (e.g., [adversarial domain adaptation](https://github.com/darsh10/qra_code)). There are also options to exclude certain question ids from training (e.g., because they are part of the evaluation split). Please run ```python create_train_data.py --help``` to see the documentation.

This is an enhanced variant of the code that we used in our paper (which now also produces dev splits with negative question bodies sampled using sentence embeddings and [FAISS](https://github.com/facebookresearch/faiss)). For the exact code that we used in the paper please see ("Reproducing Experiments").

The resulting dataset contains three files:

 * _questions.tsv.gz_: id,title,body (separated by \t) of all questions
 * _train.tsv.gz_: contains the ids of the questions that can be used for training (positive instances)
 * _dev.tsv.gz_: contains ids of the validation questions, and a list of negative questions (each id in the list is separated by whitespace)


## Training a Model

We can now use this dataset to train a new duplicate detection model.

```
python bert-training/run_experiment.py bert-training/configs/bert.yaml
```

please change the paths in the ```bert.yaml``` file accordingly. 
This configuration shows how the transfer performance to another task can be tested, e.g., answer selection. 
It can be easily extended with new datasets to test the performance of a trained model (by adding a new data-module).


# Reproducing our Experiments

We split this into several parts.

 1. [Data creation for DQG](./reproducing/readme-datacreation-dqg.md)
 2. [Data creation for WS-TB](./reproducing/readme-datacreation-ws-tb.md)
 3. [Model training and evaluation](./reproducing/readme-training.md)

We provide the data we used for model training on our [public fileserver](https://public.ukp.informatik.tu-darmstadt.de/emnlp2019-duplicate_question_detection/). 
