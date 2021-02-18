import json
import logging
import os
import re
import zipfile

import xmltodict
from slugify import slugify

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w");

class Epub:
    def __init__(self, path):
        self.path_book = path;
        self.filename = util.get_name(os.path.basename(path));
        self.extension = util.get_extension(os.path.basename(path));

        with zipfile.ZipFile(self.path_book, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zip_file:

            container = xmltodict.parse(zip_file.read("META-INF/container.xml").decode("utf-8"));
            full_path = container["container"]["rootfiles"]["rootfile"]["@full-path"];

            self.dir_content = os.path.dirname(full_path);
            self.content = xmltodict.parse(zip_file.read(full_path).decode("utf-8"));

            self.title = self._get_value(self.content["package"]["metadata"]["dc:title"]);

        self.get_and_save_cover();

    def get_and_save_cover(self):
        path_cover_epub = self._get_path_cover();
        extension = util.get_extension(path_cover_epub);
        self.path_cover = configuration["PATH_COVERS"] + slugify(self.filename) + extension;

        try:
            with zipfile.ZipFile(self.path_book, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zip_file:
                with open(self.path_cover, "wb") as cover:
                    if self.dir_content != "":
                        cover.write(zip_file.read(self.dir_content + "/" + path_cover_epub));
                    else:
                        cover.write(zip_file.read(path_cover_epub));
        except Exception as error:
            logging.warning(f"The cover has not been saved. -> {error}");

    def get_page(self, page):
        pathTemp = os.getcwd() + configuration["PATH_TEMP"];
        all_data = [];

        for element in self.content["package"]["manifest"]["item"]:
            if "html" in element["@href"]:
                all_data.append(element["@href"]);

        try:
            with zipfile.ZipFile(self.path_book, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zip_file:
                data = zip_file.read(all_data[page]).decode("utf-8");
                data = data.replace("src=\"../", "src=\"");

                files = re.findall("src=['\"]([^'\"]+?)['\"]", data);
                for file_extract in files:
                    if not "http" in file_extract:
                        zip_file.extract(file_extract, pathTemp);
                
                data = data.replace("src=\"", f"src=\"{configuration['PATH_TEMP']}");

                return data;
        except Exception as error:
            logging.warning(f"Cannot read page {all_data[page]}. -> {error}");
            return "Page with some error. Check the log for more details.";

    def _get_path_cover(self):
        try:
            item_cover = "";
            metas = self.content["package"]["metadata"]["meta"];
            if isinstance(metas, list):
                for meta in metas:
                    if "@name" in meta:
                        if meta["@name"] == "cover":
                            item_cover = meta["@content"];
            else:
                item_cover = metas["@content"];

            for item in self.content["package"]["manifest"]["item"]:
                if item["@id"] == item_cover:
                    return item["@href"];
        except Exception as error:
            logging.warning(f"The cover has not been found. -> {error}");           

    def _get_value(self, content):
        if isinstance(content, list):
            values = []
            for element in content:
                values.append(element["#text"]);
            return values;
        else:
            if "#text" in content:
                return content["#text"];
            else:
                return content;
