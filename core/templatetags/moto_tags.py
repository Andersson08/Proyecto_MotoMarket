from django import template

register = template.Library()


@register.filter
def cop(valor):
    try:
        return "$" + f"{int(valor):,}".replace(",", ".")
    except (TypeError, ValueError):
        return valor


@register.filter
def estrellas(valor):
    if not valor:
        return ""
    llenas = round(valor)
    return "★" * llenas + "☆" * (5 - llenas)


@register.filter
def bs(campo):
    widget = campo.field.widget
    clase = "form-select" if getattr(widget, "input_type", "") == "select" else "form-control"
    if campo.errors:
        clase += " is-invalid"
    return campo.as_widget(attrs={"class": clase})
