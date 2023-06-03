from dateutil.parser import parse
import requests

# Global variables

DEBUG = False

genres = ['Mistery', 'Thriller', 'Magic', 'Fantasy', 'Romance', 'Horror', 'Science Fiction']
fields = ['subject', 'author_name', 'author_key', 'isbn', 'cover_i', 'cover_edition_key']
languages = ['eng', 'spa', 'fre']
lang_dict = {'eng': 'English',
             'en': 'English',
             'spa': 'Spanish',
             'es': 'Spanish',
             'fre': 'French',
             'fr': 'French'
             }
limit = 100


class InvalidBookError(Exception):
    pass


class Book():
    def __init__(self, title=None, author=None, author_key=None, genres=None, language=None, isbn=None, cover=None,
                 book_id=None, work_id=None, publisher=None, synopsis=None):
        self.title = title
        self.author = author
        self.author_key = author_key
        self.genres = genres
        self.language = language
        self.isbn = isbn
        self.cover = cover
        self.book_id = book_id
        self.work_id = work_id
        self.publisher = publisher
        self.synopsis = synopsis

    def isValid(self):
        return self.title and self.author and self.genres and self.language and self.isbn and self.cover and self.publisher and self.synopsis

    def __repr__(self):
        return f'Book(Title: {self.title}, ' \
               f'Author: {self.author}, ' \
               f'Author_Key: {self.author_key}, ' \
               f'Subject: {self.genres}, ' \
               f'Languages: {self.language}, ' \
               f'ISBN: {self.isbn}, ' \
               f'Cover: {self.cover}, ' \
               f'BookID: {self.book_id}, ' \
               f'WorkID: {self.work_id}, ' \
               f'Publisher: {self.publisher}, ' \
               f'Synopsis: {self.synopsis}' \
               f')'


class Author():
    def __init__(self, name=None, birth_date=None, bio=None, picture=None, author_id=None):
        self.name = name
        self.birth_date = birth_date
        self.bio = bio
        self.picture = picture
        self.author_id = author_id

    def isValid(self):
        return self.name and self.birth_date and self.bio

    def __repr__(self):
        return f'Author(' \
               f'Name: {self.name}, ' \
               f'Birth Date: {self.birth_date}, ' \
               f'OL ID: {self.author_id}, ' \
               f'Biography: {self.bio}, ' \
               f'Picture: {self.picture}' \
               f')'


def findSubject(genres_original: list[str], genres_book: list[str]):
    _return = set()
    for original_genre in genres_original:
        for genre in genres_book:
            if genre.lower().find(original_genre.lower()) != -1:
                _return.add(original_genre)
                break
    return _return


def request_retry(url, num_retries=2, **kwargs):
    """Make multiple GET requests until it is successful or num_retries is reached."""
    for _ in range(num_retries):
        try:
            response = requests.get(url, **kwargs)
            if response.status_code == 200:
                ## Return response if successful
                return response
        except requests.exceptions.ConnectionError:
            pass
    return None


def getDataFromGoogleAPI(book: Book):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{book.isbn}"

    # Make a GET request to the API endpoint URL to retrieve the data from Google Books API
    r = request_retry(url)

    if r is not None:
        d = r.json()
        if d['totalItems']:
            selfLink = d['items'][0]['selfLink']
            r = request_retry(selfLink)
            if r is not None:
                d = r.json()
                d = d.get('volumeInfo')
                book.title = d.get('title')
                book.publisher = d.get('publisher') if not book.publisher else book.publisher
                book.language = lang_dict.get(d.get('language'))
                book.synopsis = d.get('description')
                if not book.synopsis:
                    getDataFromWorksAPI(book)
            else:
                raise InvalidBookError
        else:
            raise InvalidBookError
    else:
        if DEBUG: print("Book not found in Google API", book.isbn)
        raise InvalidBookError


def getDataFromBooksAPI(book: Book):
    book_url = f"https://openlibrary.org/works/{book.book_id}.json"

    # Make a GET request to the API endpoint URL to retrieve the Publisher, ISBN and WorkID
    r = request_retry(book_url)

    if r is not None:
        d = r.json()
        if d.get('isbn_13') is not None:
            book.isbn = d['isbn_13'][0]
        elif d.get('isbn_10') is not None:
            book.isbn = d['isbn_10'][0]
        else:
            if DEBUG: print("ISBN Not Found", book.book_id)
            raise InvalidBookError

        book.work_id = d['works'][0]['key'].split('/')[-1]
        if d.get('publishers') is not None:
            book.publisher = d['publishers'][0]
    else:
        if DEBUG: print("BooksAPI url not found", book.book_id)
        raise InvalidBookError


