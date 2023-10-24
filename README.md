<h1 align="center"> RegulonDB HT ETL </h1>
<p align="center" >
  <img alt="RegulonDB Logo" style="width:50%;height:25%;" src="https://drive.google.com/uc?export=view&id=1BtKqNvtchMidDMUSyeJZPCnfMb-saaYm"></img>
</p>

[![License](https://img.shields.io/badge/license-MIT-brightgreen?style=plastic)](LICENSE)
[![RegulonDBVersion](https://img.shields.io/badge/RegulonDB_version-12.0-blue?style=plastic)](https://regulondb.ccg.unam.mx/)
[![EcocycVersion](https://img.shields.io/badge/last_Ecocyc_version_tested-27.0-red?style=plastic)](https://ecocyc.org/)
[![Status](https://img.shields.io/badge/release_1.0.0-yellowgreen?style=plastic)](CHANGELOG.md)

This software is used for the extraction and processing of diferent collections of HT Datasets.

## System requirements

- Software:
  - [Python 2.7](https://www.python.org/)
  - [Python 3.10](https://www.python.org/) or above
  - [Snakemake 7.14.0](https://snakemake.readthedocs.io/en/stable/#)
  - [Pandas 1.3.4](https://pandas.pydata.org/)
  - [Biopython 1.79](https://biopython.org/docs/1.79/api/Bio.html)
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

- [User Manual](docs/MU)
- [Operation Manual](docs/MO)
- [Maintenance Manual](docs/MM)

## Project website

[RegulonDB WebSite](https://regulondb.ccg.unam.mx/)

## License

RegulonDB Ecocyc Extractor is [Apache 2.0 licensed](LICENSE).

## Support contact information

[Support contact](https://regulondb.ccg.unam.mx/menu/about_regulondb/contact_us/index.jsp)

## Software quality checklist

**Accessibility**

<!--  - [ ] Unique DOI [identifier](http://....) (Please update identifier and link) -->
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
