# Maintenance Manual RegulonDB HT ETL

## Introduction

This document describes the current status of the MCO-ETL system. The objective is to show and describe the internal structure of each of the components that make it up.

## System internal structure

The folder structure that makes up the system, as shown in the template in Figure 1, is made up of a directory where is the MCO data extraction program, written in _Python_, is called **mco_etl**, a directory configuration file for general data of the database and collections called **config**, a directory of configuration files for execution environments **envs**, a folder with the validation and data loading programs provided by the RegulonDB team **release_modules**, a directory **schemas** that contains the necessary schemas for data validation, a directory **input_files** with the files of the ontology to be read, in addition to folders of output where the resulting data and log files will be put.

![](../diagrams/mco-etl-directory-structure.png)
Figure 1. System folder organization

## Plugins and compatibility with other systems

Due to the nature of the _Snakemake_ system, there are no compatibility problems since the software necessary for the execution of the programs is installed locally in isolated environments, you simply need to have _Python3.8_ or higher to be able to install the _Snakemake_ system.

## Operation restrictions

In the _Windows_ operating system, the _Snakemake_ system usually gives problems to install it and also to create execution environments, so it is recommended to use a _Linux/Unix_ system or, failing that, the Windows Subsystem for Linux (WSL) that allows us to use the Terminal and Bash of _Linux_ from _Windows 10_ or install _Linux_ on a virtual machine. In this way we can use the Snakemake system to run and test the program.

## Suggestions for improvement

Within my recommendations, add a directory for local libraries in the root directory, since it has to be accessed from the path **.Snakemake/conda/\*.Yaml** which makes searching for a local library more confusing, at the moment this directory is in the path **release_modules/apis/**

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
