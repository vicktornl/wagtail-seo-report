from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from wagtail_seo_report.settings import get_setting

def get_seo_view():
    view_path = get_setting("REPORT_VIEW", "wagtail_seo_report.views.WagtailSeoReportView")
    try:
        return import_string(view_path)
    except ImportError:
        raise ImproperlyConfigured(
            f"WAGTAIL_SEO_REPORT_REPORT_VIEW '{view_path}' could not be imported. "
            "Ensure it is defined as 'app.module.ViewName'."
        )