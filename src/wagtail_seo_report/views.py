from django.db.models import Case, When, Value, IntegerField, Q, F
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
            search_description_score=Case(
                When(Q(search_description__isnull=True) | Q(search_description=''), then=Value(0)),  # No description or empty string gets 0
                When(Q(search_description_length__gte=50) & Q(search_description_length__lte=160), then=Value(60)),  # Optimal length
                When(Q(search_description_length__lt=50) & Q(search_description__isnull=False) & ~Q(search_description=''), then=Value(30)),  # Too short
                When(Q(search_description_length__gt=160) & Q(search_description__isnull=False) & ~Q(search_description=''), then=Value(10)),  # Too long
                default=Value(0),
                output_field=IntegerField()
            ),
            seo_title_length=Length('seo_title'),
            seo_title_score=Case(
                When(Q(seo_title__isnull=True) | Q(seo_title=''), then=Value(0)),  # No title or empty string gets 0
                When(Q(seo_title_length__gte=50) & Q(seo_title_length__lte=60), then=Value(40)),  # Optimal length
                When(Q(seo_title_length__lt=50) & Q(seo_title__isnull=False) & ~Q(seo_title=''), then=Value(20)),  # Too short
                When(Q(seo_title_length__gt=60) & Q(seo_title__isnull=False) & ~Q(seo_title=''), then=Value(10)),  # Too long
                default=Value(0),
                output_field=IntegerField()
            ),
            seo_score=F('seo_title_score') + F('search_description_score')
        ).order_by('seo_score')
        
        return qs


    
