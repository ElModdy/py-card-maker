import page2img
import squid
import anki

if __name__ == '__main__':
    pages = squid.get_pages()
    for page in pages:
        name = page[0]
        page_num = page[1]
        notebook = page[2]

        bugged = page2img.handle_page(name)

        anki.uploadCard(name, page_num, notebook, bugged)





