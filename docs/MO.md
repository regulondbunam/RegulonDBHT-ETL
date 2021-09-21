# Operation Manual RegulonDB HT ETL

## Introduction to the system

The Snakemake script for the MCO data upload process was thought to make uploading data to RegulonDB Multigenomic faster and more controlled, due to the modular nature of Snakemake allows the upload process to be carried out from any computer that meets the execution requirements but without the need to configure its _Python_ environment for each of the data load modules.

## Hardware Recommendations

- RAM: 6 GB
- Storage: 500 MB

## Software Requirements

- Operating System Linux/Unix (recommended)
- Python 3.9
- Snakemake

## Installation Instructions

It is not necessary to carry out an installation, but it is necessary to place all the modules of the process with the directory structure of the diagram [Directory structure](../diagrams/mco-etl-directory-structure.png) so that you have a better control from the Snakefile.

## Common problems

The problem of desicronization of _Rules_ can occur, which are those that control the execution of the modules in the correct order, if a module is executed earlier than expected it may have problems executing the next one since it depends on the files that the previous one generates.
It is recommended in the **_rule:_** to put a parameter **_priority:_** so that they are executed in order, keep in mind that the priority is higher the higher the value of the number that is specified.

```python
rule mcoet:
	priority: 10
```

## Definitions, acronyms and abbreviations

**MCO** - Microbial Condition Ontology
**[Snakemake](https://snakemake.readthedocs.io/en/stable/)** - The Snakemake workflow management system is a tool to create reproducible and scalable data analyses. Workflows are described via a human readable, Python based language.

## Help and Support

If you have a problem or suggestion of any kind related to what is described in this manual, you can send an email to: [regusoft@ccg.unam.mx](mailto:regusoft@ccg.unam.mx)

The documents mentioned as reference in this manual may be requested through the aforementioned address.

## Bibliographic references

**Websites**
Website title: Snakemake
Web link: [https://snakemake.readthedocs.io/en/stable/](https://snakemake.readthedocs.io/en/stable/)

<!--
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
