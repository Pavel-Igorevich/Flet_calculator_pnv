import flet as ft


def process_and_replace_keys(dictionary):
    keys_to_remove = [key for key in dictionary.keys() if isinstance(key, str) and key.startswith('_')]

    for key in keys_to_remove:
        del dictionary[key]

    for key, value in dictionary.items():
        if isinstance(value, dict):
            process_and_replace_keys(value)

    # Замена ключей 'null' на None
    if 'null' in dictionary:
        dictionary[None] = dictionary.pop('null')


def checking_size(event):
    if len(event.control.value) == 0:
        event.control.error_text = 'Не может быть пустым'
    elif len(event.control.value) < 2 or not event.control.value.isdigit():
        event.control.error_text = 'Размер задается целым числом от 10'
    else:
        event.control.error_text = ''


def checking_quantity(event):
    if not event.control.value:
        event.control.error_text = 'Не может быть пустым'
    elif not event.control.value.isdigit():
        event.control.error_text = 'Количество задается целым числом'
    else:
        event.control.error_text = ''


def card(name_card, content_fields):
    title = ft.Row(
        [ft.Text(name_card)],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    fields = [title, ]
    for field in content_fields:
        # print(field)
        fields.append(field)
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                fields,
                spacing=20,
            ),
            padding=10,
        ),
        surface_tint_color=ft.colors.BLACK
    )


def card_result(part_content, name_card=None):
    if name_card:
        name_card = ft.Container(
            ft.Text(
                name_card,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_700,
                size=15,
            ),
        )

    card_content = ft.Card(
        content=ft.Container(
            width=1000,
            padding=ft.padding.symmetric(20, 10),
            content=ft.Column(
                part_content,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
        ),
    )
    if name_card:
        return name_card, card_content
    else:
        return card_content


def load_files(e: ft.FilePickerResultEvent, layout_name):
    upload_files = []
    if not e.files:
        load_file_text = ''
    else:
        load_file_text = ", ".join(map(lambda f: f.name, e.files))
        # todo реализация только для пк, потом переделать
        for num, file in enumerate(e.files):
            upload_files.append(
                [f"{layout_name}_{num}.{file.name.split('.')[-1]}", file.path]
            )
    return load_file_text, upload_files


def create_general_params():
    width = ft.TextField(
        label="Ширина",
        suffix_text="мм",
    )
    height = ft.TextField(
        label="Высота",
        suffix_text="мм",
    )
    quantity = ft.TextField(
        label="Количество",
        suffix_text="шт.",
    )
    load_file_text = ft.TextField(
        label="Файлы макета",
        read_only=True,
        col={'xs': 12, 'sm': 10}
    )
    load_file_btn = ft.IconButton(
        icon=ft.icons.UPLOAD_FILE,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.AMBER, color=ft.colors.BLACK, padding=10
        )
    )
    return width, height, quantity, load_file_text, load_file_btn
