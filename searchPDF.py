# Adapted from https://glenzac.wordpress.com/2021/06/26/search-through-all-pdfs-in-a-folder-using-python/

import os
import re
import PyPDF2


def list_files(pdf_dir):
	return os.listdir(pdf_dir)


def search_all_files(pdf_list, pdf_dir, search_string):
	results = []
	for pdf in pdf_list:
		pdf_results = search_pdf(pdf, pdf_dir, search_string)
		if pdf_results:
			results.extend(pdf_results)

	return results


def search_pdf(pdf, pdf_dir, search_string):
	file_results = []
	pdf_obj = open("{d}/{f}".format(d=pdf_dir, f=pdf), 'rb')
	pdf_reader = PyPDF2.PdfReader(pdf_obj)
	for i in range(0, len(pdf_reader.pages)):
		search_result = search_page(pdf_reader.pages[i], i, search_string)
		if search_result:
			file_results.append(search_result)
	if len(file_results) > 0:
		file_results.insert(0, "\nFile: {}".format(pdf))
		return file_results
	else:
		return None


def search_page(page, page_num, search_string):
	page_text = page.extract_text()
	if page_text:
		res_search = re.search(search_string, page_text)
		if res_search:
			res_string = str(page_text[res_search.start() - 100:res_search.end() + 100]).replace("\n"," ")
			return "Found on page {p}: {r}".format(p=page_num, r=res_string)
	return None


def export_results(results, search_string):
	with open("{}-results.txt".format(search_string), "w", encoding="utf-8") as f:
		f.write("Results for search term {}".format(search_string))
		for result in results:
			f.write("{}\n".format(result))


search_string = input("Search term: ")
pdf_dir = "researchexpeditionpdfs"
pdf_list = list_files(pdf_dir)
results = search_all_files(pdf_list=pdf_list, pdf_dir=pdf_dir, search_string=search_string)
if len(results) > 0:
	export_results(results, search_string)
else:
	print("No results across all files.")
