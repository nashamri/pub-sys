{
  description = "A Nix-flake-based Python development environment";

  inputs.nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*.tar.gz";

  outputs = { self, nixpkgs, }:
    let
      supportedSystems = [

        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"

      ];
      forEachSupportedSystem = f:
        nixpkgs.lib.genAttrs supportedSystems
        (system: f { pkgs = import nixpkgs { inherit system; }; });
    in {

      packages = forEachSupportedSystem ({ pkgs }: {
        django-bulma = pkgs.callPackage ./packages/django-bulma.nix { };
      });
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs;
            [

              python312
              ruff-lsp
              uv
              djlint
              sqlitestudio

            ] ++ (with pkgs.python312Packages; [

              pip
              django
              django-types
              django-crispy-forms
              self.packages.x86_64-linux.django-bulma

            ]);
        };
      });
    };
}
