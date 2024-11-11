from django.conf import settings

def get_setting(name: str, default=None):
    return getattr(settings, "WAGTAIL_SEO_REPORT_%s" % name, default)

WAGTAIL_SEO_REPORT_REPORT_VIEW = "wagtail_seo_report.views.WagtailSeoReportView"
WAGTAIL_SEO_REPORT_ICON = "report-icon"  # Optional icon name

