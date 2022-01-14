# User Manual RegulonDB HT ETL

## Introduction

The Snakemake script for the MCO data upload process was thought to make uploading data to RegulonDB Multigenomic faster and more controlled, due to the modular nature of Snakemake allows the upload process to be carried out from any computer that meets the execution requirements but without the need to configure its _Python_ environment for each of the data load modules.

## Snakefile run

To run the Snakefile script you must follow the following steps.

- Run the complete script:

```shell
$ snakemake -s mco_Snakefile --cores 1 --use-conda
```

The `-s` parameter is the name of the Snakefile script.
The option `--cores` indicates how many cores of the computer will be used to process the script, it is recommended to indicate them to avoid problems when executing.
The `--use-conda` option is used to indicate that the _conda_ environment is used to download the necessary modules and create sandboxes.

- Run the script as a test:

```shell
$ snakemake -s mco_Snakefile --cores 1 --use-conda -n
```

The `-n` parameter indicates that a clean test execution will be run showing the jobs to be executed or if there is a problem with the script.

- Execute only one rule:

```shell
$ snakemake -s mco_Snakefile --cores 1 --use-conda -R [my_rule]
```

The parameter `-R` indicates the name of the _rule_ that you want to execute, you can put several and they will be executed in the order given.

- Run the script forcibly:

```shell
$ snakemake -s mco_Snakefile --cores 1 --use-conda -f
```

The `-f` parameter is to perform a forced execution, in case the output files have already been generated to execute the script or a single rule.

- Run script and generate a report:

```shell
$ snakemake -s mco_Snakefile --cores 1 --use-conda -report
```

The `-report` parameter is used to generate a report, in html format, of the execution of the script with the memory data and the _log_ in general in a graphical presentation.

## Mco_etl module

The MCO data extraction module has console parameter handling, for a better use of it you can follow these recommendations (only for isolated execution of the module outside the script):

- `" -i "," --inputfile "," Input Ontology file name "` Indicates the input file, the ontology in `.owl` format.
- `" -o "," --outputfile "," Output Ontology terms file name "` Indicates the name of the `JSON` file to output the ontology terms, by default` mco_terms.json`.
- `" -m "," --metadatafile "," Output Ontology metadata file name "` Indicates the name of the `JSON` output file of the ontology metadata, by default` mco_ontology.json`.
- `" -u "," --url "," Input Ontology source "` In case the ontology is found on the internet, this parameter indicates the url to be used in the process. This parameter is still unstable due to the lack of stanarization in the creation of ontologies.
- `" -l "," --log "," Log file name "` Indicates the name of the log file.
- `" -s "," --schemaversion "," Schema Version "` Indicates the version of the schema that will be used for data validation.
  For this module the library [`Owlready2`](https://pypi.org/project/Owlready2/) is needed, which is the one that allows the reading of the` .owl` ontology, if the module is executed with the Snakefile script It is not necessary to install it on your computer directly, you only need to indicate in the file `envs/et_tools` the name and version of the library.

```yaml
channels:
  - bioconda
  - conda-forge
dependencies:
  - owlready2
```

## Definitions, acronyms and abbreviations

**MCO** - Microbial Condition Ontology
**[Snakemake](https://snakemake.readthedocs.io/en/stable/)** - The Snakemake workflow management system is a tool to create reproducible and scalable data analyses. Workflows are described via a human readable, Python based language.
**[Owlready2](https://pypi.org/project/Owlready2/)** - Owlready2 is a module for ontology-oriented programming in Python 3, including an optimized RDF quadstore.

## Help and Support

If you have a problem or suggestion of any kind related to what is described in this manual, you can send an email to: [regusoft@ccg.unam.mx](mailto:regusoft@ccg.unam.mx)

The documents mentioned as reference in this manual may be requested through the aforementioned address.

## Bibliographic references

**Websites**
Website title: Snakemake
Web link: [https://snakemake.readthedocs.io/en/stable/](https://snakemake.readthedocs.io/en/stable/)
Website title: Owlready2 0.26
Web link: [https://pypi.org/project/Owlready2/](https://pypi.org/project/Owlready2/)

<!---
  HISTORIAL DE REVISIONES

  **Fecha:** 26/01/2021
  **Versión:** 1.0
  **Descripción:** Creación de manual de mantenimiento
  **Realizado por: ** Felipe Betancourt Figueroa
  **Estado:** Sin revisar

  **Fecha:** [dd/mm/aaaa]
  **Versión:** [#.#]
  **Descripción:** [Indicar los cambios que se realizaron en el documento]
  **Realizado por: ** [Nombre de la persona que realice los cambios]
  **Estado:**[Revisión <Trabajado,  Verificado>, Estable **<**Vo.Bo, Validado>]
  [Repetir esta sección por cada versión que se realice en el documento]
-->
