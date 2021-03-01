import page2img
import squid
import anki

if __name__ == '__main__':
    pages = squid.get_pages()
    for page in pages:
        name = page[0]
        page_num = page[1]
        notebook = page[2]
        is_new = page[3]

        bugged = page2img.handle_page(name)

        if is_new:
            anki.uploadCard(name, page_num, notebook, bugged)
            print("Nuova pagina ({}) in {}".format(page_num, notebook))
        else:
            print("Pagina {} modificata in {}".format(page_num, notebook))





