{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};
      in rec {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            (pkgs.python3.withPackages (pp: [
              pp.httpx
              pp.aiofiles
              pp.tqdm
            ]))
          ];
        };
      }
    );
}
