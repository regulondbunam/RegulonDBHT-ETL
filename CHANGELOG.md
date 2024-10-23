# RegulonDB HT ETL

This version solves the changes on RegulonDB 13.5.0

## [2.0.0](https://github.com/regulondbunam/RegulonDBHT-ETL/releases/tag/2.0.0) - 2024-10-24
New updates in the input data requires constantly software updates and code was not properly modulated, now to avoid future problems in maintenance we decide to rework the full code and make it more dev friendly.

### Added

- **Feb, 2024**
- Publications from datasets pmids can be extracted.
- Source Serie object.
- ObjectTested object.
- ObjectTested Genes.
- Sample object.
- LinkedDatasets object.
- ReleaseControl object.
- Temporal ID property.
- Reference Genome property.
- Assembly Genome ID property.
- Five Prime Enrichment property.
- Experiment Condition property.
- Cut Off property.
- Public Notes property.
- Source Reference Genome property.
- Collection Data object property.
- Metadata object property.
- **Mar, 2024**
- Final JSON file are generated with respective names.
- External Reference property added to dataset object.
- **Aug, 2024**
- Metadata objects now have an ID.
- New utility function added, find_many_in_dict_list(), Finds dictionaries in a dictionary List by certain key.
- **Oct, 2024**
- Growth Conditions function that process GC from dataset metadata.
- Objects Tested now have AbbName property.

### Changed

- **Feb, 2024**
- New code structure is now implemented.
- **Mar, 2024**
- DB Links field contains DBName and DBLink
- **Apr, 2024**
- Properties that returns a dictionary now are assembled in an upper level.
- Authors Data is processed in the dataset object.
- Uniformized Data is processed in the dataset object, tfBinfings (sites, peaks) ready.
- **May, 2024**
- Uniformized Data is processed in the dataset object, TUs ready.
- Uniformized Data is processed in the dataset object, TSS ready.
- Uniformized Data is processed in the dataset object, TTS ready.
- Uniformized Data is processed in the dataset object, multiple sources ready.
- Utils module cleaned, repeated functions, functions that must be classes and unused functions.
- Added modules for Gene Expression processing with the uniformized data.
- Added class Summary, there are properties to define that need to be reviewed by the project manager.
- **Aug, 2024**
- GeneExpression's IDs are now more readable, removed properties without values.
- Snakemake Config files modified to adjust for new project schema.
- **Oct, 2024**
- Update Gene Expression Temp ID and ID format.

### Deprecated

- Old code structure.

### Removed

- **May, 2024**
- src/ht_etl/dataset_metadata.py
- src/ht_etl/peaks_datasets.py
- src/ht_etl/sites_dataset.py
- src/ht_etl/tss_datasets.py
- src/ht_etl/tts_datasets.py
- src/ht_etl/tu_datasets.py
- src/ht_etl/gene_expression_dataset_metadata.py
- src/ht_etl/gene_exp_datasets.py
- src/ht_etl/nlp_growth_conditions.py

### Fixed

- **Feb, 2024**
- ObjectTested returned null objects that can't be read and have to be a list.
- ObjectTested tried to process TF that doesn't exist.
- **Mar,2024**
- Sample Replicates IDs and Linked Datasets now are List of List of IDs.
- **Aug, 2024**
- TUs objects were missing name. Added.
- Sites' left and right position were String instead of Integer. Fixed
- NLP_GC's terms were not object arrays, temporal_id were generating wrong, dataset ids does not match with correspond Dataset ID. Fixed.
- GeneExpression's temporal_id were generating wrong, dataset ids does not match with correspond Dataset ID. Fixed.
- Uniformized_Data Domain Objects Base were not adding dataset_ids. Fixed.
- Uniformized_Data Peaks and Sites were not adding dataset_ids. Fixed
- Uniformized_Data TSS, TTS and TU LeftEnd and RightEnd properties were wrong written. Fixed
- ObjectTested externalCrossReferenceID property were wrong written. Fixed
- Genes were not generating correctly geneNames. Fixed
- Many JSON files were generated with incorrect properties. Fixed

### Security

- Without changes.
