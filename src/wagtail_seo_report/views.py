from django.db import models
from django.db.models.functions import Length
from wagtail.models import Page
from wagtail.admin.views.reports import PageReportView
from django.utils.translation import gettext_lazy as _


class WagtailSeoReportView(PageReportView):
    """
    A Wagtail ReportView that displays an SEO report.
    Contains a full list of all pages, sorted by SEO score(from worst to best).
    """
    title = _("SEO report")
    header_icon = "site"
    permission_policy = "wagtailadmin.access_admin"
    results_template_name = "wagtail_seo_report/seo_score_report_results.html"    
    

    def get_queryset(self):
        qs = Page.objects.all()

        # Annotate the queryset with the SEO score
        qs = qs.annotate(
            search_description_length=Length('search_description'),
            search_description_score=models.Case(
                models.When(search_description__isnull=True, then=models.Value(0)),
                models.When(models.Q(search_description_length__gte=50) & models.Q(search_description_length__lte=160), then=models.Value(60)),
                models.When(models.Q(search_description_length__lt=50) & models.Q(search_description_isnull=False), then=models.Value(40)),
                models.When(models.Q(search_description_length__gt=160) & models.Q(search_description_isnull=False), then=models.Value(40)),
                default=models.Value(0),
                output_field=models.IntegerField()
            ),
            seo_title_length=Length('seo_title'),
            seo_title_score=models.Case(
                models.When(seo_title__isnull=True, then=models.Value(0)),
                models.When(models.Q(seo_title_length__gte=50) & models.Q(seo_title_length__lte=60), then=models.Value(40)),
                models.When(models.Q(seo_title_length__lt=50) & models.Q(seo_title_isnull=False), then=models.Value(20)),
                models.When(models.Q(seo_title_length__gt=60) & models.Q(seo_title_isnull=False), then=models.Value(20)),
                default=models.Value(0),
                output_field=models.IntegerField()
            ),
            seo_score=models.F('seo_title_score') + models.F('search_description_score')
        ).order_by('seo_score')
        return qs


    
