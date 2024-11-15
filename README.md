# Wagtail SEO Report

[![Version](https://img.shields.io/pypi/v/wagtail-seo-report.svg?style=flat)](https://pypi.python.org/pypi/wagtail-seo-report/)

A custom SEO report for you Wagtail pages.

![Wagtail SEO Report](./screenshot.jpg)

## Requirements

- Wagtail >= 6

## Settings

Overwrite this setting in order to extend the report with custom fields:

```python
WAGTAIL_SEO_REPORT_VIEW = "wagtail_seo_report.views.WagtailSEOReportView"
```
