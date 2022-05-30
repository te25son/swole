from typing import Any, Dict, Optional

from returns.maybe import Maybe


class Context:
    def __init__(
        self,
        template_name: str,
        template_folder_name: str,
        hx_request_header: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.template = self._get_template_path(
            template_name, template_folder_name, hx_request_header
        )
        self.data = Maybe.from_optional(data).value_or({})

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value: str):
        self._template = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: dict):
        self._data = value

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value

    def __getitem__(self, key: str, value: Any) -> None:
        self.data[key] = value

    @staticmethod
    def _get_template_path(
        template_name: str,
        template_folder_name: str,
        hx_request_header: Optional[str],
    ) -> str:
        template_path = f"{template_folder_name}/{template_name}"
        return (
            Maybe.from_optional(hx_request_header)
            .bind_optional(lambda x: f"{template_path}.html")
            .value_or(f"{template_path}_base.html")
        )


class WorkoutsContext(Context):
    def __init__(
        self,
        template_name: str,
        hx_request_header: Optional[str],
        data: Optional[dict] = None,
    ) -> None:
        super().__init__(template_name, "workouts", hx_request_header, data)


class AccountContext(Context):
    def __init__(
        self,
        template_name: str,
        hx_request_header: Optional[str],
        data: Optional[dict] = None,
    ) -> None:
        super().__init__(template_name, "account", hx_request_header, data)
