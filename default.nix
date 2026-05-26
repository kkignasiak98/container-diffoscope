{
  lib,
  python3Packages,
  fetchFromGitHub,
  fetchPypi,
  nix-update-script,
}:

python3Packages.buildPythonApplication (finalAttrs: {
  pname = "container-diffoscope";
  version = "0.1.0";
  pyproject = true;
  __structuredAttrs = true;

  src = fetchFromGitHub {
    owner = "kkignasiak98";
    repo = "container-diffoscope";
    tag = finalAttrs.version;
    hash = "sha256-Ox5MfVzCQU8y+P3N5KqTEMSVLHeIaIhZlZdgLAdA2Mw=";
  };

  build-system = [
    python3Packages.poetry-core
  ];

  dependencies = [
    (python3Packages.polars.overridePythonAttrs (old: rec {
      version = "1.26.0";
      src = fetchPypi {
        inherit (old) pname;
        inherit version;
        hash = "sha256-tUktOOXsKuaohTgzxaMVSRlKNhuQETT8Xy9XtJvVY+o=";
      };
    }))
    (python3Packages.typer.overridePythonAttrs (old: rec {
      version = "0.15.3";
      src = fetchPypi {
        inherit (old) pname;
        inherit version;
        hash = "sha256-gYhzYl0FaWU0ODFlZ4YYmffply8ubgwW2rYINFztcTw=";
      };
      propagatedBuildInputs = (old.propagatedBuildInputs or []) ++ [
        python3Packages.typing-extensions
      ];
    }))
  ];

  pythonImportsCheck = [
    "container_diffoscope"
  ];

  passthru.updateScript = nix-update-script { };

  meta = {
    description = "Elegant Container filesystem comparison";
    homepage = "https://github.com/kkignasiak98/container-diffoscope";
    changelog = "https://github.com/kkignasiak98/container-diffoscope/releases/tag/${finalAttrs.src.tag}";
    license = lib.licenses.mit;
    maintainers = with lib.maintainers; [ ];
    mainProgram = "container-diffoscope";
  };
})
