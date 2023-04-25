import re
from typing import Optional

import numpy as np
import streamlit as st


def parse_numbers_input(n_input: str) -> np.ndarray:
    is_valid = re.match(r'^\d+(,\d+)*$', n_input)

    if is_valid:
        return np.array([float(n.strip()) for n in n_input.split(',')])

    return np.array([])


def calculate_stats(numbers: np.ndarray) -> dict:
    if numbers.size == 0:
        return {}

    return {
        'stddev': numbers.std(),
        'size': numbers.size,
        'avg': numbers.mean(),
        'estimate': np.sqrt(np.sum([(n - numbers.mean()) ** 2 for n in numbers]) / (numbers.size - 1))
    }


def show_stats(stats: dict, header: Optional[str]):
    if header:
        st.subheader(header)

    st.markdown(f'**Standard deviation (stddev):** {round(stats["stddev"], 4)}')
    st.markdown(f'**Average (mean):** {round(stats["avg"], 4)}')
    st.markdown(f'**Estimate (S):** {round(stats["estimate"], 4)}')
    st.markdown(f'**Estimate power of 2 (S^2):** {round(stats["estimate"] ** 2, 4)}')


def main():
    st.set_page_config(
        page_title="Sapir's Statistics",
        page_icon="🖩",
    )

    st.title("Sapir's statistics")

    input_numbers_first = st.text_input('First list of numbers (required)', '')
    input_numbers_second = st.text_input('Second list of numbers (optional)', '')

    if st.button('Calculate!'):
        st.balloons()

        numbers_first: np.ndarray = parse_numbers_input(input_numbers_first)
        numbers_second: np.ndarray = parse_numbers_input(input_numbers_second)

        if numbers_first.size == 0:
            st.write('Invalid input (first list)!')
            return

        if input_numbers_second and numbers_second.size == 0:
            st.write('Invalid input (second list)!')
            return

        stats_first = calculate_stats(numbers_first)
        stats_second = calculate_stats(numbers_second)

        show_stats(stats_first, f'First list ({numbers_first.size})')

        if stats_second:
            show_stats(stats_second, f'Second list ({numbers_second.size})')

            independent_var_eq = (numbers_first.size - 1) * stats_first['estimate'] ** 2 + \
                                 (numbers_second.size - 1) * stats_second['estimate'] ** 2
            independent_var_eq = independent_var_eq / (numbers_first.size + numbers_second.size - 2)
            independent_var_eq = independent_var_eq * (
                    (numbers_first.size + numbers_second.size) / (numbers_first.size * numbers_second.size)
            )
            independent_var_eq = np.sqrt(independent_var_eq)

            independent_var_diff_raw = (stats_first['estimate'] ** 2 / stats_first['size']) + (
                        stats_second['estimate'] ** 2 / stats_second['size'])
            independent_var_diff = np.sqrt(independent_var_diff_raw)

            df = numbers_first.size + numbers_second.size - 2

            df_tag = independent_var_diff_raw ** 2 / (
                    stats_first['estimate'] ** 2 / (stats_first['size'] ** 2 * (stats_first['size'] - 1)) +
                    stats_second['estimate'] ** 2 / (stats_second['size'] ** 2 * (stats_second['size'] - 1))
            )

            st.subheader("Combination stats")
            st.markdown(f"**df:** {round(df, 4)}")
            st.markdown(f"**Independent variance equality:** {round(independent_var_eq, 4)}")
            st.markdown(f"**Independent variance inequality:** {round(independent_var_diff, 4)}")
            st.markdown(f"**df` (tag):** {round(df_tag, 4)}")


if __name__ == '__main__':
    main()
