{
  description = "Dev shell with Zed, Python, Node, and LSPs";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux"; # change if needed
      pkgs = import nixpkgs { inherit system; };
     python = pkgs.python3.withPackages (ps: with ps; [
        fastapi
        uvicorn
        pandas
        numpy
      ]);
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          # Editor
          zed-editor

          # Node ecosystem
          nodejs
          typescript
          typescript-language-server

          # Python ecosystem
          python
          python3Packages.pip
          python3Packages.virtualenv
          pyright
          ruff

          # General tools
          git
          curl
        ];

        shellHook = ''
          echo "🚀 Dev shell ready!"
          echo "Zed + Node + Python + LSPs"
        '';
      };
    };
}
