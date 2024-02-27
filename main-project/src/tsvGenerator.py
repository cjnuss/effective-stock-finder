import edgar

print("Generating TSV file...")
#Creates the tsv file
edgar.download_index("./src/newfiles", 2024, "Stock-Finder aery.2@osu.edu", skip_all_present_except_last=False)
print("Done!")