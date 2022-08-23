<p align="center">
<a><img width="400" alt="OxAPI Logo" src="https://dr96isfyftsoo.cloudfront.net/logo-transparent.png"></a>
</p>
<br/>
<p align="center">
<a href="https://colab.research.google.com/drive/1pDJnMI5KNBY3QDrsFls0DYbulj3GgQf1?usp=sharing"><img alt="Colab" src="https://img.shields.io/badge/colab-notebook-yellow"></a>
<a href="https://img.shields.io/uptimerobot/ratio/m792235727-a2ab4cd1ffe3d2e025e777b9"><img alt="Uptime" src="https://img.shields.io/uptimerobot/ratio/m792235727-a2ab4cd1ffe3d2e025e777b9"></a>
<a href="https://img.shields.io/website?url=https%3A%2F%2Foxapi.ai"><img alt="Website Up" src="https://img.shields.io/website?url=https%3A%2F%2Foxapi.ai"></a>
</p>
<p align="center">
<a href="https://github-public-storage.s3.eu-central-1.amazonaws.com/oxapi-python-coverage.svg"><img alt="Coverage" src="https://github-public-storage.s3.eu-central-1.amazonaws.com/oxapi-python-coverage.svg"></a>
<a href="https://github-public-storage.s3.eu-central-1.amazonaws.com/oxapi-python-pylint.svg"><img alt="PyLint" src="https://github-public-storage.s3.eu-central-1.amazonaws.com/oxapi-python-pylint.svg"></a>
<a href="https://img.shields.io/pypi/v/oxapi"><img alt="PyPi" src="https://img.shields.io/pypi/v/oxapi"></a>
<a href="https://img.shields.io/github/issues/Oxolo/oxapi-python"><img alt="Issues" src="https://img.shields.io/github/issues/Oxolo/oxapi-python"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

This Python library provides simplified access to the OxAPI from applications written in Python.

```python
import oxapi
oxapi.api_key = "sk-..."

encoding = oxapi.Encoding.run(
    model="all-mpnet-base-v2",
    texts=["Hello", "How are you?"]
)
```

The OxAPI offers a variety of models from natural language processing for your convenience.

We provide highly optimized and production-ready endpoints to serve artificial intelligence for
your deep tech applications.

Hosting and running such models is very difficult and time-consuming. At OxAPI, you get all the
latest NLP technology for building applications without any of the inconveniences that come with
it.

We provide open-source and proprietary models with transparent and fair pricing as
high-performance endpoints. Each model is documented in detail and offers an easy-to-use and
understandable API. We take care of hosting, hardware selection, and optimization for you.
The results are some of the fastest models on the market. OxAPI, from developers, for
developers.

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install -U oxapi
```

Install from source with:

```sh
python setup.py install
```

## Documentation

For the full documentation of the API itself, please visit the [OxAPI documentation](https://oxapi.ai/documentation).

If you want to check the documentation of this package, visit the [docs](http://github-oxapi-python-doc.s3-website.eu-central-1.amazonaws.com)

Additionally, you find an interative tutorial on Colab: <a href="https://colab.research.google.com/drive/1pDJnMI5KNBY3QDrsFls0DYbulj3GgQf1?usp=sharing"><img alt="Colab" src="https://img.shields.io/badge/colab-notebook-yellow"></a>

## Audience

This package is intended for anyone working with natural language processing.

- You need a reliable and scalable API to build your application on
- You need the latest models at your fingertips
- You don't need thousands of models, only a few really good ones
- You need results blazingly fast 🚀
- You don't want to bother creating and maintaining GPU clusters
- You want someone else to take care of all the dirtywork
- You have one or more of the following usecases:
    - Natural Language Understanding
        - Named Entity Recognition
        - Emotion Classification
        - Content Filtering
        - Spell Checking
        - Intention Classifcation
        - Encoding
        - Topic Classification
    - Natural Language Generation
        - Paraphrasing
        - Spell-checking
        - Code Generation
        - Summarization
        - Product Description
        - Ad-Generation
        - And many more ... 

The list of use-cases will be expanded upon in the future. We will expand our offer with models from
computer vision and audio eventually in the coming weeks and months. Stay tuned!

## Reliability

We see reliability and speed as our core assets. Visit our [statuspage](https://status.oxapi.ai) on recent updates and healthchecks.

## FAQ

If you have any questions, please check the [FAQ](https://oxapi.ai/pricing) section of our hompage.

## Usage

### API key

The library needs to be configured with your account's secret key. Either set it as the `OXAPI_KEY` environment variable before using the library:

```bash
export OXAPI_KEY='sk-...'
```

Or set `oxapi.api_key` to its value:

```python
import oxapi
oxapi.api_key = "sk-..."
```

### Completion

```python
from oxapi import Completion

# Performing API call

completion = Completion.run(
    model="gpt-neo-2-7b", 
    prompt="My name is Tim.\nSentiment: Neutral\nIt is such a lovely day.\nSentiment: Positive\nAlthough I am in a bad mood\nSentiment:",
    max_length=2, 
    do_sample=False, 
    eos_words=["\n"]
)

# Fetching result

res = completion.format_result(result_format="str")

