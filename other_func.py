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
        fields.append(field)
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                fields,
                spacing=20,
            ),
            padding=10,
        ),
        # shadow_color=ft.colors.BLACK,
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
        input_filter=ft.NumbersOnlyInputFilter()
    )
    height = ft.TextField(
        label="Высота",
        suffix_text="мм",
        input_filter=ft.NumbersOnlyInputFilter()
    )
    quantity = ft.TextField(
        label="Количество",
        suffix_text="шт.",
        input_filter=ft.NumbersOnlyInputFilter()
    )
    return width, height, quantity


def create_comments_and_layout_files_fields():
    comment_field_1 = ft.TextField(label="Место комментариев для верстки", multiline=True, max_lines=5)
    comment_field_2 = ft.TextField(label="Место комментариев для производства", multiline=True, max_lines=5)
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
    content_files = ft.ResponsiveRow(
        [
            load_file_text,
            ft.Container(
                content=load_file_btn,
                alignment=ft.alignment.center,
                col={'xs': 12, 'sm': 2},
                padding=ft.padding.only(top=5)
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    contents = [comment_field_1, comment_field_2, load_file_text, load_file_btn]
    return card(
        'Комментарии и файлы макета',
        [comment_field_1, comment_field_2, ft.Divider(), content_files]
    ), contents
