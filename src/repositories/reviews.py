from db.tables import Review


async def get_reviews() -> list[dict]:
    return await (
        Review.select(Review.all_columns(), Review.user.name)
    )


async def create_review(user_id: str, stars: int, message: str) -> dict:
    return await (
        Review.insert(
            Review(
                user=user_id,
                stars=stars,
                message=message
            )
        )
    )
