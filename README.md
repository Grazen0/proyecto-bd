# Proyecto BD

> [!NOTE] Nota importante
>
> La data generada con los scripts, como es muy grande para subirla a GitHub, se encuentra en este [link de Drive](https://drive.google.com/drive/folders/160GlLABwiquvY-NyMvyWOhCZ1Y0HsvAt?usp=sharing). Habiendo descargado la data, el directorio local `data` debería verse así:
>
> ```
> data
> ├── manual/
> │   ├── 01-rarities.csv
> │   └── 02-element_types.csv
> └── generated/
>     ├── 1k/
>     │   └── ...
>     ├── 10k/
>     │   └── ...
>     ├── 100k/
>     │   └── ...
>     └── 1000k/
>         └── ...
> ...
> ```

Este repo tiene una configuración de Docker Compose para iniciar un contenedor de PostgreSQL con un volumen configurado de `data/` a `/data`. Se puede iniciar con este comando:

```bash
docker compose up -d
```

La creación inicial, generación de datos y carga de los datos se hace con los scripts en `src/`. Porsiaca, incluimos un script `run_all.sh` que corre todo en orden.

El repo también incluye un `shell.nix` para reproducir el entorno de Python y PostgreSQL necesario para correr los scripts.

TLDR: Al final, esta secuencia de comandos debería funcionar:

```bash
nix-shell
docker compose up -d
./run_all.sh
```
