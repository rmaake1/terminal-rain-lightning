{ lib, python3Packages }:

python3Packages.buildPythonApplication {
  format = "pyproject";
  pname = "terminal-rain-lightning";
  version = "0.1.0";

  propagatedBuildInputs = [ python3Packages.setuptools ];

  src = ./.;
}
