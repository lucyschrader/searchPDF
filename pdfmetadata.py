import os
from PyPDF2 import PdfReader as pr
from tqdm import tqdm


def list_files(pdf_dir):
	return os.listdir(pdf_dir)


def collate_metadata(directory, files):
	collated_metadata = []
	for file in tqdm(files, desc="Checking files"):
		file_path = "{d}/{f}".format(d=directory,
		                             f=file)
		metadata = {}
		reader = pr(file_path)
		meta = reader.metadata
		metadata["filename"] = file
		metadata["filesize"] = round(os.stat(file_path).st_size / (1024 * 1024), 2)
		metadata["pagecount"] = len(reader.pages)
		collated_metadata.append(metadata)

	return collated_metadata


def print_metadata(metadata):
	report_rows = []
	for row in metadata:
		report_row = "Filename: {n}\tFilesize: {s} MB\tPage count: {p}\n".format(n=row["filename"],
		                                                                         s=row["filesize"],
		                                                                         p=row["pagecount"])
		report_rows.append(report_row)
	with open("document_metadata.txt", "w+", encoding="utf-8") as f:
		f.writelines(report_rows)


def run():
	pdf_dir = "researchexpeditionpdfs"
	files = list_files(pdf_dir)
	pdf_metadata = collate_metadata(pdf_dir, files)
	print_metadata(pdf_metadata)


if __name__ == "__main__":
	run()
