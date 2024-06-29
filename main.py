import tkinter as tk
import mcapi
from collections.abc import Iterable
import json
from collections import Counter
from PIL import Image
from translate import Translator
import tkinter.messagebox
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


languages = ['uk-UA', 'de-DE', 'en-UK']
language = 'en-UK'

root = tk.Tk()


def extract_keywords(data):
    keywords = []
    for k, v in data.items():
        if isinstance(v, Iterable) and not isinstance(v, str):
            v = " ".join(v)

        keywords.append(str(v).lower())
    return " ".join(keywords)


def search():
    is_empety = True
    search_query = search_query_entry.get()
    print(search_query)
    data = mcapi.get_data()

    found_mobs_listbox.delete(0, tk.END)

    for i in range(len(data)):
        item = data[i]

        keywords = extract_keywords(item)

        if search_query in keywords:
            is_empety = False
            print(item["displayName"])
            found_mobs_listbox.insert(tk.END, f'{i}. {item["displayName"]}')

    if is_empety:
        tkinter.messagebox.showinfo("Моб не знайдено", "Моб не знайдено")

    found_mobs_listbox.update()


def open_popup():
    selection = found_mobs_listbox.curselection()
    if selection:
        index = selection[0]
        mob_id = int(found_mobs_listbox.get(index).split(". ")[0])

        data = mcapi.get_data()[mob_id]

        if language != 'en-UK':
            # loading_label = tk.Label(new_window, text="Завантаження данних", font=('Terminal ',25), width=20)
            # loading_label.pack()

            tkinter.messagebox.showinfo(title="Завантаження", message="Відбувається завантаження данних. Зачекайте")

        formated_data = format_data(data)

        # if language != 'en-UK':
        # loading_label.pack_forget()
        new_window = tk.Toplevel(root)

        title_label = tk.Label(new_window, text=data["displayName"], font=('Terminal ', 25), width=20)
        title_label.pack()

        for k, v in formated_data[0].items():
            tk.Label(new_window, text=f"{k}: {v}").pack()

        def show_metadata_keys():
            tk.Label(new_window, text=str(formated_data[1])).pack()
            show_metadata_keys_button.pack_forget()

        show_metadata_keys_button = tk.Button(new_window, text="Показати ключі метаданних", command=show_metadata_keys,
                                              width=40)
        show_metadata_keys_button.pack()

        categories = {"hostile": "hostile.png"}

        def show_category_image():
            mob_type = data["type"]
            image = Image.open(resource_path(categories[mob_type]))
            image.show()

            show_category_image_button.pack_forget()

        if data["type"] in categories.keys():
            show_category_image_button = tk.Button(new_window, text="Показати зображення", command=show_category_image,
                                                   width=40)
            show_category_image_button.pack()

        new_window.mainloop()
    else:
        tkinter.messagebox.showwarning(title='Помилка', message="Виберіть предмет зі списку")


def format_data(data: dict):
    formated_data = {}

    # formated_data["Айді"] = data["id"]
    # formated_data["Внутрішній айді"] = data["internalId"]
    # formated_data["Ім'я"] = data["name"]
    # formated_data["Показане ім'я"] = data["displayName"]
    # formated_data["Довжина"] = data["width"]
    # formated_data["Висота"] = data["height"]
    # formated_data["Тип"] = data["type"]
    # formated_data["Категорія"] = data["category"]
    metadataKeys = json.dumps(data["metadataKeys"], indent=2)

    translator = Translator(to_lang=language)
    # translation = translator.translate("This is a pen.")

    # for k in data.keys():
    #     if k == "metadataKeys":
    #         continue

    #     if language != 'en-UK':
    #         translated_key = translator.translate(k)
    #     else:
    #         translated_key = k

    #     formated_data[translated_key] = data[k]
    #     print(translated_key, k)

    to_translate = ". ".join(data.keys()).lower()
    translated = translator.translate(to_translate)
    keys = translated.split(".")
    print(keys)
    print(to_translate)

    i = 0

    for k in data.keys():
        if k == "metadataKeys":
            continue

        formated_data[keys[i]] = data[k]
        print(formated_data[keys[i]], data[k])
        i += 1

    return formated_data, metadataKeys


def set_language(lang):
    global language
    language = lang


top = tk.Frame(root)
bottom = tk.Frame(root)
top.pack(side=tk.TOP)
bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

tk.Button(root, text="uk-UA", width=10, height=1, command=lambda: set_language("uk-UA")).pack(in_=top, side=tk.LEFT)
tk.Button(root, text='de-DE', width=10, height=1, command=lambda: set_language('de-DE')).pack(in_=top, side=tk.LEFT)
tk.Button(root, text='en-UK', width=10, height=1, command=lambda: set_language('en-UK')).pack(in_=top, side=tk.LEFT)

title_label = tk.Label(text="Minecraft mobs", font=('Terminal ', 25))
title_label.pack()

search_query_entry = tk.Entry(width=40)
search_query_entry.pack()

search_button = tk.Button(text="Search", command=search, width=40)
search_button.pack()

found_mobs_listbox = tk.Listbox(width=40)
found_mobs_listbox.pack()

open_popup_button = tk.Button(text="Open mob data", command=open_popup, width=40)
open_popup_button.pack()

data = mcapi.get_data()

types = [item["type"] for item in data]
print(Counter(types))

root.mainloop()
