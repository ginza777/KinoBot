from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema

from .utils import (app_schema_view, in_app_schema_view,
                                main_schema_view, panel_schema_view)

swagger_urlpatterns = [
    re_path("swagger-without-ui/", main_schema_view.without_ui(cache_timeout=0), name="schema-json"),  # noqa
    re_path(
        r"^swagger/$",
        main_schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path("redoc/", main_schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),  # noqa
    re_path("apps/swagger", panel_schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),  # noqa
    re_path("bots/swagger", in_app_schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),  # noqa
    re_path("swagger/", app_schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),  # noqa
]


class CustomHeaderSchemaGenerator(SwaggerAutoSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_manual_parameters(self, parameters):
        super_params = super().get_pagination_parameters()
        # add custom header parameters
        parameters.append(openapi.Parameter("Device-Name", openapi.IN_HEADER, description="Device Name",
                                            type=openapi.TYPE_STRING, required=True, default="X-Device-Name"))  # noqa
        parameters.append(openapi.Parameter("User-Agent", openapi.IN_HEADER, description="User-Agent",
                                            type=openapi.TYPE_STRING, required=True,
                                            default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                                                    " (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"))  # noqa
        parameters.append(openapi.Parameter("Device-Type", openapi.IN_HEADER, description="Device Type",
                                            type=openapi.TYPE_STRING, required=True, default="Android"))  # noqa
        parameters.append(openapi.Parameter("Device-Id", openapi.IN_HEADER, description="Device Id",
                                            type=openapi.TYPE_STRING, required=True, default="X-Device-Id"))
        parameters.append(openapi.Parameter("Account-Id", openapi.IN_HEADER, description="Account Id",
                                            type=openapi.TYPE_STRING, required=False)) # noqa
        return super_params + parameters
