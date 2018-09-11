# lm-reports-to-html-widget

## Introduction
This script that takes several LogicMonitor reports and a keyfile as input, and produces a CSV of their intersection, then updates a text widget with an HTML table generated from this CSV.

## Installation

To install this package, run the following:

```
git clone https://github.com/ianbloom/lm-reports-to-html-widget.git
```

Then, run the following:

```
sudo python setup.py install
```

Included in this repo is an example key file (key.txt).  Replace the dummy values in this file with values corresponding to your API credentials.

## Usage

For information about the required variables, run the following:

```
python table_html.py -h
```

This script takes five arguments:
* _-file_ : Path to file containing API credentials
* _-cpu_ : ID of a CPU Device Metric Trends Report
* _-mem_ : ID of a MEM Device Metric Trends Report
* _-inv_ : ID of a Device Inventory Report
* _-widget_ : ID of a text widget to post HTML table into

