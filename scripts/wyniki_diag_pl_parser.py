from bs4 import BeautifulSoup
import pandas as pd
import os as os

# HTML parser of wyniki.diag.pl to extract blood tests results to csv file quickly and use for further analyzing for example in ChatGPT
# I made this script because I was too lazy about manual copy/paste job and processing of data from generated PDFs by diag.pl was very crappy.
# Even AI wasn't able to parse those PDFs correctly. To parse your blood tests results just login to wyniki.diag.pl, show results of your test,
# open website inspection, navigate to respective div by first name of your tested parameter and copy whole div with class="table__content" which
# should contain list of your parameters with their result to the file saved as blood_tests.html. You can put results from multiple tests in
# single file as well
file_path = "blood_tests.html"
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parsing of HTRML content
soup = BeautifulSoup(html_content, "html.parser")

# Extracting of table rows containing data
table_rows = soup.find_all("div", class_="table__row")

# Extracting of desired blood test parameter names with their results
data = []

for row in table_rows:
    parameter_cell = row.find("div", class_="table__cell table__cell--param-name")
    result_cells = row.find_all("div", class_="table__cell")

    if len(result_cells) > 2:
        result_cell = result_cells[1]
        reference_cell = result_cells[2]

        parameter = parameter_cell.text.strip() if parameter_cell else "N/A"
        result = result_cell.text.strip() if result_cell else "N/A"
        reference = reference_cell.text.strip() if reference_cell else "N/A"

        if parameter != "N/A":
            parameter = parameter.replace(parameter[:8], '')
            parameter = parameter.strip()

        if result != "N/A":
            result = result.replace("Co to znaczy?", '')
            result = result.strip()


        data.append({"Parametr": parameter, "Wynik": result, "Zakres referencyjny": reference})

# Data transformation into DataFrame Pandas
df = pd.DataFrame(data)

# Print the output table
print(df)

# Save the results into CSV
outname = "wyniki_badan.csv"
outdir = "./wyniki"

if not os.path.exists(outdir):
    os.mkdir(outdir)

df.to_csv(os.path.join(outdir, outname), index=False, encoding="utf-8")
print("Dane zapisano do pliku wyniki_badan.csv")
