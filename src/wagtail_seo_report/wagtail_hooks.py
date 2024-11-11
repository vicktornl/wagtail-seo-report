from django.urls import path, reverse
from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail import hooks
from wagtail_seo_report import get_seo_view
from wagtail_seo_report.settings import get_setting

@hooks.register("register_reports_menu_item")
def register_seo_report_menu_item():
    icon_name = get_setting("ICON", "default-icon")  # Fallback icon if not defined
    return AdminOnlyMenuItem("SEO Report for pages", reverse('wagtail-seo-report'), icon_name=icon_name, order=700)


@hooks.register("register_admin_urls")
def register_admin_urls():
    seo_view = get_seo_view()
    return [
        path("seo-report/", seo_view.as_view(), name="wagtail-seo-report")
    ]
