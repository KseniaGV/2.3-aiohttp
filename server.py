from aiohttp import web

from database import Advertisement, Base, engine, AsyncSession


#INIT DB
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


#CREATE
async def create_ad(request):
    data = await request.json()

    async with AsyncSession() as session:
        ad = Advertisement(
            title=data.get("title"),
            description=data.get("description"),
            owner=data.get("owner"),
        )

        session.add(ad)
        await session.commit()
        await session.refresh(ad)

        return web.json_response(ad.to_dict(), status=201)


#GET one
async def get_ad(request):
    ad_id = int(request.match_info["ad_id"])

    async with AsyncSession() as session:
        ad = await session.get(Advertisement, ad_id)

        if not ad:
            return web.json_response({"error": "Advertisement not found"}, status=404)

        return web.json_response(ad.to_dict())


#GET all
async def get_ads(request):
    async with AsyncSession() as session:
        result = await session.execute(
            Advertisement.__table__.select()
        )
        rows = result.mappings().all()

        return web.json_response(list(rows))


#UPDATE
async def update_ad(request):
    ad_id = int(request.match_info["ad_id"])
    data = await request.json()

    async with AsyncSession() as session:
        ad = await session.get(Advertisement, ad_id)

        if not ad:
            return web.json_response({"error": "Advertisement not found"}, status=404)

        if "title" in data:
            ad.title = data["title"]
        if "description" in data:
            ad.description = data["description"]
        if "owner" in data:
            ad.owner = data["owner"]

        await session.commit()
        await session.refresh(ad)

        return web.json_response(ad.to_dict())


#DELETE
async def delete_ad(request):
    ad_id = int(request.match_info["ad_id"])

    async with AsyncSession() as session:
        ad = await session.get(Advertisement, ad_id)

        if not ad:
            return web.json_response({"error": "Advertisement not found"}, status=404)

        await session.delete(ad)
        await session.commit()

        return web.json_response({"status": "deleted"})


#APP
app = web.Application()

app.router.add_post("/ads", create_ad)
app.router.add_get("/ads", get_ads)
app.router.add_get("/ads/{ad_id}", get_ad)
app.router.add_patch("/ads/{ad_id}", update_ad)
app.router.add_delete("/ads/{ad_id}", delete_ad)

app.on_startup.append(lambda app: init_db())

if __name__ == "__main__":
    web.run_app(app)