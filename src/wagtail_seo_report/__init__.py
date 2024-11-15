from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from wagtail_seo_report.settings import VIEW


def get_seo_view():
    try:
        return import_string(VIEW)
    except ImportError:
        raise ImproperlyConfigured(
            f"WAGTAIL_SEO_REPORT_VIEW '{VIEW}' could not be imported. "
            "Ensure it is defined as 'app.module.ViewName'."
        )
