{
  lib,
  python3Packages,
  fetchFromGitHub,
  nix-update-script,
  diffoscope,
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
    python3Packages.pythonRelaxDepsHook
  ];

  pythonRelaxDeps = true;

  dependencies = with python3Packages; [
    polars
    typer
  ];

  propagatedBuildInputs = [
    diffoscope
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
    maintainers = with lib.maintainers; [kkignasiak98]; #there will be more in the future!
    mainProgram = "container-diffoscope";
  };
})
