# Create a class called Book which contains the members id, author_name,
# isbn, price, availability.
# Create a class called Offers which contains the members book_id,
# offer_discount_percent, start_date, end_date.

# Create a class called Store to hold the books in the store along with the store
# timings, member called directions(map location to reach the store) as well as
# the current running offers.

class Book:
    def __init__(self, name, id, author,isbn, price, availability):
        self.name = name
        self.id = id
        self.author = author
        self.isbn=isbn
        self.price=price
        self.availability=availability

class Offers:
    def __init__(self,book_id,offer_discount_percent, start_date, end_date):
        self.book_id=book_id
        self.offer_discount_percent=offer_discount_percent
        self.start_date=start_date
        self.end_date=end_date

class Store(Book,Offers):
    def __init__(self,books,offers ,id, author_name, isbn, price, availability, book_id, offer_discount_percent, start_date, end_date, store_timings, directions, current_offers):
            self.books=books
            self.offers=offers
            Book.__init__(self, id, author_name, isbn, price, availability)
            Offers.__init__(self, book_id, offer_discount_percent, start_date, end_date)
            self.store_timings = store_timings
            self.directions = directions
            self.current_offers = current_offers
            
book1=Book("Wings",10,"kalam",12,100,True)
offer1=Offers(10,5,"10-10-2023","20-10-2023")
store=(book1,offer1)
store.books.id
        
