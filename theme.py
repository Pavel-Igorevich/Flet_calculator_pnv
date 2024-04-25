import flet as ft
import json


def read_json_file(file_path):
    with open(file_path, mode='r') as file:
        content = file.read()
        return json.loads(content)


def main():
    file_path = 'assets/material-theme.json'
    theme_json_data = read_json_file(file_path)
    themes = []
    for color_theme in ['light', 'dark']:
        theme_data = theme_json_data['schemes'][color_theme]
        theme = ft.ColorScheme(
            primary=theme_data['primary'],
            on_primary=theme_data['onPrimary'],
            primary_container=theme_data['primaryContainer'],
            on_primary_container=theme_data['onPrimaryContainer'],
            secondary=theme_data['secondary'],
            on_secondary=theme_data['onSecondary'],
            secondary_container=theme_data['secondaryContainer'],
            on_secondary_container=theme_data['onSecondaryContainer'],
            tertiary=theme_data['tertiary'],
            on_tertiary=theme_data['onTertiary'],
            tertiary_container=theme_data['tertiaryContainer'],
            on_tertiary_container=theme_data['onTertiaryContainer'],
            error=theme_data['error'],
            on_error=theme_data['onError'],
            error_container=theme_data['errorContainer'],
            on_error_container=theme_data['onErrorContainer'],
            background=theme_data['background'],
            on_background=theme_data['onBackground'],
            surface=theme_data['surface'],
            on_surface=theme_data['onSurface'],
            surface_variant=theme_data['surfaceVariant'],
            on_surface_variant=theme_data['onSurfaceVariant'],
            outline=theme_data['outline'],
            outline_variant=theme_data['outlineVariant'],
            shadow=theme_data['shadow'],
            scrim=theme_data['scrim'],
            inverse_surface=theme_data['inverseSurface'],
            on_inverse_surface=theme_data['inverseOnSurface'],
            inverse_primary=theme_data['inversePrimary']
        )
        themes.append(theme)
    return themes
