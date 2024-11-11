from django.urls import path, reverse

from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail import hooks

from .views import WagtailSeoReportView


@hooks.register("register_reports_menu_item")
def register_seo_report_menu_item():
    return AdminOnlyMenuItem("SEO Report for pages", reverse('wagtail-seo-report'), icon_name=WagtailSeoReportView.header_icon, order=700)


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("seo-report/", WagtailSeoReportView.as_view(), name="wagtail-seo-report"),
    ]