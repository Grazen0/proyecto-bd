{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    postgresql
    (python3.withPackages (
      ps: with ps; [
        psycopg
        faker
      ]
    ))
  ];
}
