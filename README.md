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

## Setup

This script requires three reports.  One 'Device Metric Trends' report for CPU, one for memory, and a 'Device Inventory' report with as many device properties included as you like.  Make note of the IDs of these reports.

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

## Example

For my LogicMonitor account, I run the following:

```
python table_html.py -file key.txt -cpu 19 -mem 20 -inv 21 -widget 1567
```

## Result

The script will save a CSV and an HTML file of the data locally, and will post said HTML file into a LogicMonitor text widget to look like the following:

![Optional Text](https://github.com/ianbloom/lm-reports-to-html-widget/blob/master/images/Screen%20Shot%202018-09-11%20at%204.11.41%20PM.png)

