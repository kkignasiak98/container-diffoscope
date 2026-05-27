# Documentation: https://docs.brew.sh/Formula-Cookbook
#                https://docs.brew.sh/rubydoc/Formula
# PLEASE REMOVE ALL GENERATED COMMENTS BEFORE SUBMITTING YOUR PULL REQUEST!
class ContainerDiffoscope < Formula
  include Language::Python::Virtualenv

  desc "Elegant Container filesystem comparison "
  homepage "https://github.com/kkignasiak98/container-diffoscope"
  url "https://github.com/kkignasiak98/container-diffoscope/archive/refs/tags/0.1.0.tar.gz"
  sha256 "107fe5768f1023fb1f3474fe1c54d8cadf45e34645470d6893c1a84ff4a5f9c1"
  license ""

  depends_on "python@3.13"
  depends_on "diffoscope"

  # Additional dependency
  # resource "" do
  #   url ""
  #   sha256 ""
  # end

    # polars ships pre-built Rust binaries — use platform wheels, not the sdist
on_macos do
    on_arm do
      resource "polars" do
        url "https://files.pythonhosted.org/packages/e3/0a/5c9455ff271c3583bf0fd505911e5787ca7bc0f247968853cb6dcfbedffb/polars-1.26.0-cp39-abi3-macosx_11_0_arm64.whl", using: :nounzip
        sha256 "587eb3c5000423eb20be998f523e605ddba0d3c598ba4a7e2a4d0b92b1fd2a7e"
      end
    end
    on_intel do
      resource "polars" do
        url "https://files.pythonhosted.org/packages/4a/99/ce4427576a6134504e6dd58f5d411d55b228a05950c5fff5b75e90263cb1/polars-1.26.0-cp39-abi3-macosx_10_12_x86_64.whl", using: :nounzip
        sha256 "2afefcd356608981b2e15d46df9ddaa6e77f36095ebeb73c3261e198bd51c925"
      end
    end
  end
  on_linux do
    on_arm do
      resource "polars" do
        url "https://files.pythonhosted.org/packages/e6/eb/b420131563a42ac0866224aa6284a356107d036c32d825c5478767a1446e/polars-1.26.0-cp39-abi3-manylinux_2_24_aarch64.whl", using: :nounzip
        sha256 "110d6987d37ae954a5ef16d739fb717df9d39b144790d12d98fb3e72ed35621c"
      end
    end
    on_intel do
      resource "polars" do
        url "https://files.pythonhosted.org/packages/6c/0a/c9e388b35533fc1827eaeb0f3940ba0a1058511bf77aaa689ebb1b0bef88/polars-1.26.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", using: :nounzip
        sha256 "66c30f4b7e060c2e7f3a45d6ac94ab3b179831a2f1e629401bf7912d54311529"
      end
    end
  end

  resource "annotated-doc" do
    url "https://files.pythonhosted.org/packages/57/ba/046ceea27344560984e26a590f90bc7f4a75b06701f653222458922b558c/annotated_doc-0.0.4.tar.gz"
    sha256 "fbcda96e87e9c92ad167c2e53839e57503ecfda18804ea28102353485033faa4"
  end

  resource "click" do
    url "https://files.pythonhosted.org/packages/9b/98/518d8e5081007684232226f475082b30087d0f585e8457db087298259f49/click-8.4.1.tar.gz"
    sha256 "918b5633eddf6b41c32d4f454bf0de810065c74e3f7dbf8ee5452f8be88d3e96"
  end

  resource "markdown-it-py" do
    url "https://files.pythonhosted.org/packages/06/ff/7841249c247aa650a76b9ee4bbaeae59370dc8bfd2f6c01f3630c35eb134/markdown_it_py-4.2.0.tar.gz"
    sha256 "04a21681d6fbb623de53f6f364d352309d4094dd4194040a10fd51833e418d49"
  end

  resource "mdurl" do
    url "https://files.pythonhosted.org/packages/d6/54/cfe61301667036ec958cb99bd3efefba235e65cdeb9c84d24a8293ba1d90/mdurl-0.1.2.tar.gz"
    sha256 "bb413d29f5eea38f31dd4754dd7377d4465116fb207585f97bf925588687c1ba"
  end

  def install
    virtualenv_install_with_resources
  end

  resource "pygments" do
    url "https://files.pythonhosted.org/packages/c3/b2/bc9c9196916376152d655522fdcebac55e66de6603a76a02bca1b6414f6c/pygments-2.20.0.tar.gz"
    sha256 "6757cd03768053ff99f3039c1a36d6c0aa0b263438fcab17520b30a303a82b5f"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/c0/8f/0722ca900cc807c13a6a0c696dacf35430f72e0ec571c4275d2371fca3e9/rich-15.0.0.tar.gz"
    sha256 "edd07a4824c6b40189fb7ac9bc4c52536e9780fbbfbddf6f1e2502c31b068c36"
  end

  resource "shellingham" do
    url "https://files.pythonhosted.org/packages/58/15/8b3609fd3830ef7b27b655beb4b4e9c62313a4e8da8c676e142cc210d58e/shellingham-1.5.4.tar.gz"
    sha256 "8dbca0739d487e5bd35ab3ca4b36e11c4078f3a234bfce294b0a0291363404de"
  end

  resource "typer" do
    url "https://files.pythonhosted.org/packages/e4/51/9aed62104cea109b820bbd6c14245af756112017d309da813ef107d42e7e/typer-0.25.1.tar.gz"
    sha256 "9616eb8853a09ffeabab1698952f33c6f29ffdbceb4eaeecf571880e8d7664cc"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"diffoscope", "--help"
    system bin/"container-diffoscope", "--help"
  end
end