print(completion.result)
```

Output:
```
{'results': ['Neutral\n']}
```

### Classification

```python
from oxapi import Classification

# Performing API call

classification = Classification.run(
    model="dialog-content-filter", 
    texts=["I want to kill myself.", "I want to kill myself.<sep>You should not do that!", "I want to kill myself.<sep>Do it!"]
)

# Fetching result

res = classification.format_result(result_format="pd")

print(res)
```

Output:
```
                                                text label          confidence_score
0                             I want to kill myself.  unsafe      0.9772329101403038
1  I want to kill myself.<sep>You should not do t...  safe        0.9736578740966625
2                  I want to kill myself.<sep>Do it!  unsafe      0.9266854663680397
```

### Encoding

```python
from oxapi import Encoding

# Performing API call

encoding = Encoding.run(
    model="all-mpnet-base-v2",
    texts=["Hello", "How are you?"]
)

# Fetching result

print(encoding.result)
```

Output:
```
{'results': [[
   -0.017791748046875,
   -2.980232238769531e-07,
   -0.022003173828125,
   0.02105712890625,
   -0.06695556640625,
   -0.02435302734375,
   -0.0174713134765625,
   ...
    -0.0011529922485351562]]
}
```

### Transformation

```python
from oxapi import Transformation

# Performing API call

transformation = Transformation.run(
    model="punctuation-imputation", 
    texts=["hello my name is tim i just came back from nyc how are you doing"]
)

# Fetching result

print(transformation.result)
```

Output:
```
{'results': ['Hello my name is Tim. I just came back from NYC. How are you doing?']}
```

### Pipeline

```python
from oxapi import Pipeline

# Performing API call

pipeline = Pipeline.run(
    model="en-core-web-lg",
    texts=["Hi there!"]
)

# Fetching result

print(pipeline.result)
```

Output:
```
{'results': [{'text': 'Hi there!',
   'ents': [],
   'sents': [{'start': 0, 'end': 9}],
   'tokens': [{'id': 0,
     'start': 0,
     'end': 2,
     'tag': 'UH',
     'pos': 'INTJ',
     'morph': '',
     'lemma': 'hi',
     'dep': 'ROOT',
     'head': 0},
    {'id': 1,
     'start': 3,
     'end': 8,
     'tag': 'RB',
     'pos': 'ADV',
     'morph': 'PronType=Dem',
     'lemma': 'there',
     'dep': 'advmod',
     'head': 0},
    {'id': 2,
     'start': 8,
     'end': 9,
     'tag': '.',
     'pos': 'PUNCT',
     'morph': 'PunctType=Peri',
     'lemma': '!',
     'dep': 'punct',
     'head': 0}],
   'sents_text': ['Hi there!']}]
}
```

### Asynchronous call pipeline

With ```oxapi-python``` package is possible to make calls to OxAPI in parallel. The ```AsyncCallPipe``` class takes as input a list of API calls each set through the ```prepare``` function to be executed by the pipeline.

```python
from oxapi.async import AsyncCallPipe

from oxapi import Completion
from oxapi import Classification
from oxapi import Transformation
from oxapi import Pipeline

# Set up API calls

cl = Classification.prepare(model="dialog-content-filter", texts=["I want to kill myself."])
cm = Completion.prepare(model="gpt-neo-2-7b", prompt="Hello there, ", max_length=25, do_sample=True, eos_words=["\n"])
tr = Transformation.prepare(model="punctuation-imputation", texts=["hello my name is tim i just came back from nyc how are you doing"])
pl = Pipeline.prepare(model="en-core-web-lg", texts=["Hi there!"])

# Building and running the asynchronous pipe

asy = AsyncCallPipe([cl, cm, tr, pl])
res = asy.run()

# Fetching the result of the first call in the list

print(res[0].format_result(result_format="pd"))
```

Output:
```
                                                text label          confidence_score
0                             I want to kill myself.  unsafe      0.9772329101403038
```

It is possible to add API calls to the asynchronous pipe even after its instantiation though the ```add``` function. There's also the ```flush``` function to clear the list in the pipe.

```python
from oxapi.async import AsyncCallPipe
from oxapi import Encoding

# Instantiate an empty asynchornous pipe

asy = AsyncCallPipe()

# Set up API call and add it to the pipe

en = Encoding.prepare(model="all-mpnet-base-v2", texts=["Hello", "How are you?"])
asy.add(en)

# running the asynchronous pipe

res = asy.run()
```

## Package Structure

```
├── oxapi
│   ├── abstract                
│   │   └── api.py              # Non-instantiable, super classes for API calls
│   ├── nlp                     
│   │   ├── classification.py   # NLP Classification package
│   │   ├── completion.py       # NLP Completion package
│   │   ├── encoding.py         # NLP Encoding package
│   │   ├── pipeline.py         # NLP Pipeline package
│   │   └── transformation.py   # NLP Transformation package
│   ├── utils.py                # General utilities
│   ├── async.py               # package for asynchronous API calls
│   └── error.py                # Custom exceptions module
├── tests                       # Tests
└── docs_src                    # Documentation source files
```

## Credits

(C) 2022 Oxolo GmbH