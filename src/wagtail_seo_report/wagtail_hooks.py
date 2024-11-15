from django.templatetags.static import static
from django.urls import path, reverse
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from wagtail_seo_report import get_seo_view


class WagtailSEOReportMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.has_perm("wagtailsearchpromotions.view_searchpromotion")


@hooks.register("register_reports_menu_item")
def register_seo_report_menu_item():
    return WagtailSEOReportMenuItem(
        "SEO", reverse("wagtail-seo-report"), icon_name="wagtail-seo-report", order=700
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    seo_view = get_seo_view()
    return [path("seo-report/", seo_view.as_view(), name="wagtail-seo-report")]


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["wagtail_seo_report/wagtail_seo_report.svg"]


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_seo_report/core.css"),
    )
