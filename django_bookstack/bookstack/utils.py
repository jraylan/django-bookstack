
from django_bookstack.bookstack import library


def get_page_by_name(page_name, using):
    '''
    Returns the page as html by it's name.
    '''
    return get_page_by_id(
        get_page_id_by_name(page_name, using),
        using
    )


def get_page_by_id(page_id, using):
    '''
    Returns the page as html by it's id.
    '''
    return library.get_instance(using).getPagesExporthtml(id=page_id)


def get_page_id_by_name(page_name, using):
    '''
    Returns the page id by it's name.
    '''
    return [x.get('id')
            for x in library.get_instance(using).getPagesList()['data']
            if x['slug'] == page_name
            ][0]


def get_chapter_by_name(chapter_name, using):
    '''
    Returns the chapter as html by it's name.
    '''
    return get_chapter_by_id(get_chapter_id_by_name(chapter_name, using), using)


def get_chapter_by_id(chapter_id, using):
    '''
    Returns the chapter as html by it's id.
    '''
    return library.get_instance(using).getChaptersExporthtml(id=chapter_id)


def get_chapter_id_by_name(chapter_name, using):
    '''
    Returns the chapter id by it's name.
    '''
    return [x.get('id')
            for x in library.get_instance(using).getChaptersList()['data']
            if x['slug'] == chapter_name
            ][0]


def get_book_by_name(book_name, using):
    '''
    Returns the book as html by it's name.
    '''
    return get_book_by_id(get_book_id_by_name(book_name, using), using)


def get_book_by_id(book_id, using):
    '''
    Returns the book as html by it's id.
    '''
    return library.get_instance(using).getBooksExporthtml(id=book_id)


def get_book_id_by_name(book_name, using):
    '''
    Returns the book id by it's name.
    '''
    return [x.get('id')
            for x in library.get_instance(using).getBooksList()['data']
            if x['slug'] == book_name
            ][0]


def get_shelf_by_name(shelf_name, using):
    '''
    Returns the shelf as html by it's name.
    '''
    return get_shelf_by_id(get_shelf_id_by_name(shelf_name, using), using)


def get_shelf_by_id(shelf_id, using):
    '''
    Returns the shelf as html by it's id.
    '''
    return library.get_instance(using).getShelvesExporthtml(id=shelf_id)


def get_shelf_id_by_name(shelf_name, using):
    '''
    Returns the shelf id by it's name.
    '''
    return [x
            for x in library.get_instance(using).getShelvesList()['data']
            if x['slug'] == shelf_name
            ][0]
