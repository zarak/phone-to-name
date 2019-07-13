# README

Place csv file with phone numbers in a folder named `source_files` in the root
directory. 

```
.
├── phone_to_name
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   └── settings.cpython-36.pyc
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   ├── source_files
│   │   ├── emails.csv
│   │   └── phone_numbers.csv
│   └── spiders
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-36.pyc
│       │   └── zabasearch.cpython-36.pyc
│       └── zabasearch.py
├── readme.md
└── scrapy.cfg
```

Run the crawler with the command `scrapy crawl zabasearch -o zaba.csv -t csv`.
