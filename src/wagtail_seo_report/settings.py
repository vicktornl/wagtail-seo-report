from django.conf import settings

def get_setting(name: str, default=None):
    return getattr(settings, "WAGTAIL_SEO_REPORT_%s" % name, default)

REPORT_VIEW = get_setting("REPORT_VIEW", "wagtail-seo-report.views.WagtailSeoReportView")

