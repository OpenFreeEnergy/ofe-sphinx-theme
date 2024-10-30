"""Sphinx theme for Open Free Energy software based on the PyData theme."""

# Add imports here
from pathlib import Path
from typing import Optional

from sphinx.application import Sphinx
from sphinx.config import Config
import sass
from sass import SassColor

from importlib.metadata import version


__version__ = version('ofe_sphinx_theme')


def html_theme_path() -> Path:
    """The path to the theme itself."""
    here = Path(__file__).parent.resolve()
    return here


def compile_css(app: Sphinx, exception: Optional[Exception]):
    """Compile SASS into CSS"""
    if exception is not None:
        return

    src = html_theme_path() / "sass/ofe-sphinx-theme.scss"
    dest = Path(app.outdir) / "_static/styles/ofe-sphinx-theme.css"

    dest.parent.mkdir(exist_ok=True, parents=True)

    accent_color = app.config["html_theme_options"].get(
        "accent_color", "DarkGoldenYellow"
    )
    accent_color, accent_color_darkmode = {
        "DarkGoldenYellow": (
            "var(--ofe-color-DarkGoldenYellow)",
            "var(--ofe-color-DarkGoldenYellow)",
        ),
        "FeelingSpicy": (
            "var(--ofe-color-FeelingSpicy)",
            "var(--ofe-color-FeelingSpicy-darkmode)",
        ),
        "FeelingSick": (
            "var(--ofe-color-FeelingSick)",
            "var(--ofe-color-FeelingSick-darkmode)"),
        "FeelingFabulous": (
            "var(--ofe-color-FeelingFabulous)",
            "var(--ofe-color-FeelingFabulous-darkmode)",
        ),
        "FeelingBlue": (
            "var(--ofe-color-FeelingBlue)",
            "var(--ofe-color-FeelingBlue-darkmode)"
        ),
    }.get(accent_color, accent_color)

    css = sass.compile(
        filename=str(src),
        output_style="compressed",
        custom_functions={
            "accent_color": lambda: accent_color,
            "accent_color_darkmode": lambda: accent_color_darkmode,
        },
    )

    with open(dest, "w") as f:
        print(css, file=f)


def setup(app: Sphinx):
    """Set up the theme's Sphinx extension"""
    app.add_html_theme("ofe_sphinx_theme", str(html_theme_path()))

    app.connect("build-finished", compile_css)

    # usually this would be done in the `"config-init"` event,
    # but this event runs before themes are loaded
    app.config.templates_path.append(str(html_theme_path() / "templates"))

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
