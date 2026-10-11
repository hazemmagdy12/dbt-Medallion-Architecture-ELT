import uvicorn
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from database import db

@strawberry.type
class Recommendation:
    item_name: str

@strawberry.type
class Query:
    @strawberry.field
    def get_recommendations(self, burger_id: str) -> list[Recommendation]:
        cypher_query = """
        MATCH (b:Burger {id: $burger_id})<-[:BOUGHT]-(u:User)-[:BOUGHT]->(other_item)
        WHERE other_item.id <> $burger_id
        RETURN DISTINCT other_item.name AS item_name
        """
        results = db.run_query(cypher_query, {"burger_id": burger_id})
        return [Recommendation(item_name=row["item_name"]) for row in results]

@strawberry.type
class Mutation:
    
    @strawberry.mutation
    def add_purchase(self, user_name: str, burger_id: str) -> str:
        cypher_query = """
        MATCH (u:User {name: $user_name})
        MATCH (b:Burger {id: $burger_id})
        CREATE (u)-[:BOUGHT]->(b)
        """
        db.run_query(cypher_query, {"user_name": user_name, "burger_id": burger_id})
        return f" Successfully added purchase: {user_name} bought {burger_id}"

    @strawberry.mutation
    def update_burger_price(self, burger_id: str, new_price: float) -> str:
        cypher_query = "MATCH (b:Burger {id: $burger_id}) SET b.price = $new_price"
        db.run_query(cypher_query, {"burger_id": burger_id, "new_price": new_price})
        return f" Burger {burger_id} price updated to {new_price}"

    @strawberry.mutation
    def delete_user(self, user_name: str) -> str:
        cypher_query = "MATCH (u:User {name: $user_name}) DETACH DELETE u"
        db.run_query(cypher_query, {"user_name": user_name})
        return f" User '{user_name}' and all their connections deleted successfully"

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI(title="Burger App Graph API (Full CRUD)")
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    print(" Starting GraphQL Server at http://127.0.0.1:8000/graphql")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)