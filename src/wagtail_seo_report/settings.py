from django.conf import settings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANGUAGES = [
    ("nl", "Nederlands"),
]

LANGUAGE_CODE = "nl"

LOCALE_PATHS = [os.path.join(BASE_DIR, "locales")]

def get_setting(name: str, default=None):
    return getattr(settings, "WAGTAIL_SEO_REPORT_%s" % name, default)


WAGTAIL_SEO_REPORT_REPORT_VIEW = "wagtail_seo_report.views.WagtailSeoReportView"
