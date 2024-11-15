from django.conf import settings


def get_setting(name: str, default=None):
    return getattr(settings, "WAGTAIL_SEO_REPORT_%s" % name, default)


VIEW = get_setting("VIEW", default="wagtail_seo_report.views.WagtailSEOReportView")
