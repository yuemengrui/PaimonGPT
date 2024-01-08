# *_*coding:utf-8 *_*
# @Author : YueMengRui
from mylogger import logger
from info.libs.Knowledge_Base.text_splitter.chinese_text_splitter import ChineseTextSplitter
from langchain.document_loaders import UnstructuredFileLoader, TextLoader, UnstructuredMarkdownLoader, \
    UnstructuredPowerPointLoader, UnstructuredWordDocumentLoader, UnstructuredHTMLLoader, CSVLoader, \
    UnstructuredODTLoader
from .pdf_layout_loader import PDFLayoutLoader

LOADER_MAPPING = {
    "csv": (CSVLoader, {}),
    "doc": (UnstructuredWordDocumentLoader, {}),
    "docx": (UnstructuredWordDocumentLoader, {}),
    "html": (UnstructuredHTMLLoader, {}),
    "md": (UnstructuredMarkdownLoader, {}),
    "odt": (UnstructuredODTLoader, {}),
    "ppt": (UnstructuredPowerPointLoader, {}),
    "pptx": (UnstructuredPowerPointLoader, {}),
    "txt": (TextLoader, {"encoding": "utf8"}),
    # Add more mappings for other file extensions and loaders as needed
}


def load_file(filepath, ext=None, pdf=False, embedding_model=None):
    logger.info({'load_file': {'file_path': filepath, 'ext': ext}})
    if not ext:
        ext = filepath.lower().split('.')[-1]

    if ext == 'pdf':
        loader = PDFLayoutLoader()
        docs = loader.load(filepath, embedding_model=embedding_model)
    else:
        if ext in LOADER_MAPPING:
            loader_class, loader_args = LOADER_MAPPING[ext]
            loader = loader_class(filepath, **loader_args)
        else:
            logger.warning({'Unsupported file extension': '{}'.format(ext)})
            loader = UnstructuredFileLoader(filepath, mode="elements")

        textsplitter = ChineseTextSplitter(pdf=pdf)
        docs = loader.load_and_split(text_splitter=textsplitter)
        docs = [{'type': 'text', 'content': x.page_content, 'page': None} for x in docs]

    return docs
