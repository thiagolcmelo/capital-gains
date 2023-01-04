from subprocess import PIPE, Popen

from src.cli import main, parse_input
from src.operation import Operation
from src.tax import Tax
from tests.utils import (
    assert_tax_output_equal,
    captured_output,
    data_cases_input_filenames,
    data_cases_output_filenames,
    data_cases_parsed,
)


def test_pipe_file_to_stdin(
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

        p = Popen(
            [
                "/usr/bin/env",
                "python3",
                "src/cli.py",
            ],
            stdin=PIPE,
            stdout=PIPE,
        )
        out, _ = p.communicate(input_string.encode("utf-8"))
        assert_tax_output_equal(out.decode("utf-8"), output_string, label)


def test_redirect_file_to_stdin(
    data_cases_input_filenames, data_cases_output_filenames, data_cases_parsed
):
    for input_file, output_file, parsed in zip(
        data_cases_input_filenames, data_cases_output_filenames, data_cases_parsed
    ):
        label = parsed["label"]

        with open(output_file, "r") as f_output:
            output_string = f_output.read()

        p = Popen(
            [
                "sh",
                "-c",
                f"/usr/bin/env python3 src/cli.py < {input_file}",
            ],
            stdout=PIPE,
        )
        out, _ = p.communicate()
        assert_tax_output_equal(out.decode("utf-8"), output_string, label)
