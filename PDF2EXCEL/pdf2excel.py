import tabula

# convert PDF into CSV
tabula.convert_into("your_PDF.pdf", "output.xls", output_format="xls", pages='all', lattice=True)

# convert all PDFs in a directory
#tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all)# Read pdf into DataFrame

# Using DataFrame for further analysis
df = tabula.read_pdf("PDF_File", pages='all')
