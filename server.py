from aiohttp import web
from database import Advertisement, Session


async def create_ad(request):
    data = await request.json()

    with Session() as session:
        ad = Advertisement(
            title=data["title"],
            description=data["description"],
            owner=data["owner"]
        )

        session.add(ad)
        session.commit()
        session.refresh(ad)

        return web.json_response(
            {
                "id": ad.id,
                "title": ad.title,
                "description": ad.description,
                "owner": ad.owner,
                "created_at": ad.created_at.isoformat()
            },
            status=201
        )


async def get_ad(request):
    ad_id = int(request.match_info["ad_id"])

    with Session() as session:
        ad = session.get(Advertisement, ad_id)

        if ad is None:
            return web.json_response(
                {"error": "Advertisement not found"},
                status=404
            )

        return web.json_response(
            {
                "id": ad.id,
                "title": ad.title,
                "description": ad.description,
                "owner": ad.owner,
                "created_at": ad.created_at.isoformat()
            }
        )


async def update_ad(request):
    ad_id = int(request.match_info["ad_id"])
    data = await request.json()

    with Session() as session:
        ad = session.get(Advertisement, ad_id)

        if ad is None:
            return web.json_response(
                {"error": "Advertisement not found"},
                status=404
            )

        if "title" in data:
            ad.title = data["title"]

        if "description" in data:
            ad.description = data["description"]

        if "owner" in data:
            ad.owner = data["owner"]

        session.commit()

        return web.json_response(
            {
                "id": ad.id,
                "title": ad.title,
                "description": ad.description,
                "owner": ad.owner,
                "created_at": ad.created_at.isoformat()
            }
        )


async def delete_ad(request):
    ad_id = int(request.match_info["ad_id"])

    with Session() as session:
        ad = session.get(Advertisement, ad_id)

        if ad is None:
            return web.json_response(
                {"error": "Advertisement not found"},
                status=404
            )

        session.delete(ad)
        session.commit()

        return web.json_response(
            {"status": "deleted"}
        )


app = web.Application()

app.router.add_post("/ads", create_ad)
app.router.add_get("/ads/{ad_id}", get_ad)
app.router.add_patch("/ads/{ad_id}", update_ad)
app.router.add_delete("/ads/{ad_id}", delete_ad)

web.run_app(app)