def getDataFromWorksAPI(book: Book):
    works_url = f"https://openlibrary.org/works/{book.work_id}.json"

    # Make a GET request to the API endpoint URL to retrieve the Synopsis.
    r = request_retry(works_url)

    if r is not None:
        d = r.json()
        desc = d.get('description')
        if desc is None:
            raise InvalidBookError

        if type(desc) is dict:
            book.synopsis = desc['value']
        else:
            book.synopsis = desc
    else:
        if DEBUG: print("Work Not found", book.work_id)
        raise InvalidBookError


def getAuthorInfoFromAuthorsAPI(auth: Author):
    authors_url = f"https://openlibrary.org/authors/{auth.author_id}.json"

    # Make a GET request to the API endpoint URL to retrieve the author information
    r = request_retry(authors_url)

    if r is not None:
        d = r.json()
        auth.name = d.get('name')
        birth_date = d.get('birth_date')
        auth.birth_date = parse(birth_date if birth_date else "1234")
        bio = d.get('bio')
        auth.bio = bio['value'] if type(bio) is dict else bio
        photo = d.get('photos')
        if photo is not None:
            auth.picture = f"https://covers.openlibrary.org/b/id/{photo[0]}-M.jpg"
        else:
            auth.picture = "https://openlibrary.org/images/icons/avatar_author-lg.png"
    else:
        if DEBUG: print("Author Not found", auth.author_id)


def getBookList():
    genres_str = ' OR '.join([f'"{subj}"' for subj in genres])
    languages_str = ' AND '.join(languages)
    fields_str = ','.join(fields)

    q = {
        "first_publish_year": "[1975 TO 2023]",
        "subject": f'({genres_str})',
        "language": f'({languages_str})',
    }

    query = {
        "q": ' '.join([f'{k}:{v}' for k, v in q.items()]),
        "has_fulltext": "true",
        "facet": "false",
        "fields": fields_str,
        "page": 1,
        "offset": 0,
        "limit": limit,
        "sort": "editions"
    }

    endpoint = f"https://openlibrary.org/search.json"

    valid_books = []
    # Search books while limit is not reached
    while True:
        response = requests.get(endpoint, params=query)
        if DEBUG:  print(response.url)
        json = response.json()
        books = []
        booksFound = json['numFound']
        for doc in json['docs']:
            if doc.get('cover_edition_key') is not None and doc.get('isbn') is not None:
                b = Book(
                    author_key=doc['author_key'],
                    author=doc['author_name'],
                    genres=findSubject(genres, doc['subject']),
                    book_id=doc['cover_edition_key'],
                    cover=f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-M.jpg"
                )
                books.append(b)

        for book in books:
            try:
                getDataFromBooksAPI(book)
                getDataFromGoogleAPI(book)
            except InvalidBookError:
                continue

            if book.isValid():
                if DEBUG: print("Valid Book: ", book)
                valid_books.append(book)
                if len(valid_books) == limit:
                    return valid_books
            else:
                if DEBUG: print("Invalid Book: ", book)
        # If there is not enough valid books, keep searching while books aren't finished
        if len(valid_books) < limit and (query['offset'] + limit) < booksFound:
            query['offset'] += limit
        else:
            return valid_books


def getAuthorsList(books: list[Book]):
    authors_ids = set()
    authors = []

    for book in books:
        authors_ids.update(set(book.author_key))

    for author_id in authors_ids:
        a = Author(author_id=author_id)
        getAuthorInfoFromAuthorsAPI(a)
        authors.append(a)
        if DEBUG: print(f'{"Valid" if a.isValid() else "Invalid"} author: ', a)

    return authors


def getBooksFromAPI():
    # AND: &&, OR: ||, NOT: !
    books = getBookList()
    print(f'{len(books)} complete books found!')

    authors = getAuthorsList(books)
    print(f'{len(authors)} authors found!')

    return books, authors


if __name__ == '__main__':
    getBooksFromAPI()

# Cojer libros de la query
# bookID = cover_edition_key -> Books API for the rest of specific attributes (isbn, pages, author, publisher, etc) -> https://openlibrary.org/books/OL28172760M.json
# coverID = cover_i -> cover api for covers -> "https://covers.openlibrary.org/b/id/{COVER_ID}-M.jpg"
# workID -> get From booksAPI -> https://openlibrary.org/works/OL82563W.json -> get "description" as synopsis
