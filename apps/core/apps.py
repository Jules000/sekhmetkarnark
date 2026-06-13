from django.apps import AppConfig
from django.template.context import BaseContext, Context, RenderContext


def _patched_copy(self):
    if type(self) is BaseContext:
        duplicate = BaseContext.__new__(BaseContext)
        duplicate.dicts = self.dicts[:]
        return duplicate
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.dicts = self.dicts[:]
    for attr in ("template", "template_name", "render_context", "autoescape", "use_l10n", "use_tz", "_dict", "_stack", "request", "_processors", "_processors_index"):
        if hasattr(self, attr):
            setattr(duplicate, attr, getattr(self, attr))
    return duplicate


def _patched_new(self, values=None):
    new_context = _patched_copy(self)
    new_context._reset_dicts(values)
    return new_context


BaseContext.__copy__ = _patched_copy
Context.new = _patched_new


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Core"
