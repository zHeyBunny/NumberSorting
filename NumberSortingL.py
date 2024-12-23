import streamlit as st
import pandas as pd
from io import BytesIO

# Коды операторов
mts_codes = {910, 911, 912, 913, 914, 915, 916, 917, 918,
             919, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989}
megafon_codes = {920, 921, 922, 923, 924, 925, 926, 927, 928,
                 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 999}

# Функция для сортировки номеров


def sort_numbers(numbers):
    mts_numbers = []
    megafon_numbers = []
    other_numbers = []

    for number in numbers:
        number = number.strip()
        if len(number) < 4 or not number.isdigit():
            other_numbers.append(number)
            continue

        try:
            # Извлекаем первые три цифры после "+7" или "7"
            code = int(number[1:4])
            if code in mts_codes:
                mts_numbers.append(number)
            elif code in megafon_codes:
                megafon_numbers.append(number)
            else:
                other_numbers.append(number)
        except ValueError:
            other_numbers.append(number)

    return mts_numbers, megafon_numbers, other_numbers


# Streamlit UI
st.title("Number Sorter")
st.markdown(
    "Введите номера телефонов (каждый с новой строки) в поле ниже и нажмите кнопку **\"Сортировать\"**.")

# Поле для ввода номеров
input_numbers = st.text_area("Введите номера телефонов", height=200)

if st.button("Сортировать"):
    if not input_numbers.strip():
        st.warning("Пожалуйста, введите хотя бы один номер телефона.")
    else:
        numbers = input_numbers.strip().split("\n")
        mts, megafon, others = sort_numbers(numbers)

        # Выровнять длины списков
        max_length = max(len(mts), len(megafon), len(others))
        mts += ["" for _ in range(max_length - len(mts))]
        megafon += ["" for _ in range(max_length - len(megafon))]
        others += ["" for _ in range(max_length - len(others))]

        # Создание DataFrame для Excel
        data = {
            "MTS": mts,
            # Пустой разделительный столбец
            "": ["" for _ in range(max_length)],
            "Megafon": megafon,
            # Еще один разделительный столбец
            "  ": ["" for _ in range(max_length)],
            "Others": others,
        }
        df = pd.DataFrame(data)

        # Создание Excel-файла в памяти
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        # Предложить скачать файл
        st.success("Сортировка завершена!")
        st.download_button(
            label="Скачать Excel файл",
            data=output,
            file_name="sorted_numbers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# Копирайт
st.markdown("---")
st.markdown("© zHeyBunny")
