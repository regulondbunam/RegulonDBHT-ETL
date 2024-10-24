# standard
import argparse

# third party


# local


def get_arguments():
    """
    Defines the arguments that the program will support.

    Returns:
        arguments: argparse Object, defined arguments for the execution of the program.
    """

    # ARGUMENTS DESCRIPTION

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="HT ETL",
        epilog="You need to provided at least one entity argument(--datasets, --tfbinding, etc...)")

    # GENERAL ARGUMENTS

    parser.add_argument(
        "-dbout",
        "--databaseout",
        help="Name of the output database where will be written.",
        choices=["regulondbmultigenomic", "regulondbht", "regulondbdatamarts"],
        default="regulondbht",
        metavar="regulondbht",
    )

    parser.add_argument(
        "-collection",
        "--collection-path",
        help="Path to read de origin files data.",
        metavar="../InputData/",
        default="../InputData/",
    )

    parser.add_argument(
        "-in",
        "--input",
        help="Path to read de origin file data.",
        metavar="../InputData/",
        default="../InputData/",
    )

    parser.add_argument(
        "-col",
        "--collection-name",
        help="Collection name.",
        metavar="ChIP-seq",
        default="ChIP-seq",
    )

    parser.add_argument(
        "-au",
        "--author",
        help="Path to read de authors' origin files.",
        metavar="../InputData/",
        default="../InputData/",
    )

    parser.add_argument(
        "-bed",
        "--bed",
        help="Path to read de bed dataset files.",
        metavar="../InputData/",
        default="../InputData/",
    )

    parser.add_argument(
        "-out",
        "--output",
        help="Path where the json files of the process will be stored.",
        metavar="../RawData/",
        default="../RawData/",
    )

    parser.add_argument(
        "-l",
        "--log",
        help="Path where the log of the process will be stored.",
        metavar="../logs/ht_etl_log/",
        default="../logs/ht_etl_log/",
    )

    parser.add_argument(
        "-r",
        "--report",
        help="Path where the report of the process will be stored.",
        metavar="../logs/ht_etl_log/",
        default="../logs/ht_etl_log/",
    )

    parser.add_argument(
        "-org",
        "--organism",
        help="Organism whose information is been downloaded.",
        default="ECOLI",
        metavar="ecoli",
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Imput Data Verison.",
        default="0.0.0",
        metavar="0.0.0",
    )

    parser.add_argument(
        "-dstype",
        "--dataset-type",
        help="Dataset record source name.",
        choices=["TFBINDING", "RNAP_BINDING_SITES", "GENE_EXPRESSION",
                 "TSS", "TUS", "TTS", "REGULONS", "GSELEX"]
    )

    parser.add_argument(
        "-colltype",
        "--collection-type",
        help="Collection type name.",
        default="CHIP_SEQ",
        metavar="ChIP_SEQ"
    )

    parser.add_argument(
        "-collsrc",
        "--collection-source",
        help="Collection source name.",
        default="REGULONDB",
        metavar="REGULONDB"
    )

    parser.add_argument(
        "-status",
        "--collection-status",
        help="Collection status.",
        choices=["DEPRECATED", "CURRENT"],
        default="CURRENT",
        metavar="CURRENT"
    )

    parser.add_argument(
        "-email",
        "--email",
        help="User email address to connect to PUBMED database.",
        default="reguadm@ccg.unam.mx",
        metavar="reguadm@ccg.unam.mx",
    )

    parser.add_argument(
        "-u",
        "--url",
        help="URL to DB server.",
        default="mongodb://localhost",
        metavar="mongodb://localhost",
    )

    parser.add_argument(
        "-db",
        "--database",
        help="Name of the database where IDs are taken.",
        choices=["regulondbmultigenomic", "regulondbht", "regulondbdatamarts"],
        default="regulondbmultigenomic",
        metavar="regulondbmultigenomic",
    )

    parser.add_argument(
        "-bnum",
        "--bnumbers",
        help="Path to get bnumbers from mg database.",
        metavar="./config/bnumbers.json",
        default="./config/bnumbers.json",
    )

    # COLLECTIONS ARGUMENTS

    parser.add_argument(
        "-sheet",
        "--sheet",
        help="URL to DB server.",
        default="DATASET",
        metavar="DATASET",
    )

    parser.add_argument(
        "-rows",
        "--rows-to-skip",
        help="URL to DB server.",
        default=1,
    )

    arguments = parser.parse_args()

    return arguments


def load_arguments():
    """
    Load the arguments that the program will support.

    Returns:
        arguments: argparse Object, loaded arguments for the execution of the program.
    """

    arguments = get_arguments()
    return arguments
