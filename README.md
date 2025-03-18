<h1 align="center"> RegulonDB HT ETL </h1>
<p align="center" >
  <img alt="RegulonDB Logo" style="width:50%;height:25%;" src="docs/regulondb_logo.png"></img>
</p>

[![License](https://img.shields.io/badge/license-APACHE-brightgreen?style=plastic)](LICENSE)
[![RegulonDBVersion](https://img.shields.io/badge/RegulonDB_version-13.6-blue?style=plastic)](https://regulondb.ccg.unam.mx/)
[![EcocycVersion](https://img.shields.io/badge/last_Ecocyc_version_tested-28.5-red?style=plastic)](https://ecocyc.org/)
[![Status](https://img.shields.io/badge/release_2.0.1-yellowgreen?style=plastic)](CHANGELOG.md)

This software is used for the extraction and processing of diferent collections of HT Datasets.

## System requirements

- Software:
  - [Python 3.10](https://www.python.org/) or above
  - [Snakemake 7.14.0](https://snakemake.readthedocs.io/en/stable/#) or above
  - [Pandas 1.3.4](https://pandas.pydata.org/) or above
  - [Biopython 1.79](https://biopython.org/docs/1.79/api/Bio.html) or above
- Hardware:
  - RAM: 8 GB (minimal recommended)
  - Storage: 5 GB

## Install

[Install guide](INSTALL.md)

## Quick start

```shell
python src/ -h
```

## Manuals

- [User Manual](docs/MU.md)
- [Operation Manual](docs/MO.md)
- [Maintenance Manual](docs/MM.md)

## Project website

[RegulonDB WebSite](https://regulondb.ccg.unam.mx/)

## License

RegulonDB Ecocyc Extractor is [Apache 2.0 licensed](LICENSE).

## Support contact information

[Support contact](https://regulondb.ccg.unam.mx/manual/aboutUs/contact)

## Software quality checklist

**Accessibility**

<!--- [ ] Unique DOI [identifier](http://....) (Please update identifier and link) --->

- [x] Version control system

**Documentation**

- [x] README file

**Learnability**

- [x] Quick start

**Buildability**

- [x] INSTALL file

**Identity**

- [x] Website

**Copyright & Licensing**

- [x] LICENSE file

**Portability**

- [x] Multiple platforms

**Supportability**

- [x] E-mail address
- [x] Issue tracker

**Analysability**

- [x] Source code structured
- [x] Coding standards - [Google style guides](http://google.github.io/styleguide/) [Python style guide](https://pep8.org/#pep-8-%E2%80%94-the-style-guide-for-python-code)

**Changeability**

- [x] CONTRIBUTING file
- [x] Code of Conduct file
- [x] Code changes, and their authorship, publicly visible

**Reusability**

- [x] Source code set up in a modular fashion

**Security & Privacy**

- [x] Passwords must never be stored in unhashed form
