{ python3, fetchPypi, }:
python3.pkgs.buildPythonPackage rec {
  pname = "crispy-bulma";
  version = "0.11.0";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-J+zNCaWnd1TWRGL2H/WFwA/rjBX2XQ2PlnarJva8NWI=";
  };

  nativeBuildInputs = with python3.pkgs; [ setuptools wheel ];

  propagatedBuildInputs = with python3.pkgs; [
    asgiref
    django
    django-crispy-forms
  ];

}
