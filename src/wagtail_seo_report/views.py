from django.db.models import Case, CharField, F, IntegerField, Q, Value, When
from django.db.models.functions import Cast, Length, Round
from django.utils.translation import gettext_lazy as _
from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page


class WagtailSEOReportView(PageReportView):
    """
    A Wagtail ReportView that displays an SEO report.
    Contains a full list of all pages, sorted by SEO score (from worst to best).
    """

    title = _("SEO")
    header_icon = "wagtail-seo-report"
    results_template_name = "wagtail_seo_report/seo_score_report_results.html"
    list_export = [
        "title",
        "seo_title",
        "search_description",
    ]
    export_headings = {
        "title": _("title"),
        "seo_title": _("title tag"),
        "search_description": _("meta description"),
    }
    export_filename = "wagtail_seo_report"

    model = Page
    seo_score_components = [
        {"name": "seo_title_score", "weight": 40, "method": "annotate_seo_title_score"},
        {
            "name": "search_description_score",
            "weight": 60,
            "method": "annotate_search_description_score",
        },
    ]

    def get_seo_score_components(self):
        return self.seo_score_components

    def annotate_seo_score(self, qs):
        # Normalize weights to ensure they add up to 100
        total_weight = sum(
            component["weight"] for component in self.seo_score_components
        )

        # Initialize seo_score to zero
        qs = qs.annotate(seo_score=Value(0, output_field=IntegerField()))

        for component in self.seo_score_components:
            name = component["name"]
            weight = component["weight"]
            method_name = component["method"]

            # Calculate the component's effective weight as a fraction of 100
            normalized_weight = weight / total_weight * 100

            # Call the annotation method specified in the component
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                qs = method(qs)

                # Add the normalized weighted component score into seo_score
                qs = qs.annotate(
                    seo_score=Cast(
                        Round(F("seo_score") + F(name) * normalized_weight / 100, 0),
                        output_field=IntegerField(),
                    )
                )
            else:
                raise NotImplementedError(
                    f"The method {method_name} is not implemented"
                )

        return qs

    def annotate_search_description_score(self, qs):
        return qs.annotate(
            search_description_length=Length("search_description"),
            search_description_score=Case(
                When(
                    Q(search_description__isnull=True) | Q(search_description=""),
                    then=Value(0),
                ),
                When(
                    Q(search_description_length__gte=50)
                    & Q(search_description_length__lte=160),
                    then=Value(100),
                ),
                When(
                    Q(search_description__isnull=False)
                    & Q(search_description_length__lt=50)
                    & ~Q(search_description=""),
                    then=Value(50),
                ),
                When(
                    Q(search_description__isnull=False)
                    & Q(search_description_length__gt=160)
                    & ~Q(search_description=""),
                    then=Value(25),
                ),
                default=Value(0),
                output_field=IntegerField(),
            ),
        )

    def annotate_seo_title_score(self, qs):
        return qs.annotate(
            seo_title_value=Case(
                When(Q(seo_title__isnull=False), then=F("seo_title")),
                default=Value("title"),
                output_field=CharField(),
            ),
            seo_title_length=Length("seo_title_value"),
            seo_title_score=Case(
                When(
                    Q(seo_title_length__gte=50) & Q(seo_title_length__lte=60),
                    then=Value(100),
                ),
                When(
                    Q(seo_title_length__lt=50),
                    then=Value(50),
                ),
                When(
                    Q(seo_title_length__gt=60),
                    then=Value(50),
                ),
                default=Value(0),
                output_field=IntegerField(),
            ),
        )

    def get_queryset(self):
        qs = self.model.objects.all().select_related(
            "latest_revision", "latest_revision__user"
        )
        qs = self.annotate_seo_score(qs)
        qs = qs.order_by("seo_score")
        return qs
