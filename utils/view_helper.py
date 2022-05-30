from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from returns.maybe import Maybe

from utils.response_context import Context


def render_view(
    request: HttpRequest,
    context: Context,
    template_override: str | None = None,
    trigger: str | None = None,
) -> HttpResponse:
    response = render(
        request=request,
        template_name=Maybe.from_optional(template_override).value_or(context.template),
        context=context.data,
    )

    if trigger:
        response.headers["hx-trigger"] = trigger

    return response


class HtmxResponse(HttpResponse):
    def __init__(
        self, trigger: str | None = None, content=b"", *args, **kwargs
    ) -> None:
        super().__init__(content, *args, **kwargs)

        if trigger:
            self.headers["hx-trigger"] = trigger
