{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  env = {
    PGHOST = "localhost";
    PGPORT = "5555";
    PGDATABASE = "postgres";
    PGUSER = "postgres";
    PGPASSWORD = "123";
  };

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
