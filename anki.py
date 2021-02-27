import os


def uploadCard(name, page_num, notebook, bugged):
    front = '<img src="{}top.png">'.format(name) if not bugged else 'Non ho trovato la linea gialla :('
    back = ('<img src="{}down.png">'
            '<br>'
            '<span style="font-size:0.5em">pagina {}</span>').format(name, page_num)

    command = ("am broadcast -a com.elmoddy.cardmakerproxy.CREATE_CARD"
               "-e 'deck' '{}' -e 'front' '{}' -e 'back' '{}'").format(notebook, front, back)

    os.system(command)
