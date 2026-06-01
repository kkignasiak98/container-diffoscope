{
  lib,
  python3Packages,
  fetchFromGitHub,
  nix-update-script,
  diffoscope,
}:

python3Packages.buildPythonApplication (finalAttrs: {
  pname = "container-diffoscope";
  version = "0.2.0";
  pyproject = true;
  __structuredAttrs = true;

  src = ./.;
  # src = fetchFromGitHub {
  #   owner = "kkignasiak98";
  #   repo = "container-diffoscope";
  #   tag = finalAttrs.version;
  #   hash = "sha256-E1eQ5bmCOXh9BMRErBjOGzgbLr3iuSOR9VRzOklZkgM=";
  # };

  build-system = [
    python3Packages.uv-build
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
    changelog = "https://github.com/kkignasiak98/container-diffoscope/releases/tag/${finalAttrs.version}";
    license = lib.licenses.mit; 
    maintainers = with lib.maintainers; [kkignasiak98]; #there will be more in the future!
    mainProgram = "container-diffoscope";
  };
})
