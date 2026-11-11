import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class ConverterCliTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(prefix="markdown pdf ")
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.input_dir = self.root / "markdown files"
        self.input_dir.mkdir()
        self.output_pdf = self.root / "merged output.pdf"
        self.executable = self.root / "wkhtmltopdf custom.exe"
        self.executable.touch()
        self.executable.chmod(0o755)
        self.args = [str(self.input_dir), str(self.output_pdf)]

    def test_passes_paths_with_spaces_to_converter(self):
        with patch.object(main, "convert_and_merge_md_files") as convert:
            main.main([*self.args, "--wkhtmltopdf", str(self.executable)])

        convert.assert_called_once_with(
            self.input_dir, self.output_pdf, str(self.executable.resolve())
        )

    def test_discovers_executable_on_path(self):
        with patch("main.shutil.which", return_value=str(self.executable)) as which:
            with patch.object(main, "convert_and_merge_md_files") as convert:
                main.main(self.args)

        which.assert_called_once_with("wkhtmltopdf")
        convert.assert_called_once_with(
            self.input_dir, self.output_pdf, str(self.executable.resolve())
        )

    def test_rejects_a_missing_input_directory(self):
        self.assert_cli_error(
            [str(self.root / "missing"), str(self.output_pdf)],
            "input directory does not exist",
        )

    def test_rejects_a_missing_explicit_executable(self):
        self.assert_cli_error(
            [*self.args, "--wkhtmltopdf", str(self.root / "missing.exe")],
            "wkhtmltopdf is not executable",
        )

    def test_explains_how_to_supply_an_executable_when_path_lookup_fails(self):
        with patch("main.shutil.which", return_value=None):
            self.assert_cli_error(self.args, "Install it or use --wkhtmltopdf")

    def test_rejects_a_missing_output_directory(self):
        self.assert_cli_error(
            [str(self.input_dir), str(self.root / "missing" / "merged.pdf")],
            "output directory does not exist",
        )

    def test_rejects_a_merged_path_that_would_overwrite_an_intermediate(self):
        (self.input_dir / "notes.md").touch()

        self.assert_cli_error(
            [str(self.input_dir), str(self.input_dir / "notes.pdf")],
            "output path would overwrite an input or intermediate file",
        )

    def assert_cli_error(self, args, message):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as error:
            main.main(args)
        self.assertEqual(error.exception.code, 2)
        self.assertIn(message, stderr.getvalue())
