{ lib, python3Packages }:
with python3Packages;
buildPythonApplication {
  format = "pyproject";
  pname = "terminal-rain-lightning";
  version = "0.1.0";

  propagatedBuildInputs = [ setuptools ];

  src = ./.;
}
