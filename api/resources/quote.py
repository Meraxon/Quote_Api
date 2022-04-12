from api import Resource, reqparse, db
from api.models.author import AuthorModel
from api.models.quote import QuoteModel


# /authors/<int:author_id>/quotes/<int:quote_id>
class QuoteResource(Resource):
    def get(self, author_id, quote_id):
        quote = QuoteModel.query.get(quote_id)
        if quote:
            return quote.to_dict(), 200
        return {"Error": "Quote not found"}, 404

    def put(self, quote_id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("text")
        new_data = parser.parse_args()

        quote = QuoteModel.query.get(quote_id)
        quote.author = new_data["author"]
        quote.text = new_data["text"]
        db.session.commit()
        return quote.to_dict(), 200

    def delete(self, author_id=None, quote_id=None):
        author = AuthorModel.query.get(author_id)
        quote = QuoteModel.query.get(quote_id)
        if author is None:
            return {"Error": f"Author with id = {author_id} not found"}, 404
        elif quote is None:
            return {"Error": f"Quote with id = {quote_id} not found"}, 404
        db.session.delete(quote)
        db.session.commit()
        return f"{author.name}'s quote with id={quote_id} is deleted.", 200


# /authors/<int:author_id>/quotes
# /quotes
class QuoteListResource(Resource):
    def get(self, author_id=None):
        if author_id is None:  # Если запрос приходит по url: /quotes
            quotes = QuoteModel.query.all()
            return [quote.to_dict() for quote in quotes], 200  # Возвращаем ВСЕ цитаты

        author = AuthorModel.query.get(author_id)
        quotes = author.quotes.all()
        return [quote.to_dict() for quote in quotes], 200  # Возвращаем все цитаты автора

    def post(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        quote_data = parser.parse_args()
        # TODO: раскомментируйте строку ниже, чтобы посмотреть quote_data
        # print(f"{quote_data=}")
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404

        quote = QuoteModel(author, quote_data["text"])
        db.session.add(quote)
        db.session.commit()
        return quote.to_dict(), 201