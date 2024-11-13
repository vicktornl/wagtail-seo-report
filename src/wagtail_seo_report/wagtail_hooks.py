from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from wagtail_seo_report import get_seo_view


@hooks.register("register_reports_menu_item")
def register_seo_report_menu_item():
    class CustomMenuItem(MenuItem):
        def is_shown(self, request):
            return (
                request.user.has_perm("wagtailsearchpromotions.add_searchpromotion")
                or request.user.is_superuser
            )

    return CustomMenuItem(
        "SEO", reverse("wagtail-seo-report"), icon_name="search", order=700
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    seo_view = get_seo_view()
    return [path("seo-report/", seo_view.as_view(), name="wagtail-seo-report")]
