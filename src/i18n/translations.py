"""Bilingual (EN/SV) translations for MaxOvertime."""

from __future__ import annotations

_TRANSLATIONS: dict[str, dict[str, str]] = {
    # Navbar
    "app.title": {
        "en": "Max Overtime",
        "sv": "Max Overtime",
    },
    "app.subtitle": {
        "en": "Variant Allele Frequency Tracker",
        "sv": "Variantallelfrekvens-spårare",
    },
    # Navigation
    "nav.analysis": {
        "en": "Analysis",
        "sv": "Analys",
    },
    "nav.tutorial": {
        "en": "Tutorial",
        "sv": "Tutorial",
    },
    "disclaimer.text": {
        "en": "Max Overtime. For research use and clinical decision support only. Not a standalone diagnostic device. Outputs may be incomplete or incorrect and must be reviewed by qualified experts in the full clinical, laboratory, and histopathological context. The authors assume no responsibility for clinical decisions or other consequences of use.",
        "sv": "Max Overtime. Endast för forskningsbruk och kliniskt beslutsstöd. Inte ett fristående diagnostiskt verktyg. Resultat kan vara ofullständiga eller felaktiga och måste granskas av kvalificerade experter i fullständigt kliniskt, laboratoriemässigt och histopatologiskt sammanhang. Författarna tar inget ansvar för kliniska beslut eller andra konsekvenser av användning.",
    },
    # Upload section
    "upload.section_label": {
        "en": "Data Input",
        "sv": "Datainmatning",
    },
    "upload.heading": {
        "en": "Upload Variant Files",
        "sv": "Ladda upp variantfiler",
    },
    "upload.subtitle": {
        "en": "Configure timepoints and upload one variant file per timepoint.",
        "sv": "Konfigurera tidpunkter och ladda upp en variantfil per tidpunkt.",
    },
    "upload.sample_id": {
        "en": "Sample ID",
        "sv": "Prov-ID",
    },
    "upload.sample_id_placeholder": {
        "en": "e.g. AML_2024_001",
        "sv": "t.ex. AML_2024_001",
    },
    "upload.timepoint": {
        "en": "Timepoint",
        "sv": "Tidpunkt",
    },
    "upload.date": {
        "en": "Date",
        "sv": "Datum",
    },
    "upload.drop_file": {
        "en": "Drop file or click to browse",
        "sv": "Släpp fil eller klicka för att bläddra",
    },
    "upload.supported_formats": {
        "en": "VCF, MAF, TSV, CSV",
        "sv": "VCF, MAF, TSV, CSV",
    },
    "upload.add_timepoint": {
        "en": "Add timepoint",
        "sv": "Lägg till tidpunkt",
    },
    "upload.analyze": {
        "en": "Run Analysis",
        "sv": "Kör analys",
    },
    "upload.remove": {
        "en": "Remove",
        "sv": "Ta bort",
    },
    "upload.min_timepoints": {
        "en": "At least 2 timepoints are required.",
        "sv": "Minst 2 tidpunkter krävs.",
    },
    "upload.file_uploaded": {
        "en": "File uploaded",
        "sv": "Fil uppladdad",
    },
    # Results section
    "results.heading": {
        "en": "Results",
        "sv": "Resultat",
    },
    "results.vaf_axis": {
        "en": "Variant Allele Frequency (%)",
        "sv": "Variantallelfrekvens (%)",
    },
    "results.plot_title": {
        "en": "VAF Over Time",
        "sv": "VAF över tid",
    },
    "results.download_pdf": {
        "en": "PDF Report",
        "sv": "PDF-rapport",
    },
    "results.download_excel": {
        "en": "Excel",
        "sv": "Excel",
    },
    "results.download_tsv": {
        "en": "TSV Data",
        "sv": "TSV-data",
    },
    "results.export": {
        "en": "Export",
        "sv": "Exportera",
    },
    # Variant table
    "table.heading": {
        "en": "Variant Table",
        "sv": "Varianttabell",
    },
    "table.select": {
        "en": "Plot",
        "sv": "Plotta",
    },
    "table.gene": {
        "en": "Gene",
        "sv": "Gen",
    },
    "table.transcript": {
        "en": "Transcript",
        "sv": "Transkript",
    },
    "table.protein_change": {
        "en": "Protein Change",
        "sv": "Proteinförändring",
    },
    "table.chrom": {
        "en": "Chr",
        "sv": "Krom",
    },
    "table.pos": {
        "en": "Position",
        "sv": "Position",
    },
    "table.hint": {
        "en": "Select rows to update the plot. All variants are selected by default.",
        "sv": "Markera rader för att uppdatera diagrammet. Alla varianter är markerade som standard.",
    },
    # Errors
    "error.parse_failed": {
        "en": "Failed to parse file: {detail}",
        "sv": "Kunde inte tolka filen: {detail}",
    },
    "error.no_variants": {
        "en": "No variants found in the uploaded files.",
        "sv": "Inga varianter hittades i de uppladdade filerna.",
    },
    "error.missing_files": {
        "en": "Please upload files for all timepoints.",
        "sv": "Vänligen ladda upp filer för alla tidpunkter.",
    },
    "error.missing_dates": {
        "en": "Please set dates for all timepoints.",
        "sv": "Vänligen ange datum för alla tidpunkter.",
    },
    "error.missing_sample_id": {
        "en": "Please enter a sample ID.",
        "sv": "Vänligen ange ett prov-ID.",
    },
    # Tutorial
    "tutorial.hero.title": {
        "en": "How to Use Max Overtime",
        "sv": "Så använder du Max Overtime",
    },
    "tutorial.hero.subtitle": {
        "en": "Track variant allele frequencies across sequential samples to monitor clonal evolution, treatment response, and disease progression.",
        "sv": "Spåra variantallelfrekvenser över sekventiella prover för att följa klonal evolution, behandlingssvar och sjukdomsprogression.",
    },
    "tutorial.workflow.title": {
        "en": "Workflow",
        "sv": "Arbetsflöde",
    },
    "tutorial.workflow.s1": {
        "en": "Prepare",
        "sv": "Förbered",
    },
    "tutorial.workflow.s2": {
        "en": "Upload",
        "sv": "Ladda upp",
    },
    "tutorial.workflow.s3": {
        "en": "Analyze",
        "sv": "Analysera",
    },
    "tutorial.workflow.s4": {
        "en": "Export",
        "sv": "Exportera",
    },
    "tutorial.step1.title": {
        "en": "Prepare Your Files",
        "sv": "Förbered dina filer",
    },
    "tutorial.step1.desc": {
        "en": "Max Overtime accepts variant call files in several standard formats. Each file represents one timepoint of sequencing data.",
        "sv": "Max Overtime accepterar variantfiler i flera standardformat. Varje fil representerar en tidpunkt av sekvenseringsdata.",
    },
    "tutorial.format.vcf.title": {
        "en": "VCF",
        "sv": "VCF",
    },
    "tutorial.format.vcf.desc": {
        "en": "Variant Call Format. Standard output from variant callers (GATK, Mutect2, VarDict). VAF is extracted from FORMAT fields: AF, AD, or DP.",
        "sv": "Variant Call Format. Standardutdata från variantanropare (GATK, Mutect2, VarDict). VAF extraheras från FORMAT-fält: AF, AD eller DP.",
    },
    "tutorial.format.maf.title": {
        "en": "MAF",
        "sv": "MAF",
    },
    "tutorial.format.maf.desc": {
        "en": "Mutation Annotation Format. Used by cBioPortal, GDC, and TCGA. VAF is computed from t_alt_count and t_ref_count columns.",
        "sv": "Mutation Annotation Format. Används av cBioPortal, GDC och TCGA. VAF beräknas från kolumnerna t_alt_count och t_ref_count.",
    },
    "tutorial.format.tsv.title": {
        "en": "TSV / CSV",
        "sv": "TSV / CSV",
    },
    "tutorial.format.tsv.desc": {
        "en": "Tab- or comma-separated files with flexible column naming. Required columns: chromosome, position, ref, alt. VAF column or count columns for computation.",
        "sv": "Tabb- eller kommaseparerade filer med flexibel kolumnnamning. Obligatoriska kolumner: kromosom, position, ref, alt. VAF-kolumn eller räknekolumner för beräkning.",
    },
    "tutorial.step2.title": {
        "en": "Set Up Timepoints",
        "sv": "Ställ in tidpunkter",
    },
    "tutorial.step2.desc": {
        "en": "Enter a sample ID, then configure at least two timepoints. For each timepoint, set the sampling date and upload the corresponding variant file. Use the + button to add more timepoints.",
        "sv": "Ange ett prov-ID och konfigurera minst två tidpunkter. Ange provtagningsdatum och ladda upp motsvarande variantfil för varje tidpunkt. Använd +-knappen för att lägga till fler tidpunkter.",
    },
    "tutorial.step2.tip": {
        "en": "Dates are used for the X-axis of the plot. Accurate dates ensure correct spacing between timepoints.",
        "sv": "Datum används för X-axeln i diagrammet. Korrekta datum säkerställer rätt avstånd mellan tidpunkter.",
    },
    "tutorial.step3.title": {
        "en": "Analyze & Interpret",
        "sv": "Analysera och tolka",
    },
    "tutorial.step3.desc": {
        "en": "Click \"Run Analysis\" to parse all files and match variants across timepoints. Variants are matched by genomic coordinates (chromosome, position, reference allele, alternate allele).",
        "sv": "Klicka på \"Kör analys\" för att tolka alla filer och matcha varianter över tidpunkter. Varianter matchas via genomiska koordinater (kromosom, position, referensallel, alternativ allel).",
    },
    "tutorial.step3.plot": {
        "en": "The plot shows VAF (%) on the Y-axis and date on the X-axis. Each line represents one variant. Hover over points to see gene name, VAF, sequencing depth, and protein change.",
        "sv": "Diagrammet visar VAF (%) på Y-axeln och datum på X-axeln. Varje linje representerar en variant. Hovra över punkter för att se gennamn, VAF, sekvenseringsdjup och proteinförändring.",
    },
    "tutorial.step3.table": {
        "en": "The variant table shows all detected variants in wide format with VAF and depth per timepoint. Select or deselect rows to control which variants appear in the plot.",
        "sv": "Varianttabellen visar alla detekterade varianter i brett format med VAF och djup per tidpunkt. Markera eller avmarkera rader för att styra vilka varianter som visas i diagrammet.",
    },
    "tutorial.step4.title": {
        "en": "Export Results",
        "sv": "Exportera resultat",
    },
    "tutorial.step4.desc": {
        "en": "Download your results in multiple formats for reporting, further analysis, or archiving.",
        "sv": "Ladda ner dina resultat i flera format för rapportering, vidare analys eller arkivering.",
    },
    "tutorial.step4.pdf": {
        "en": "High-resolution vector PDF of the VAF plot, suitable for publications and clinical reports.",
        "sv": "Högupplöst vektor-PDF av VAF-diagrammet, lämplig för publikationer och kliniska rapporter.",
    },
    "tutorial.step4.excel": {
        "en": "Excel workbook with a wide-format table showing VAF% (depth) per timepoint per variant.",
        "sv": "Excel-arbetsbok med en bredformatstabell som visar VAF% (djup) per tidpunkt per variant.",
    },
    "tutorial.step4.tsv": {
        "en": "Tab-separated long-format data with all fields, suitable for downstream bioinformatic analysis.",
        "sv": "Tabbseparerad data i långformat med alla fält, lämplig för nedströms bioinformatisk analys.",
    },
    "tutorial.back": {
        "en": "Back to Analysis",
        "sv": "Tillbaka till analys",
    },
    "tutorial.column_reqs": {
        "en": "Column Requirements",
        "sv": "Kolumnkrav",
    },
    "tutorial.col.required": {
        "en": "Required",
        "sv": "Obligatorisk",
    },
    "tutorial.col.recommended": {
        "en": "Recommended",
        "sv": "Rekommenderad",
    },
    "tutorial.col.optional": {
        "en": "Optional",
        "sv": "Valfri",
    },
}


def t(key: str, lang: str = "en", **kwargs: str) -> str:
    """Look up a translated string.

    Parameters
    ----------
    key : str
        Dot-notation key, e.g. 'upload.heading'.
    lang : str
        Language code, 'en' or 'sv'.
    **kwargs
        Format parameters for string interpolation.

    Returns
    -------
    str
        Translated string, falling back to English, then to the key itself.
    """
    entry = _TRANSLATIONS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry.get("en") or key
    if kwargs:
        text = text.format(**kwargs)
    return text
