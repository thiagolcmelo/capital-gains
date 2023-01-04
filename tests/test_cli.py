from src.cli import main, parse_input
from src.operation import Operation
from src.tax import Tax
from tests.utils import (
    assert_operation_list_equal,
    assert_tax_output_equal,
    captured_output,
    data_cases_input_filenames,
    data_cases_output_filenames,
    data_cases_parsed,
)


def test_parse_input(data_cases_input_filenames, data_cases_parsed):
    for input_file, parsed in zip(data_cases_input_filenames, data_cases_parsed):
        with open(input_file, "r") as f:
            simulation_lines = parse_input(f.read())
            parsed_input = parsed["input"]
            label = parsed["label"]

            assert len(simulation_lines) == len(parsed_input), label

            for actual, expected in zip(simulation_lines, parsed_input):
                assert_operation_list_equal(actual, expected, label)


def test_main(
    data_cases_input_filenames, data_cases_output_filenames, data_cases_parsed
):
    for input_file, output_file, parsed in zip(
        data_cases_input_filenames, data_cases_output_filenames, data_cases_parsed
    ):
        label = parsed["label"]

        with open(input_file, "r") as f_input:
            input_string = f_input.read()

        with open(output_file, "r") as f_output:
            output_string = f_output.read()

        with captured_output() as (out, _):
            main(input_string)
            assert_tax_output_equal(out.getvalue(), output_string, label)
